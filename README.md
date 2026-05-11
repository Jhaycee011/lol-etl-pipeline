## League of Legends ETL Pipeline

A data engineering project that extracts match data from the Riot Games API,
transforms it into structured tables, and loads it into a PostgreSQL database.

Built to demonstrate core data engineering skills: API ingestion, data modeling,
ETL pipeline design, and relational database management.

-------------------------------------------------------------

## Architecture
Riot Games API → extract.py → transform.py → load.py → PostgreSQL
↑              ↑             ↑
API calls      pandas       psycopg2

-------------------------------------------------------------

## Tech Stack
| Layer | Tool |
|---|---|
| Language | Python 3.10+ |
| API | Riot Games Match V5 API |
| Transformation | pandas |
| Database | PostgreSQL |
| DB Driver | psycopg2 |
| Credentials | python-dotenv |

-------------------------------------------------------------

## Project Structure

lol-etl-pipeline/
├── extract.py       # Pulls match data from Riot Games API
├── transform.py     # Cleans and models raw JSON into DataFrames
├── load.py          # Loads structured data into PostgreSQL
├── pipeline.py      # Orchestrates the full ETL run
├── .env             # Credentials (not committed to GitHub)
├── .gitignore       # Excludes .env and venv
└── requirements.txt # Python dependencies

-------------------------------------------------------------

## Extract
- Accepts a Riot ID (game name + tagline) as input
- Fetches the player's `puuid` from the Riot Account API (`asia` routing)
- Retrieves recent match IDs (`sea` routing for PH/SEA server)
- Fetches full match details for each match ID

## Transform
- Parses deeply nested JSON responses
- Produces two normalized DataFrames:
  - `matches` — game-level info (mode, duration, patch, queue type)
  - `participants` — player-level stats (champion, KDA, CS, gold, vision score)
- Flags the tracked player's rows with `is_tracked_player = TRUE`

## Load
- Connects to a local PostgreSQL instance
- Creates tables if they don't exist (`IF NOT EXISTS`)
- Inserts records with `ON CONFLICT DO NOTHING` for idempotent runs

-------------------------------------------------------------

## `matches`
| Column | Type | Description |
|---|---|---|
| match_id | TEXT (PK) | Unique match identifier |
| game_mode | TEXT | CLASSIC, ARAM, etc. |
| queue_id | INTEGER | 420 = ranked solo, 440 = ranked flex |
| game_version | TEXT | Patch number |
| duration_sec | INTEGER | Game length in seconds |

## `participants`
| Column | Type | Description |
|---|---|---|
| id | SERIAL (PK) | Auto-increment ID |
| match_id | TEXT (FK) | References matches table |
| puuid | TEXT | Riot's unique player ID |
| player_name | TEXT | Riot ID game name |
| player_tag | TEXT | Riot ID tagline |
| champion | TEXT | Champion played |
| position | TEXT | TOP, JUNGLE, MIDDLE, BOTTOM, UTILITY |
| kills | INTEGER | |
| deaths | INTEGER | |
| assists | INTEGER | |
| win | BOOLEAN | |
| damage_dealt | INTEGER | Total damage to champions |
| gold_earned | INTEGER | |
| cs | INTEGER | Total minions killed |
| vision_score | INTEGER | |
| is_tracked_player | BOOLEAN | TRUE if this is the tracked account |

-------------------------------------------------------------

##  Setup & Usage

## 1. Clone the repo
```bash
git clone *Insert GIT link
cd lol-etl-pipeline
```

## 2. Create and activate virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

## 3. Install dependencies
```bash
pip install -r requirements.txt
```

## 4. Set up environment variables
Create a `.env` file in the project root:
RIOT_API_KEY=your-riot-api-key
DB_HOST=localhost
DB_PORT=5432
DB_NAME=lol_pipeline
DB_USER=postgres
DB_PASSWORD=your-password

> Get a free Riot API key at [developer.riotgames.com](https://developer.riotgames.com)

### 5. Create the database
```sql
CREATE DATABASE lol_pipeline;
```

### 6. Run the pipeline
```bash
python pipeline.py
```

-------------------------------------------------------------
## Sample Query — Player Performance Summary

```sql
SELECT 
    champion,
    position,
    COUNT(*) as games,
    SUM(CASE WHEN win THEN 1 ELSE 0 END) as wins,
    ROUND(AVG(kills), 1) as avg_kills,
    ROUND(AVG(deaths), 1) as avg_deaths,
    ROUND(AVG(assists), 1) as avg_assists,
    ROUND(AVG(cs), 1) as avg_cs
FROM participants
WHERE is_tracked_player = TRUE
GROUP BY champion, position
ORDER BY games DESC;
```
-------------------------------------------------------------

##  Notes

- Riot development API keys expire every 24 hours — refresh at the developer portal before running
- PH server accounts use `asia` routing for account lookup and `sea` routing for match data
- Re-running the pipeline is safe — duplicate records are automatically skipped
- Supports up to 100 matches per run (Riot API limit per request)

-------------------------------------------------------------
##  Future Improvements

- [ ] Add Apache Airflow for automated scheduling
- [ ] Migrate storage to Google BigQuery
- [ ] Add dbt for data modeling layer
- [ ] Build a Looker Studio dashboard on top of the data
- [ ] Apply for a Riot production API key for non-expiring access
-------------------------------------------------------------
## 👤 Author

**Jhaycee** — CS Graduate | Data Engineering Enthusiast  
[GitHub](https://github.com/yourusername) · [LinkedIn](https://www.linkedin.com/in/jose-christopher-ojano-525763233/)
