# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

NickOccupancy scrapes the live occupancy percentage of the Nicholas Recreation Center (UW-Madison) from `https://services.recwell.wisc.edu/FacilityOccupancy`, stores readings in a local SQLite database, and provides scripts to inspect and visualize the data.

The scraper (`nick.py`) is designed to run on a Raspberry Pi via cron job, logging output to `cron.log`.

## Dependencies

- `requests` — HTTP scraping
- `beautifulsoup4` — HTML parsing
- `numpy`, `matplotlib` — used in the Jupyter notebook for visualization
- `sqlite3` — stdlib, no install needed

Install: `pip install requests beautifulsoup4 numpy matplotlib`

## Common Commands

```bash
# One-time DB setup
python createTable.py

# Run a single occupancy scrape manually
python nick.py

# Drop the OCCUPANCY table (destructive)
python dropTable.py

# Visualize data
python main.py                      # most recent day with data
python main.py --date 2021-03-26    # specific date
python main.py --heatmap            # avg occupancy by weekday + hour
python main.py --all                # all recorded data
```

## Architecture

Data flows in one direction: `nick.py` (cron) → `data.db` (SQLite) → `main.py` (visualization).

**`data.db` schema — `OCCUPANCY` table:**
| Column | Type | Notes |
|---|---|---|
| ID | INTEGER | Auto-incremented primary key |
| DATETIME | TEXT | Python `datetime.datetime.now()` string |
| OCCUPANCY | INT | Percentage value (0–100) |

**Important:** `nick.py` has a hardcoded absolute path to the DB (`/home/pi/Python/NickOccupancy/data.db`) for Raspberry Pi deployment. `main.py` and the DB management scripts use the relative path `data.db`. When running locally, update the path in `nick.py` or run it from the project directory.

**Scraping logic in `nick.py`:** Finds all `<strong>` tags, takes the first one whose text parses as an integer ≤ 100 (stripping `%`), and treats that as the current occupancy.
