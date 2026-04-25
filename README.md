# CodebaseGPT

<p align="center">
  <img src="https://img.shields.io/badge/AI-MiniMax%20M2.7-FF6B6B?style=for-the-badge&logo=openai&logoColor=white" alt="MiniMax M2.7">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/Framework-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/UI-Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white" alt="Next.js">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

> 💬 **Chat with Your Codebase** — Ask questions about any codebase and get AI-powered answers with source code citations. Uses MiniMax M2.7's chain-of-thought reasoning for detailed explanations.

## About

**CodebaseGPT** is an intelligent code exploration tool that lets you ask questions about any codebase in natural language. It indexes your code, understands its structure, and provides answers with precise citations pointing to the exact file and line numbers.

### Who It's For

- **Developers** — Understand unfamiliar codebases quickly
- **Onboarding Teams** — Help new engineers get up to speed
- **Code Reviewers** — Understand context and dependencies
- **Technical Writers** — Extract information for documentation
- **Architects** — Analyze system design and patterns

## ✨ Features

### 🔍 Core Capabilities

- **Semantic Code Search** — Find code using natural language queries
- **Natural Language Queries** — Ask questions in plain English
- **Cited Answers** — Every answer includes source code citations with file paths and line numbers
- **Chain-of-Thought Reasoning** — Uses MiniMax M2.7 thinking to provide detailed explanations
- **Multi-language Support** — Python, JavaScript, TypeScript, Go, Rust, Java, C++, and more

### 🌐 Interface Options

| Interface | Description |
|-----------|-------------|
| **Web UI** | Beautiful Next.js chat interface |
| **CLI Tool** | Work from the command line |
| **REST API** | Integrate with other tools and workflows |

### 🔧 Technical Features

- **Chunked Indexing** — Handles large codebases efficiently
- **Language Detection** — Automatic programming language recognition
- **AST Parsing** — Deep code structure understanding
- **Embeddings** — Semantic code similarity search
- **Multi-Provider LLM** — Supports MiniMax, OpenAI, and Anthropic

## 📐 Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                          CodebaseGPT                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                      Interface Layer                          │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐                    │   │
│  │  │   Web    │  │   CLI    │  │   REST   │                    │   │
│  │  │   (Next) │  │  (Click) │  │  (Fast)  │                    │   │
│  │  └──────────┘  └──────────┘  └──────────┘                    │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                    Indexer Layer                              │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐               │   │
│  │  │   File     │  │  Language  │  │   Chunk   │               │   │
│  │  │   Walker   │  │  Detector  │  │   Splitter │               │   │
│  │  └────────────┘  └────────────┘  └────────────┘               │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                    Query Engine                               │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐               │   │
│  │  │  Embedding │  │  Similarity│  │   LLM     │               │   │
│  │  │   Search   │  │   Match    │  │  Agent    │               │   │
│  │  └────────────┘  └────────────┘  └────────────┘               │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                    Response Generator                         │   │
│  │  ┌──────────────────────────────────────────────────────┐   │   │
│  │  │  • Formatted answer with Markdown                      │   │   │
│  │  │  • Inline code citations [file:line]                   │   │   │
│  │  │  • Chain-of-thought reasoning                          │   │   │
│  │  │  • Confidence scores                                   │   │   │
│  │  └──────────────────────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## 🛠️ Installation

### Prerequisites

- Python 3.11+
- Node.js 18+ (for frontend)
- API key (MINIMAX_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY)

### Backend Installation

```bash
# Clone the repository
git clone https://github.com/moggan1337/CodebaseGPT.git
cd CodebaseGPT

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your API key
```

### Frontend Installation

```bash
cd frontend
npm install
cd ..
```

## 🚀 Quick Start

### 1. Set API Key

```bash
# MiniMax (default)
export MINIMAX_API_KEY=your_minimax_api_key

# Or use OpenAI
export OPENAI_API_KEY=your_openai_api_key

# Or use Anthropic
export ANTHROPIC_API_KEY=your_anthropic_api_key
```

### 2. Start Backend

```bash
uvicorn api.main:app --reload --port 8000
```

### 3. Start Frontend (Optional)

```bash
cd frontend
npm run dev
# Open http://localhost:3000
```

### 4. Index and Query

```bash
# Index a codebase
curl -X POST "http://localhost:8000/index/local?path=/path/to/your/code"

# Ask a question
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "How does authentication work?", "include_thinking": true}'
```

## 📚 CLI Usage

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

Open http://localhost:3000 to:

1. Enter a codebase path and click "Index"
2. Wait for indexing to complete
3. Ask questions in the chat interface
4. View citations and chain-of-thought reasoning

