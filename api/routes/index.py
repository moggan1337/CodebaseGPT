"""
CodebaseGPT - API Routes
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Query
from pydantic import BaseModel
from typing import Optional, List
import os
import shutil

from api.indexer.code_indexer import CodeIndexer
from api.services.llm import LLMService
from api.services.query_agent import QueryAgent, Citation

# Initialize services (singleton per process)
llm_service = LLMService(provider="minimax")
indexer = CodeIndexer(chunk_size=100)
query_agent = QueryAgent(indexer, llm_service)

# Create router
router = APIRouter()


class QueryRequest(BaseModel):
    question: str
    include_thinking: bool = False


class QueryResponseModel(BaseModel):
    answer: str
    citations: List[dict]
    thinking: Optional[str] = None


class SearchResult(BaseModel):
    file_path: str
    line_start: int
    line_end: int
    language: str
    preview: str


@router.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "CodebaseGPT",
        "version": "0.1.0",
        "status": "running"
    }


@router.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy"}


@router.post("/index/local")
async def index_local(path: str = Query(..., description="Path to directory to index")):
    """
    Index a local directory.
    
    Recursively scans all supported code files and creates chunks for semantic search.
    """
    if not os.path.isdir(path):
        raise HTTPException(status_code=400, detail="Path is not a directory")
    
    try:
        chunks = indexer.index_directory(path)
        return {
            "status": "success",
            "chunks_indexed": len(chunks),
            "files_processed": len(set(c.file_path for c in chunks))
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/index/file")
async def index_file(file: UploadFile = File(...)):
    """
    Upload and index a single file.
    """
    # Save to temp file
    temp_path = f"/tmp/{file.filename}"
    
    try:
        with open(temp_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        # Read content
        with open(temp_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Index file
        chunks = indexer.chunk_file(file.filename, content)
        indexer.chunks.extend(chunks)
        
        return {
            "status": "success",
            "chunks_indexed": len(chunks),
            "filename": file.filename
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)


@router.post("/query", response_model=QueryResponseModel)
async def query(request: QueryRequest):
    """
    Query the indexed codebase using natural language.
    
    Returns an answer with citations to relevant code snippets.
    """
    if not indexer.chunks:
        raise HTTPException(
            status_code=400,
            detail="No codebase indexed. Call /index/local first."
        )
    
    try:
        response = await query_agent.query(
            question=request.question,
            include_thinking=request.include_thinking
        )
        
        return QueryResponseModel(
            answer=response.answer,
            citations=[
                {
                    "file_path": c.file_path,
                    "line_number": c.line_number,
                    "snippet": c.snippet
                }
                for c in response.citations
            ],
            thinking=response.thinking
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search", response_model=List[SearchResult])
async def search(q: str = Query(..., description="Search query"), limit: int = Query(10, le=100)):
    """
    Search the codebase for files matching a query.
    """
    if not indexer.chunks:
        raise HTTPException(
            status_code=400,
            detail="No codebase indexed. Call /index/local first."
        )
    
    results = await query_agent.search(query=q, max_results=limit)
    return results


@router.get("/stats")
async def stats():
    """
    Get index statistics.
    """
    return {
        "total_chunks": len(indexer.chunks),
        "files": len(set(c.file_path for c in indexer.chunks)),
        "languages": list(set(c.language for c in indexer.chunks if c.language != 'unknown'))
    }


@router.post("/export")
async def export_index(path: str = Query("./codebase_index.json")):
    """
    Export the current index to a JSON file.
    """
    try:
        saved_path = indexer.export_index(path)
        return {"status": "success", "path": saved_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/import")
async def import_index(path: str = Query("./codebase_index.json")):
    """
    Import an index from a previously exported JSON file.
    """
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Index file not found")
    
    try:
        count = indexer.import_index(path)
        return {"status": "success", "chunks_loaded": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
