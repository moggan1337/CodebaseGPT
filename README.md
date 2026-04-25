# CodebaseGPT

<p align="center">
  <img src="https://img.shields.io/badge/AI-MiniMax%20M2.7-FF6B6B?style=for-the-badge&logo=openai&logoColor=white" alt="MiniMax M2.7">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Framework-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/UI-Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white" alt="Next.js">
</p>

> 💬 **Chat with Your Codebase** - Ask questions about any codebase and get AI-powered answers with source code citations.

## ✨ Features

- 🔍 **Semantic Code Search** - Find code using natural language
- 💬 **Natural Language Queries** - Ask questions in plain English
- 📚 **Cited Answers** - Every answer includes source code citations with file paths and line numbers
- 🧠 **Chain-of-Thought Reasoning** - Uses MiniMax M2.7 thinking to provide detailed explanations
- 🌐 **Web UI** - Beautiful Next.js interface
- ⌨️ **CLI Tool** - Work from the command line
- 📡 **REST API** - Integrate with other tools

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Backend
pip install -r requirements.txt

# Frontend
cd frontend && npm install && cd ..
```

### 2. Set API Key

```bash
export MINIMAX_API_KEY=your_minimax_api_key
```

### 3. Start the Backend

```bash
uvicorn api.main:app --reload --port 8000
```

### 4. Start the Frontend (optional)

```bash
cd frontend && npm run dev
# Open http://localhost:3000
```

### 5. Index and Query

```bash
# Index a codebase
curl -X POST "http://localhost:8000/index/local?path=/path/to/your/code"

# Ask a question
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "How does authentication work?", "include_thinking": true}'
```

## 📦 CLI Usage

```bash
# Index a project
python -m cli.main index ./my-project

# Ask questions
python -m cli.main ask ./my-project "How does authentication work?"
python -m cli.main ask ./my-project "Where is the user model defined?"

# Search code
python -m cli.main search ./my-project "authentication"

# View stats
python -m cli.main stats ./my-project
```

## 🌐 Web UI

The frontend provides an interactive chat interface:

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000 to:
1. Enter a codebase path and click "Index"
2. Ask questions in the chat
3. View citations and thinking

## 📡 API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `GET /` | GET | API info |
| `GET /health` | GET | Health check |
| `POST /index/local?path=X` | POST | Index a directory |
| `POST /index/file` | POST | Upload and index a file |
| `POST /query` | POST | Query with JSON body `{"question": "...", "include_thinking": true}` |
| `GET /search?q=X&limit=10` | GET | Search code |
| `GET /stats` | GET | Index statistics |
| `POST /export?path=X` | POST | Export index to JSON |
| `POST /import?path=X` | POST | Import index from JSON |

## 🔧 Configuration

Environment variables (in `.env`):

```bash
# LLM Provider (MiniMax default)
MINIMAX_API_KEY=your_api_key
MINIMAX_MODEL=MiniMax-M2.7

# Alternative providers
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-4o

ANTHROPIC_API_KEY=your_anthropic_key
ANTHROPIC_MODEL=claude-sonnet-4-6

# Indexing
CHUNK_SIZE=1000
CHUNK_OVERLAP=100
MAX_FILE_SIZE_MB=10
```

## 📁 Project Structure

```
CodebaseGPT/
├── api/                    # FastAPI backend
│   ├── main.py             # App entry point
│   ├── config.py            # Settings
│   ├── routes/              # API endpoints
│   │   └── index.py         # /index, /query, /search
│   ├── indexer/             # Code parsing
│   │   └── code_indexer.py  # Chunking & language detection
│   └── services/            # LLM integration
│       ├── llm.py           # Multi-provider (MiniMax, OpenAI, Anthropic)
│       └── query_agent.py   # Query handling with citations
├── cli/                     # CLI tool
│   └── main.py              # Click-based commands
├── frontend/                # Next.js UI
│   ├── app/                # Pages and layouts
│   │   ├── layout.tsx
│   │   ├── page.tsx        # Main chat UI
│   │   └── globals.css
│   └── lib/
│       └── api.ts          # API client
├── requirements.txt
├── README.md
└── CLAUDE.md
```

## 🧪 Testing

```bash
# Run tests
pytest tests/ -v
```

## 📝 License

MIT

---

<p align="center">
  Built with ❤️ and MiniMax M2.7
</p>
