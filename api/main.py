"""
CodebaseGPT - Main FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from api.config import settings
from api.routes import index as index_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan"""
    print("🚀 Starting CodebaseGPT API...")
    yield
    print("👋 Shutting down CodebaseGPT...")


# Create FastAPI app
app = FastAPI(
    title="CodebaseGPT",
    description="Chat with your codebase - AI-powered code understanding",
    version="0.1.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(index_routes.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "CodebaseGPT",
        "version": "0.1.0",
        "description": "Chat with your codebase",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy"}


# Run with: uvicorn api.main:app --reload --port 8000
