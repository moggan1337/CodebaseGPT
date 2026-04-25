"""
CodebaseGPT - Configuration
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
    # LLM Configuration (MiniMax)
    minimax_api_key: str = os.getenv("MINIMAX_API_KEY", "")
    minimax_base_url: str = "https://api.minimax.io/anthropic"
    minimax_model: str = "MiniMax-M2.7"
    
    # Alternative: OpenAI
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    openai_model: str = "gpt-4o"
    
    # Alternative: Anthropic
    anthropic_api_key: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    anthropic_model: str = "claude-sonnet-4-6"
    
    # Vector DB
    chroma_persist_directory: str = "./data/chroma"
    
    # Database
    database_url: str = "sqlite+aiosqlite:///./codebase_gpt.db"
    
    # Indexing
    chunk_size: int = 1000
    chunk_overlap: int = 100
    max_file_size_mb: int = 10
    
    # Exclude patterns
    exclude_patterns: list = [
        "node_modules/**",
        ".git/**",
        "dist/**",
        "build/**",
        "__pycache__/**",
        "*.pyc",
        ".venv/**",
        "venv/**",
        "*.min.js",
        "*.map",
    ]


settings = Settings()