## 📡 API Reference

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `GET /` | GET | API info and status |
| `GET /health` | GET | Health check |
| `POST /index/local?path=X` | POST | Index a local directory |
| `POST /index/file` | POST | Upload and index a file |
| `POST /query` | POST | Query with JSON body |
| `GET /search?q=X&limit=10` | GET | Search code |
| `GET /stats` | GET | Index statistics |
| `POST /export?path=X` | POST | Export index to JSON |
| `POST /import?path=X` | POST | Import index from JSON |

### Query Request

```json
{
  "question": "How does authentication work?",
  "include_thinking": true,
  "max_citations": 5
}
```

### Query Response

```json
{
  "answer": "Authentication works by...\n\n**Key Files:**\n- `auth/login.py:42` - Main login handler\n- `auth/middleware.py:15` - JWT validation middleware",
  "thinking": "To answer this question, I analyzed the auth module...",
  "citations": [
    {
      "file": "auth/login.py",
      "line": 42,
      "snippet": "def login(username, password):\n    user = db.query(User).filter_by(username=username).first()"
    }
  ],
  "confidence": 0.92
}
```

## 🔧 Configuration

### Environment Variables

```bash
# LLM Provider (MiniMax default)
MINIMAX_API_KEY=your_api_key
MINIMAX_MODEL=MiniMax-M2.7

# Alternative providers
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-4o

ANTHROPIC_API_KEY=your_anthropic_key
ANTHROPIC_MODEL=claude-sonnet-4-6

# Indexing settings
CHUNK_SIZE=1000
CHUNK_OVERLAP=100
MAX_FILE_SIZE_MB=10

# Server settings
HOST=0.0.0.0
PORT=8000
```

### Advanced Configuration

```python
# In api/config.py
class Settings:
    # Indexing
    chunk_size: int = 1000
    chunk_overlap: int = 100
    max_file_size_mb: int = 10
    supported_extensions: list = [
        ".py", ".js", ".ts", ".jsx", ".tsx",
        ".go", ".rs", ".java", ".cpp", ".c", ".h"
    ]
    
    # LLM
    default_provider: str = "minimax"
    temperature: float = 0.7
    max_tokens: int = 4096
    
    # Search
    max_citations: int = 10
    similarity_threshold: float = 0.7
```

## 📂 Project Structure

```
CodebaseGPT/
├── api/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry
│   ├── config.py            # Settings and configuration
│   ├── routes/
│   │   ├── __init__.py
│   │   └── index.py         # /index, /query, /search endpoints
│   ├── indexer/
│   │   ├── __init__.py
│   │   └── code_indexer.py  # Code parsing and chunking
│   └── services/
│       ├── __init__.py
│       ├── llm.py           # Multi-provider LLM integration
│       └── query_agent.py   # Query handling with citations
├── cli/
│   ├── __init__.py
│   └── main.py              # Click-based CLI commands
├── frontend/
│   ├── app/
│   │   ├── layout.tsx      # Root layout
│   │   ├── page.tsx        # Main chat UI
│   │   └── globals.css     # Global styles
│   ├── lib/
│   │   └── api.ts          # API client
│   ├── package.json
│   └── next.config.js
├── tests/
│   ├── test_indexer.py
│   └── test_query.py
├── .env.example            # Environment template
├── requirements.txt        # Python dependencies
├── pyproject.toml          # Project configuration
└── README.md
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_indexer.py -v

# Run with coverage
pytest --cov=api --cov-report=html
```

## 🔍 Example Session

```
$ python -m cli.main ask ./my-project "How does the payment processing work?"

Analyzing codebase...
Found 12 relevant files.

Payment processing works as follows:

1. **Order Creation** - When a customer places an order, `payments/checkout.py:45` 
   creates an Order record and initiates the payment flow.

2. **Payment Gateway** - The `PaymentGateway` class at `payments/gateway.py:23` 
   handles communication with Stripe:
   
   ```python
   class PaymentGateway:
       def charge(self, amount, payment_method):
           stripe.Charge.create(
               amount=int(amount * 100),
               currency='usd',
               payment_method=payment_method
           )
       ```

3. **Webhook Handling** - Stripe webhooks are processed at `payments/webhooks.py:67`
   to confirm successful payments and update order status.

4. **Database Updates** - After confirmation, order status is updated in 
   `orders/models.py:89` via the `Order.mark_paid()` method.

Key files:
- payments/checkout.py
- payments/gateway.py  
- payments/webhooks.py
- orders/models.py
```

## 🤝 Contributing

1. **Fork** the repository
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Setup

```bash
git clone https://github.com/moggan1337/CodebaseGPT.git
cd CodebaseGPT
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"

# Frontend
cd frontend && npm install && cd ..

# Run tests
pytest tests/ -v
```

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<p align="center">
  Built with ❤️ and MiniMax M2.7
</p>
