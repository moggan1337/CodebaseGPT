# CodebaseGPT

AI-powered code understanding - ask questions about any codebase with cited answers.

## Architecture

```
codebase-gpt/
├── api/                    # FastAPI backend
│   ├── main.py            # FastAPI app entry
│   ├── config.py          # Settings (LLM, indexing)
│   ├── indexer/           # Code parsing & chunking
│   │   └── code_indexer.py
│   ├── services/          # LLM integration
│   │   ├── llm.py         # Multi-provider (MiniMax, OpenAI, Anthropic)
│   │   └── query_agent.py # Query handling with citations
│   └── routes/            # API endpoints
│       └── index.py       # /index/local, /query, /search
├── cli/                   # Command-line tool
│   └── main.py            # Click-based CLI
├── frontend/              # Next.js web UI
│   ├── app/              # App Router pages
│   └── lib/              # API client
└── tests/                # Unit tests
```

## Key Commands

### Backend
```bash
# Install dependencies
pip install -r requirements.txt

# Start API server
uvicorn api.main:app --reload --port 8000

# With MiniMax API key
export MINIMAX_API_KEY=your-key
```

### Frontend
```bash
cd frontend
npm install
npm run dev  # http://localhost:3000
```

### CLI
```bash
# Index a codebase
python -m cli.main index /path/to/project

# Ask questions
python -m cli.main ask /path/to/project "How does auth work?"

# Search
python -m cli.main search /path/to/project "login"
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info |
| `/health` | GET | Health check |
| `/index/local?path=X` | POST | Index a directory |
| `/query` | POST | Query the indexed codebase |
| `/search?q=X` | GET | Search code |
| `/stats` | GET | Index statistics |
| `/export` | POST | Export index to JSON |
| `/import` | POST | Import index from JSON |

## Configuration

Environment variables:
- `MINIMAX_API_KEY` - MiniMax API key (default provider)
- `MINIMAX_MODEL` - Model name (default: MiniMax-M2.7)
- `OPENAI_API_KEY` - OpenAI fallback
- `ANTHROPIC_API_KEY` - Anthropic fallback

## Supported Languages

Python, JavaScript, TypeScript, Java, C#, C++, Go, Rust, Ruby, PHP, Swift, Kotlin, SQL, HTML, CSS, JSON, YAML, Markdown, Shell
