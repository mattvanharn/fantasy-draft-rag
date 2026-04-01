"""Central configuration: paths, constants, and model hyperparameters."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Data directories
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
MODEL_DIR = PROJECT_ROOT / "models"

# Data files
COMBINED_PARQUET = PROCESSED_DATA_DIR / "combined_stats_adp.parquet"
ANALYSIS_PARQUET = PROCESSED_DATA_DIR / "analysis_with_value.parquet"
WEEKLY_PARQUET = PROCESSED_DATA_DIR / "weekly_stats.parquet"

# League settings
SCORING_FORMAT = "half_ppr"
LEAGUE_SIZE = 12
ROSTER_SLOTS = {
    "QB": 1,
    "RB": 2,
    "WR": 2,
    "TE": 1,
    "FLEX": 2,
    "K": 1,
    "DST": 1,
    "BENCH": 6,
}

POSITIONS = ["QB", "RB", "WR", "TE", "K", "DST"]

# LLM settings
GROQ_MODEL = "qwen/qwen3-32b"
GROQ_TEMPERATURE = 0.0
SQL_GENERATION_PROMPT = """You are an expert SQLite query writer for fantasy football analysis.
Database schema:
{schema}
Sample rows from player_seasons:
{sample_data}
Rules:
- Return ONLY SQL. No explanation. No markdown fences.
- Generate ONLY a single SELECT query.
- Use only tables/columns that exist in schema.
- Use player_display_name for player names.
- seasonal_fantasy_points is half-PPR points.
- adp is average draft position (lower means earlier draft pick).
- season is integer (e.g., 2024).
- position values are abbreviations (QB, RB, WR, TE, K, DST).
- Use ORDER BY for ranking questions (best/top/worst).
- Unless user asks otherwise, include LIMIT 20.
- If comparing players/seasons, include relevant identifying columns.
Question: {question}
SQL:"""

# ML model hyperparameters
TRAIN_SEASONS = list(range(2018, 2024))  # 2018-2023
VAL_SEASON = 2024
TEST_SEASON = 2025
BATCH_SIZE = 64
LEARNING_RATE = 0.001
EPOCHS = 100
HIDDEN_DIM = 128
DROPOUT = 0.2
PATIENCE = 15


# ---------------------------------------------------------------------------
# RAG settings (deferred — not used until an unstructured corpus exists)
# Previous RAG attempt over templated player-season summaries was abandoned;
# future RAG will target unstructured text (articles, Reddit, Twitter).
# ---------------------------------------------------------------------------
CHROMA_DIR = PROJECT_ROOT / "data" / "chroma"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CHROMA_COLLECTION = "player_seasons"
EMBEDDING_DEVICE = "cpu"
INGEST_MIN_SEASONAL_POINTS = 10.0
INGEST_INCLUDE_IF_ADP_LE = float(LEAGUE_SIZE * 16)
