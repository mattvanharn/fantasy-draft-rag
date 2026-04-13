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
LEAGUE_SIZE = 12  # used for VOR calculations in Milestone 2
POSITIONS = ["QB", "RB", "WR", "TE", "K", "DST"]

# ---------------------------------------------------------------------------
# Scoring settings
#
# SCORING_PRESETS contains platform-specific point values with no reception
# weight — format (standard / half-PPR / PPR) is applied separately via the
# "receptions" key so each platform only needs one base dict.
#
# Stat column names map directly to nflreadpy weekly columns.
# DST (tiered points-allowed) is not representable as a flat weight dict;
# deferred until team-level data is added.
# ---------------------------------------------------------------------------
SCORING_PRESETS: dict[str, dict[str, float]] = {
    "espn": {
        # Passing — INT: -2
        "passing_yards": 0.04,
        "passing_tds": 4.0,
        "passing_interceptions": -2.0,
        "passing_2pt_conversions": 2.0,
        # Rushing
        "rushing_yards": 0.1,
        "rushing_tds": 6.0,
        "rushing_2pt_conversions": 2.0,
        "rushing_fumbles_lost": -2.0,
        # Receiving (no receptions key — set per format below)
        "receiving_yards": 0.1,
        "receiving_tds": 6.0,
        "receiving_2pt_conversions": 2.0,
        "receiving_fumbles_lost": -2.0,
        # Misc fumbles (on sacks)
        "sack_fumbles_lost": -2.0,
        # Kicking — ESPN awards 6pts for 60+ and penalizes missed FGs
        "fg_made_0_19": 3.0,
        "fg_made_20_29": 3.0,
        "fg_made_30_39": 3.0,
        "fg_made_40_49": 4.0,
        "fg_made_50_59": 5.0,
        "fg_made_60_": 6.0,
        "pat_made": 1.0,
        "fg_missed": -1.0,
    },
    "yahoo": {
        # Passing — INT: -1 (Yahoo is less punishing than ESPN/Sleeper)
        "passing_yards": 0.04,
        "passing_tds": 4.0,
        "passing_interceptions": -1.0,
        "passing_2pt_conversions": 2.0,
        # Rushing
        "rushing_yards": 0.1,
        "rushing_tds": 6.0,
        "rushing_2pt_conversions": 2.0,
        "rushing_fumbles_lost": -2.0,
        # Receiving (no receptions key — set per format below)
        "receiving_yards": 0.1,
        "receiving_tds": 6.0,
        "receiving_2pt_conversions": 2.0,
        "receiving_fumbles_lost": -2.0,
        # Misc fumbles (on sacks)
        "sack_fumbles_lost": -2.0,
        # Kicking — no FG missed penalty, no separate 60+ tier
        "fg_made_0_19": 3.0,
        "fg_made_20_29": 3.0,
        "fg_made_30_39": 3.0,
        "fg_made_40_49": 4.0,
        "fg_made_50_59": 5.0,
        "fg_made_60_": 5.0,
        "pat_made": 1.0,
    },
    "sleeper": {
        # Passing — INT: -2
        "passing_yards": 0.04,
        "passing_tds": 4.0,
        "passing_interceptions": -2.0,
        "passing_2pt_conversions": 2.0,
        # Rushing
        "rushing_yards": 0.1,
        "rushing_tds": 6.0,
        "rushing_2pt_conversions": 2.0,
        "rushing_fumbles_lost": -2.0,
        # Receiving (no receptions key — set per format below)
        "receiving_yards": 0.1,
        "receiving_tds": 6.0,
        "receiving_2pt_conversions": 2.0,
        "receiving_fumbles_lost": -2.0,
        # Misc fumbles (on sacks)
        "sack_fumbles_lost": -2.0,
        # Kicking — no FG missed penalty, no separate 60+ tier
        "fg_made_0_19": 3.0,
        "fg_made_20_29": 3.0,
        "fg_made_30_39": 3.0,
        "fg_made_40_49": 4.0,
        "fg_made_50_59": 5.0,
        "fg_made_60_": 5.0,
        "pat_made": 1.0,
    },
}

# All 9 scoring settings (3 platforms × 3 formats), keyed by "{platform}_{format}".
# Column names in fetch_stats.py are "fantasy_points_{key}" (e.g. fantasy_points_espn_half_ppr).
_RECEPTION_WEIGHTS = {"standard": 0.0, "half_ppr": 0.5, "ppr": 1.0}

ALL_SCORING_SETTINGS: dict[str, dict[str, float]] = {
    f"{platform}_{fmt}": {**preset, "receptions": weight}
    for platform, preset in SCORING_PRESETS.items()
    for fmt, weight in _RECEPTION_WEIGHTS.items()
}

# LLM settings
GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_TEMPERATURE = 0.3

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
