"""
CodebaseGPT - Query Agent
Handles natural language queries against indexed codebase
"""
from typing import List, Optional, Dict
from dataclasses import dataclass

from api.indexer.code_indexer import CodeIndexer, CodeChunk
from api.services.llm import LLMService


@dataclass
class Citation:
    """A citation to source code"""
    file_path: str
    line_number: int
    snippet: str
    relevance_score: float


@dataclass
class QueryResponse:
    """Response to a query"""
    answer: str
    citations: List[Citation]
    thinking: Optional[str] = None


class QueryAgent:
    """Agent that answers questions about code"""
    
    SYSTEM_PROMPT = """You are CodebaseGPT, an expert at understanding and explaining code.

Your task is to answer user questions about their codebase based on the provided code snippets.

Guidelines:
- Answer in natural language
- Be specific and reference actual code
- If you're unsure, say so
- Provide code examples when helpful
- Explain what code does, not just what it says
- Suggest improvements when relevant

Format your response with:
1. Direct answer to the question
2. Code references (file:line)
3. Explanation of how the code works
"""
    
    def __init__(self, indexer: CodeIndexer, llm: LLMService):
        self.indexer = indexer
        self.llm = llm
    
    async def query(
        self,
        question: str,
        max_context_chunks: int = 10,
        include_thinking: bool = True
    ) -> QueryResponse:
        """
        Answer a question about the codebase
        """
        
        # Find relevant code chunks
        relevant_chunks = self.indexer.find_relevant_chunks(
            question,
            top_k=max_context_chunks
        )
        
        if not relevant_chunks:
            return QueryResponse(
                answer="I couldn't find any relevant code in the indexed codebase. Try re-indexing or using different search terms.",
                citations=[]
            )
        
        # Build context from chunks
        context = self._build_context(relevant_chunks)
        
        # Generate answer using LLM
        prompt = self._build_prompt(question, context)
        
        try:
            response = await self.llm.generate(
                prompt=prompt,
                system=self.SYSTEM_PROMPT,
                max_tokens=2000,
                thinking=include_thinking
            )
            
            answer = self.llm.extract_text(response)
            thinking = self.llm.extract_thinking(response) if include_thinking else None
            
            # Create citations
            citations = self._create_citations(relevant_chunks)
            
            return QueryResponse(
                answer=answer,
                citations=citations,
                thinking=thinking
            )
        
        except Exception as e:
            return QueryResponse(
                answer=f"Error generating answer: {str(e)}",
                citations=[]
            )
    
    def _build_context(self, chunks: List[CodeChunk]) -> str:
        """Build context string from code chunks"""
        context_parts = []
        
        for i, chunk in enumerate(chunks, 1):
            header = f"--- Code Snippet {i} ---\n"
            header += f"File: {chunk.file_path}\n"
            header += f"Lines: {chunk.start_line}-{chunk.end_line}\n"
            if chunk.language != 'unknown':
                header += f"Language: {chunk.language}\n"
            header += "\n"
            
            # Truncate long chunks
            content = chunk.content
            if len(content) > 500:
                content = content[:500] + "..."
            
            context_parts.append(header + content)
        
        return "\n\n".join(context_parts)
    
    def _build_prompt(self, question: str, context: str) -> str:
        """Build the full prompt for the LLM"""
        return f"""Based on the following code from the codebase, answer this question:

Question: {question}

---
{context}
---

Answer the question using the code above. Reference specific files and line numbers when explaining.
Cite your sources at the end of your response."""
    
    def _create_citations(self, chunks: List[CodeChunk]) -> List[Citation]:
        """Create citations from code chunks"""
        citations = []
        
        for chunk in chunks:
            snippet = chunk.content[:200] + "..." if len(chunk.content) > 200 else chunk.content
            
            citation = Citation(
                file_path=chunk.file_path,
                line_number=chunk.start_line,
                snippet=snippet,
                relevance_score=1.0  # In production, use actual relevance score
            )
            citations.append(citation)
        
        return citations
    
    async def search(
        self,
        query: str,
        max_results: int = 10
    ) -> List[Dict]:
        """
        Search the codebase for relevant code
        Returns formatted search results
        """
        chunks = self.indexer.find_relevant_chunks(query, top_k=max_results)
        
        results = []
        for chunk in chunks:
            results.append({
                "file_path": chunk.file_path,
                "line_start": chunk.start_line,
                "line_end": chunk.end_line,
                "language": chunk.language,
                "preview": chunk.content[:300] + "..." if len(chunk.content) > 300 else chunk.content
            })
        
        return results
