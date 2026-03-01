# Fantasy Football AI Draft Assistant

A RAG (Retrieval-Augmented Generation) powered draft assistant that answers natural language fantasy football questions using real NFL data, expert rankings, and injury reports.

## What It Does

Ask questions like:

- "Who should I draft in round 3 if I need a WR?"
- "What are the injury concerns for Saquon Barkley?"
- "Which rookies have the highest upside this season?"

The system retrieves relevant data from a vector database and generates informed answers with source citations — no hallucination, just data-backed recommendations.

## Architecture

```
Question → Embed → Vector Search (ChromaDB) → Retrieved Context → LLM (Ollama) → Answer + Sources
```

## Tech Stack

- **Python 3.11**
- **LangChain** — RAG orchestration
- **ChromaDB** — vector storage
- **sentence-transformers** — embeddings (all-MiniLM-L6-v2)
- **Ollama** — local LLM inference

## Setup

Requires **Python 3.11** (for nfl_data_py compatibility). Uses [pyenv](https://github.com/pyenv/pyenv) for version management.

```bash
# Clone the repo
git clone https://github.com/mattvanharn/fantasy-draft-rag.git
cd fantasy-draft-rag

# Set Python 3.11 for this project (pyenv)
pyenv install 3.11  # if not already installed
pyenv local 3.11

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment config
cp .env.example .env
```

### Ollama Setup

```bash
# Install Ollama (Arch Linux)
sudo pacman -S ollama

# Pull a model
ollama pull llama3.2:3b

# Verify it works
ollama run llama3.2:3b "Hello, who are you?"
```

## Project Status

**Phase 1: RAG Pipeline MVP** — In Progress

See [ROADMAP](docs/ROADMAP.md) for full project plan.

## License

MIT
