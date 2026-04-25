# CodebaseGPT

<p align="center">
  <img src="https://img.shields.io/badge/Chat-Codebase-FF6B6B?style=for-the-badge&logo=openai&logoColor=white" alt="AI">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

> 💬 **Chat with Your Codebase** - Understand entire repos with AI. Answers questions with citations, cross-references, and context.

## ✨ Features

### Understanding
- 🔍 **Code Search** - Semantic search across all code
- 📚 **Context Awareness** - Understands imports, inheritance
- 🗺️ **Call Graphs** - How functions connect
- 📝 **Documentation** - Reads docs alongside code
- 🏷️ **Code Mapping** - Maps files to features

### Conversation
- 💬 **Natural Language** - Ask in plain English
- 📖 **Cited Answers** - Source code citations
- 🔗 **Deep Links** - Click to source
- 📊 **Metrics** - Code statistics on demand
- 🛠️ **Refactoring** - Suggest improvements

### Indexing
- 🐙 **GitHub** - Index repos from GitHub
- 📁 **Local** - Index local directories
- 🌐 **Enterprise** - Index private codebases
- 🔄 **Auto-Sync** - Keep index updated

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      CodebaseGPT Architecture                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    Query Interface                         │   │
│  │  - Web UI (Next.js)                                        │   │
│  │  - CLI Tool                                                │   │
│  │  - API                                                     │   │
│  │  - VS Code Extension                                       │   │
│  └──────────────────────────────────────────────────────────┘   │
│                             │                                    │
│  ┌──────────────────────────┴──────────────────────────────────┐ │
│  │                    Query Understanding                       │ │
│  │  ┌──────────────────────────────────────────────────────┐   │ │
│  │  │ LLM Agent                                               │   │ │
│  │  │ - Intent classification                               │   │ │
│  │  │ - Entity extraction (files, functions, concepts)      │   │ │
│  │  │ - Follow-up questions                                 │   │ │
│  │  └──────────────────────────────────────────────────────┘   │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                             │                                    │
│  ┌──────────────────────────┴──────────────────────────────────┐ │
│  │                    Codebase Index                           │ │
│  │  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌─────────────┐ │ │
│  │  │  AST      │ │ Embeddings│ │   Git     │ │   Symbol    │ │ │
│  │  │  Index    │ │  (Vector) │ │  History  │ │   Index     │ │ │
│  │  └───────────┘ └───────────┘ └───────────┘ └─────────────┘ │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                             │                                    │
│  ┌──────────────────────────┴──────────────────────────────────┐ │
│  │                    Retrieval & Generation                     │ │
│  │  ┌──────────────────────────────────────────────────────┐   │ │
│  │  │ Retrieval → LLM → Response + Citations                │   │ │
│  │  └──────────────────────────────────────────────────────┘   │ │
│  └──────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## 📦 Installation

```bash
git clone https://github.com/moggan1337/CodebaseGPT.git
cd CodebaseGPT

# Backend
pip install -r requirements.txt
cp .env.example .env
# Configure ANTHROPIC_API_KEY or OPENAI_API_KEY

# Frontend
cd frontend && npm install

# Index a codebase
codebase index ./my-project

# Start server
uvicorn api.main:app --reload
```

## 🚀 Usage

### CLI

```bash
# Index a project
codebase index ./my-project --name "my-project"

# Ask questions
codebase ask "How does authentication work?"
codebase ask "Where is the user model defined?"
codebase ask "What does the payment processing flow look like?"

# Search
codebase search "authentication middleware"
```

### Web UI

```bash
# Start web interface
cd frontend && npm run dev
# Open http://localhost:3000
```

### Python API

```python
from codebase_gpt import CodebaseQa

qa = CodebaseQa("./my-project")
response = qa.ask("How does the caching layer work?")

print(response.answer)
# "The caching layer uses Redis with a TTL of 3600 seconds..."

for citation in response.citations:
    print(f"Line {citation.line_number}: {citation.file}")
    print(f">>> {citation.snippet}")
```

## 📁 Project Structure

```
codebase-gpt/
├── api/
│   ├── main.py              # FastAPI app
│   ├── indexer/              # Code indexing
│   │   ├── parser.py         # AST parsing
│   │   ├── embedder.py       # Embedding generation
│   │   └── indexer.py        # ChromaDB/PGVector
│   ├── agents/
│   │   └── query_agent.py    # LLM query handling
│   └── routes/
│       ├── query.py          # Query endpoints
│       └── index.py          # Index endpoints
├── frontend/
│   ├── app/                 # Next.js app
│   ├── components/
│   └── lib/
├── cli/
│   └── main.py              # CLI tool
├── examples/
│   └── integrations/
└── tests/
```

## 🔧 Configuration

```yaml
# config.yaml
llm:
  provider: anthropic  # or openai
  model: claude-sonnet-4-6  # or gpt-4o
  temperature: 0.3

indexing:
  chunk_size: 1000
  chunk_overlap: 100
  exclude:
    - "*.test.ts"
    - "node_modules/**"
    - "dist/**"

vector_db:
  type: chroma  # or pgvector
  persist_directory: .codebase/index
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Test with specific repo
pytest tests/test_indexer.py -v --repo ./test-project

# Test query accuracy
pytest tests/test_accuracy.py -v
```

## 📚 Documentation

- [Installation Guide](docs/installation.md)
- [Quick Start](docs/quickstart.md)
- [CLI Reference](docs/cli.md)
- [API Reference](docs/api.md)
- [Integrations](docs/integrations.md)
- [Deployment](docs/deployment.md)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Add tests
4. Submit PR

## 📄 License

MIT License

---

<p align="center">
  Ask anything about your codebase
</p>
