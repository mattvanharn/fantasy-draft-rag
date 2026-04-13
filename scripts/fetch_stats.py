# Fetch raw player stats from nflreadpy, calculate fantasy scoring, and save to CSV

import nflreadpy as nfl
import polars as pl
from pathlib import Path
from ff_ai_assistant.config import ALL_SCORING_SETTINGS

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
SEASONS = list(range(2018, 2026))

# Fetch the data
weekly_stats = nfl.load_player_stats(SEASONS, summary_level="week")

# Filter to fantasy football positions and weeks 1-17
weekly_stats = weekly_stats.filter(
    pl.col("position").is_in(["QB", "RB", "WR", "TE", "K", "DST"])
).filter(pl.col("week") <= 17)

# Calculate scoring for each setting and platform
for key, scoring in ALL_SCORING_SETTINGS.items():
    weekly_stats = weekly_stats.with_columns(
        pl.sum_horizontal(
            [pl.col(stat).fill_null(0) * weight for stat, weight in scoring.items()]
        ).alias(f"fantasy_points_{key}")
    )

# One row per player-season (no team in group_by — trades would split rows and break totals/ranks)
weekly_stats = weekly_stats.sort(["season", "player_id", "week"])

season_stats = weekly_stats.group_by(
    ["player_id", "player_display_name", "position", "season"]
).agg(
    *[
        pl.col(f"fantasy_points_{key}").sum().alias(f"seasonal_fantasy_points_{key}")
        for key in ALL_SCORING_SETTINGS
    ],
    pl.col("team").last().alias("team"),
)

# Finish ranks: 1 = most points that season. Ties share the same rank (method="min").
# overall = all positions; positional = within QB/RB/WR/TE/K/DST for that season.
season_stats = season_stats.with_columns(
    pl.col("seasonal_fantasy_points_sleeper_half_ppr")
    .rank(method="min", descending=True)
    .over("season")
    .cast(pl.Int32)
    .alias("overall_points_rank"),
    pl.col("seasonal_fantasy_points_sleeper_half_ppr")
    .rank(method="min", descending=True)
    .over(["season", "position"])
    .cast(pl.Int32)
    .alias("position_points_rank"),
)

# Save the season stats and weekly stats
season_stats.write_csv(DATA_DIR / "player_stats_2018_2025_season.csv", separator="\t")
weekly_stats.write_csv(DATA_DIR / "player_stats_2018_2025_weekly.csv", separator="\t")
