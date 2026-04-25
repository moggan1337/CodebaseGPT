"""
CodebaseGPT - API Tests
"""
import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "CodebaseGPT"
    assert "version" in data


def test_health():
    """Test health check"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_stats_empty():
    """Test stats with no index"""
    response = client.get("/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total_chunks"] == 0
    assert data["files"] == 0


def test_index_local_missing_path():
    """Test index with missing directory"""
    response = client.post("/index/local?path=/nonexistent/path")
    assert response.status_code == 400


def test_query_without_index():
    """Test query without indexing first"""
    response = client.post("/query", json={"question": "test"})
    assert response.status_code == 400


def test_search_without_index():
    """Test search without indexing first"""
    response = client.get("/search?q=test")
    assert response.status_code == 400


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
