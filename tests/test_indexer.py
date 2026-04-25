"""
CodebaseGPT - Indexer Tests
"""
import pytest
import os
import tempfile
from api.indexer.code_indexer import CodeIndexer, CodeChunk


class TestCodeIndexer:
    """Test the code indexer"""

    def test_should_index_file_python(self):
        """Test Python file detection"""
        indexer = CodeIndexer()
        assert indexer.should_index_file("test.py") == True
        assert indexer.should_index_file("main.py") == True
        assert indexer.should_index_file("test.pyw") == False

    def test_should_index_file_javascript(self):
        """Test JavaScript file detection"""
        indexer = CodeIndexer()
        assert indexer.should_index_file("app.js") == True
        assert indexer.should_index_file("index.jsx") == True
        assert indexer.should_index_file("test.ts") == True

    def test_detect_language(self):
        """Test language detection"""
        indexer = CodeIndexer()
        assert indexer.detect_language("test.py") == "python"
        assert indexer.detect_language("app.js") == "javascript"
        assert indexer.detect_language("app.ts") == "typescript"
        assert indexer.detect_language("main.go") == "go"
        assert indexer.detect_language("lib.rs") == "rust"
        assert indexer.detect_language("unknown.xyz") == "unknown"

    def test_chunk_file(self):
        """Test file chunking"""
        indexer = CodeIndexer(chunk_size=10)
        content = "\n".join([f"line {i}" for i in range(50)])
        chunks = indexer.chunk_file("test.py", content)
        
        assert len(chunks) == 5
        assert all(isinstance(c, CodeChunk) for c in chunks)
        assert chunks[0].file_path == "test.py"
        assert chunks[0].language == "python"

    def test_chunk_file_small(self):
        """Test small file chunking"""
        indexer = CodeIndexer(chunk_size=100)
        content = "def hello():\n    print('hi')"
        chunks = indexer.chunk_file("test.py", content)
        
        assert len(chunks) == 1
        assert chunks[0].content == content

    def test_index_directory(self):
        """Test directory indexing"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test files
            py_file = os.path.join(tmpdir, "test.py")
            js_file = os.path.join(tmpdir, "app.js")
            
            with open(py_file, "w") as f:
                f.write("def hello():\n    print('hello')")
            
            with open(js_file, "w") as f:
                f.write("function hello() { console.log('hello'); }")
            
            indexer = CodeIndexer(chunk_size=100)
            chunks = indexer.index_directory(tmpdir)
            
            assert len(chunks) >= 2
            file_paths = set(c.file_path for c in chunks)
            assert py_file in file_paths
            assert js_file in file_paths

    def test_find_relevant_chunks(self):
        """Test relevance search"""
        indexer = CodeIndexer()
        indexer.chunks = [
            CodeChunk("1", "def hello():\n    print('hello')", "test.py", 1, 2, "python", "function"),
            CodeChunk("2", "class User:\n    pass", "user.py", 1, 2, "python", "class"),
            CodeChunk("3", "const x = 1", "app.js", 1, 1, "javascript", "variable"),
        ]
        
        # Search for "hello" should find the Python function
        results = indexer.find_relevant_chunks("hello", top_k=2)
        assert len(results) <= 2
        assert len(results) >= 1  # Should find at least one result
        assert any("hello" in c.content.lower() for c in results)

    def test_export_import_index(self):
        """Test index persistence"""
        with tempfile.TemporaryDirectory() as tmpdir:
            indexer = CodeIndexer(chunk_size=100)
            indexer.chunks = [
                CodeChunk("abc123", "def test():\n    pass", "test.py", 1, 2, "python", "function"),
            ]
            
            export_path = os.path.join(tmpdir, "index.json")
            indexer.export_index(export_path)
            
            new_indexer = CodeIndexer()
            count = new_indexer.import_index(export_path)
            
            assert count == 1
            assert new_indexer.chunks[0].content == "def test():\n    pass"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
