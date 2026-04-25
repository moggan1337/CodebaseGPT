"""
CodebaseGPT - Code Indexer
Parses code files and creates searchable embeddings
"""
import os
import re
import hashlib
from pathlib import Path
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
import json


@dataclass
class CodeChunk:
    """A chunk of code with metadata"""
    id: str
    content: str
    file_path: str
    start_line: int
    end_line: int
    language: str
    chunk_type: str  # 'function', 'class', 'file', 'comment'
    symbol_name: Optional[str] = None
    parent_symbol: Optional[str] = None


class CodeIndexer:
    """Indexes code files for semantic search"""
    
    # Language to file extension mapping
    LANG_EXTENSIONS = {
        'python': ['.py'],
        'javascript': ['.js', '.jsx', '.mjs', '.cjs'],
        'typescript': ['.ts', '.tsx'],
        'java': ['.java'],
        'csharp': ['.cs'],
        'cpp': ['.cpp', '.cc', '.cxx', '.h', '.hpp'],
        'go': ['.go'],
        'rust': ['.rs'],
        'ruby': ['.rb'],
        'php': ['.php'],
        'swift': ['.swift'],
        'kotlin': ['.kt', '.kts'],
        'sql': ['.sql'],
        'html': ['.html', '.htm'],
        'css': ['.css', '.scss', '.sass', '.less'],
        'json': ['.json'],
        'yaml': ['.yaml', '.yml'],
        'markdown': ['.md'],
        'shell': ['.sh', '.bash', '.zsh'],
    }
    
    def __init__(self, chunk_size: int = 1000):
        self.chunk_size = chunk_size
        self.chunks: List[CodeChunk] = []
    
    def should_index_file(self, file_path: str) -> bool:
        """Check if file should be indexed"""
        ext = Path(file_path).suffix.lower()
        
        # Check if extension is supported
        for lang, extensions in self.LANG_EXTENSIONS.items():
            if ext in extensions:
                return True
        
        return False
    
    def detect_language(self, file_path: str) -> str:
        """Detect programming language from file extension"""
        ext = Path(file_path).suffix.lower()
        
        for lang, extensions in self.LANG_EXTENSIONS.items():
            if ext in extensions:
                return lang
        
        return 'unknown'
    
    def chunk_file(self, file_path: str, content: str) -> List[CodeChunk]:
        """Split file into chunks"""
        chunks = []
        lines = content.split('\n')
        
        # Simple line-based chunking
        for i in range(0, len(lines), self.chunk_size):
            chunk_lines = lines[i:i + self.chunk_size]
            chunk_content = '\n'.join(chunk_lines)
            
            # Generate unique ID
            chunk_id = hashlib.md5(
                f"{file_path}:{i}:{chunk_content[:100]}".encode()
            ).hexdigest()
            
            chunk = CodeChunk(
                id=chunk_id,
                content=chunk_content,
                file_path=file_path,
                start_line=i + 1,
                end_line=min(i + self.chunk_size, len(lines)),
                language=self.detect_language(file_path),
                chunk_type='block'
            )
            chunks.append(chunk)
        
        return chunks
    
    def index_directory(self, directory: str) -> List[CodeChunk]:
        """Index all files in a directory"""
        all_chunks = []
        
        for root, dirs, files in os.walk(directory):
            # Skip hidden and common ignore directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in [
                'node_modules', '__pycache__', 'venv', '.venv', 'dist', 'build'
            ]]
            
            for file in files:
                file_path = os.path.join(root, file)
                
                if not self.should_index_file(file_path):
                    continue
                
                # Skip large files
                try:
                    size = os.path.getsize(file_path)
                    if size > 10 * 1024 * 1024:  # 10MB
                        continue
                    
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    chunks = self.chunk_file(file_path, content)
                    all_chunks.extend(chunks)
                    
                except Exception as e:
                    print(f"Error indexing {file_path}: {e}")
                    continue
        
        self.chunks = all_chunks
        return all_chunks
    
    def get_chunks_for_embedding(self) -> List[Dict[str, Any]]:
        """Get chunks in format ready for embedding"""
        return [
            {
                "id": chunk.id,
                "content": chunk.content,
                "metadata": {
                    "file_path": chunk.file_path,
                    "start_line": chunk.start_line,
                    "end_line": chunk.end_line,
                    "language": chunk.language,
                    "type": chunk.chunk_type
                }
            }
            for chunk in self.chunks
        ]
    
    def find_relevant_chunks(self, query: str, top_k: int = 10) -> List[CodeChunk]:
        """
        Find relevant chunks for a query
        Simple keyword matching - in production, use embeddings
        """
        import re
        # Tokenize by splitting on non-alphanumeric characters
        query_terms = set(re.findall(r'\w+', query.lower()))
        scored_chunks = []
        
        for chunk in self.chunks:
            content_terms = set(re.findall(r'\w+', chunk.content.lower()))
            
            # Calculate Jaccard similarity
            intersection = query_terms & content_terms
            if intersection:
                score = len(intersection) / len(query_terms)
                scored_chunks.append((score, chunk))
        
        # Sort by score and return top k
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        return [chunk for _, chunk in scored_chunks[:top_k]]
    
    def export_index(self, path: str):
        """Export index to JSON file"""
        data = {
            "chunks": [
                {
                    "id": c.id,
                    "content": c.content,
                    "file_path": c.file_path,
                    "start_line": c.start_line,
                    "end_line": c.end_line,
                    "language": c.language,
                    "chunk_type": c.chunk_type
                }
                for c in self.chunks
            ]
        }
        
        os.makedirs(os.path.dirname(path) if os.path.dirname(path) else '.', exist_ok=True)
        with open(path, 'w') as f:
            json.dump(data, f)
        
        return path
    
    def import_index(self, path: str) -> int:
        """Import index from JSON file"""
        with open(path, 'r') as f:
            data = json.load(f)
        
        self.chunks = [
            CodeChunk(
                id=c['id'],
                content=c['content'],
                file_path=c['file_path'],
                start_line=c['start_line'],
                end_line=c['end_line'],
                language=c['language'],
                chunk_type=c['chunk_type']
            )
            for c in data.get('chunks', [])
        ]
        
        return len(self.chunks)
