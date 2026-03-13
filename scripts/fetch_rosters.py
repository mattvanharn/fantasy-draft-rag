# Download roster info (team, position, age, experience,  etc.)
import nflreadpy as nfl
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
SEASONS = list(range(2018, 2026))

# Fetch the data
rosters = nfl.load_rosters(SEASONS)
# Save the data
rosters.write_csv(DATA_DIR / "rosters_2018_2025.csv", separator="\t")
