# Fantasy Football AI Draft Assistant

A hybrid AI draft assistant that combines a RAG (Retrieval-Augmented Generation) knowledge base with an analytics engine to answer natural language fantasy football questions — grounded in real stats, ADP data, and expert analysis.

## What It Does

Ask questions like:

- "Round 4, pick 8 — I have 2 RBs and 1 WR, who should I take?"
- "Is Ja'Marr Chase worth his ADP this year?"
- "What are the injury concerns for Saquon Barkley?"
- "Who are the best value picks at TE after round 5?"

The system retrieves relevant expert analysis from a vector database and cross-references it with real stats and ADP value calculations — then synthesizes both into an answer with reasoning and source citations.

## Architecture

```
Question + Roster + Drafted Players
          ↓
┌─────────┴─────────┐
│                   │
RAG Layer       Analytics Engine
│                   │
Expert opinions,   Stats, ADP,
injury context,    value scores,
news, narratives   positional needs
│                   │
└─────────┬─────────┘
          ↓
     LLM synthesis
          ↓
  Answer + Reasoning + Sources
```

## Tech Stack

| Component | Tool |
|-----------|------|
| RAG framework | LangChain |
| Vector database | ChromaDB |
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`) |
| LLM | Groq API (`llama-3.1-70b`) |
| Player stats | nflreadpy |
| ADP data | nflreadpy / FantasyPros |
| Scoring | Half-PPR |
| Testing | pytest |
| Python version | 3.11 via pyenv |

## Setup

```bash
# Clone the repo
git clone https://github.com/mattvanharn/fantasy-draft-rag.git
cd fantasy-draft-rag

# Set Python version (requires pyenv)
pyenv local 3.11.14

# Install uv (Arch: sudo pacman -S uv), then install dependencies
uv sync

# Configure environment
cp .env.example .env
# Edit .env and add your GROQ_API_KEY (free at console.groq.com)
```

Run scripts with `uv run python scripts/fetch_stats.py` (no need to activate the venv).

## Project Status

**Phase 1: Hybrid RAG + Analytics Pipeline** — In Progress

| Step | Status | Description |
|------|--------|-------------|
| 1. Project setup | ✅ Done | Repo, uv, dependencies |
| 2. Groq LLM setup | ✅ Done | Configure LLM via API |
| 3. Stats data | ✅ Done | Collect player stats (2018-2025) via nflreadpy |
| 4. ADP data | ✅ Done | FantasyPros CSVs collected; exploring nflreadpy alternatives |
| 5. Data exploration | 🔄 In progress | Notebook: merging stats + ADP, validating data |
| 6. Document processing | ⬜ | Convert stats to text for RAG |
| 7. Vector store | ⬜ | Embeddings + ChromaDB |
| 8. Analytics engine | ⬜ | Value scores, roster logic |
| 9. End-to-end pipeline | ⬜ | Connect all components |
| 10. Evaluation & polish | ⬜ | Testing, tuning, docs |

## License

MIT
