#!/usr/bin/env python3
"""
CodebaseGPT CLI - Chat with your codebase from the command line
"""
import asyncio
import os
import sys
import click
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.indexer.code_indexer import CodeIndexer
from api.services.llm import LLMService
from api.services.query_agent import QueryAgent

console = Console()


@click.group()
def cli():
    """CodebaseGPT CLI - Chat with your codebase"""
    pass


@cli.command()
@click.argument("path", type=click.Path(exists=True))
@click.option("--chunk-size", default=100, help="Lines per chunk")
def index(path: str, chunk_size: int):
    """Index a codebase directory"""
    console.print(f"🔍 Indexing {path}...")
    
    indexer = CodeIndexer(chunk_size=chunk_size)
    chunks = indexer.index_directory(path)
    
    console.print(f"✅ Indexed {len(chunks)} chunks from {len(set(c.file_path for c in chunks))} files")
    
    # Save index
    index_path = os.path.join(path, ".codebase_gpt_index.json")
    indexer.export_index(index_path)
    console.print(f"📦 Index saved to {index_path}")


@cli.command()
@click.argument("path", type=click.Path(exists=True))
@click.argument("question")
@click.option("--provider", default="minimax", type=click.Choice(["minimax", "openai", "anthropic"]))
def ask(path: str, question: str, provider: str):
    """Ask a question about indexed codebase"""
    asyncio.run(_ask(path, question, provider))


async def _ask(path: str, question: str, provider: str):
    """Async implementation of ask"""
    
    # Check for existing index
    index_path = os.path.join(path, ".codebase_gpt_index.json")
    
    indexer = CodeIndexer()
    
    if os.path.exists(index_path):
        console.print(f"📂 Loading existing index from {index_path}...")
        indexer.import_index(index_path)
    else:
        console.print(f"🔍 Indexing {path} first...")
        indexer.index_directory(path)
        indexer.export_index(index_path)
    
    if not indexer.chunks:
        console.print("❌ No code found to index")
        return
    
    console.print(f"📊 Indexed {len(indexer.chunks)} chunks")
    
    # Create query agent
    llm = LLMService(provider=provider)
    query_agent = QueryAgent(indexer, llm)
    
    # Ask question
    console.print(Panel(f"[bold cyan]Q:[/bold cyan] {question}", title="Question"))
    console.print()
    console.print("[dim]Thinking...[/dim]")
    
    try:
        response = await query_agent.query(question, include_thinking=True)
        
        # Display thinking if available
        if response.thinking:
            console.print(Panel(
                response.thinking[:1000] + ("..." if len(response.thinking) > 1000 else ""),
                title="🤔 Thinking",
                border_style="yellow"
            ))
        
        # Display answer
        console.print(Panel(
            response.answer,
            title="💬 Answer",
            border_style="green"
        ))
        
        # Display citations
        if response.citations:
            console.print()
            console.print("[bold]📚 Citations:[/bold]")
            for i, citation in enumerate(response.citations[:5], 1):
                console.print(f"  {i}. {citation.file_path}:{citation.line_number}")
    
    except Exception as e:
        console.print(f"❌ Error: {e}")


@cli.command()
@click.argument("path", type=click.Path(exists=True))
@click.argument("query")
def search(path: str, query: str):
    """Search for code in indexed codebase"""
    
    index_path = os.path.join(path, ".codebase_gpt_index.json")
    
    indexer = CodeIndexer()
    
    if os.path.exists(index_path):
        indexer.import_index(index_path)
    else:
        console.print(f"❌ No index found at {index_path}. Run `ask` first.")
        return
    
    results = indexer.find_relevant_chunks(query, top_k=10)
    
    if not results:
        console.print("❌ No results found")
        return
    
    console.print(f"🔍 Found {len(results)} results:\n")
    
    for i, chunk in enumerate(results, 1):
        console.print(f"[bold]{i}. {chunk.file_path}:{chunk.start_line}-{chunk.end_line}[/bold]")
        console.print(f"   [dim]{chunk.language}[/dim]")
        
        # Show preview with syntax highlighting
        preview = chunk.content[:200] + "..." if len(chunk.content) > 200 else chunk.content
        syntax = Syntax(preview, chunk.language if chunk.language != 'unknown' else 'text')
        console.print(syntax)
        console.print()


@cli.command()
@click.argument("path", type=click.Path(exists=True))
def stats(path: str):
    """Show stats about indexed codebase"""
    
    index_path = os.path.join(path, ".codebase_gpt_index.json")
    
    if not os.path.exists(index_path):
        console.print(f"❌ No index found at {index_path}")
        return
    
    indexer = CodeIndexer()
    indexer.import_index(index_path)
    
    files = set(c.file_path for c in indexer.chunks)
    languages = set(c.language for c in indexer.chunks if c.language != 'unknown')
    
    console.print(Panel(
        f"[bold]Total Chunks:[/bold] {len(indexer.chunks)}\n"
        f"[bold]Total Files:[/bold] {len(files)}\n"
        f"[bold]Languages:[/bold] {', '.join(sorted(languages)) if languages else 'None detected'}",
        title="📊 Index Statistics"
    ))


if __name__ == "__main__":
    cli()
