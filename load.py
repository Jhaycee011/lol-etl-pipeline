import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    """Create and return a database connection."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def create_tables(conn):
    """Create matches and participants tables if they don't exist yet."""
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS matches (
                match_id     TEXT PRIMARY KEY,
                game_mode    TEXT,
                queue_id     INTEGER,
                game_version TEXT,
                duration_sec INTEGER
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS participants (
                id                SERIAL PRIMARY KEY,
                match_id          TEXT REFERENCES matches(match_id),
                puuid             TEXT,
                player_name       TEXT,
                player_tag        TEXT,
                champion          TEXT,
                position          TEXT,
                kills             INTEGER,
                deaths            INTEGER,
                assists           INTEGER,
                win               BOOLEAN,
                damage_dealt      INTEGER,
                gold_earned       INTEGER,
                cs                INTEGER,
                vision_score      INTEGER,
                is_tracked_player BOOLEAN
            );
        """)

        conn.commit()
        print("Tables created (or already exist).")

def load_matches(conn, matches_df):
    """Insert match rows, skip duplicates."""
    with conn.cursor() as cur:
        for _, row in matches_df.iterrows():
            cur.execute("""
                INSERT INTO matches (match_id, game_mode, queue_id, game_version, duration_sec)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (match_id) DO NOTHING;
            """, (
                row["match_id"],
                row["game_mode"],
                row["queue_id"],
                row["game_version"],
                row["duration_sec"]
            ))
        conn.commit()
        print(f"Loaded {len(matches_df)} matches.")

def load_participants(conn, participants_df):
    """Insert participant rows, skip duplicates."""
    with conn.cursor() as cur:
        for _, row in participants_df.iterrows():
            cur.execute("""
                INSERT INTO participants 
                    (match_id, puuid, player_name, player_tag, champion, position,
                     kills, deaths, assists, win, damage_dealt, gold_earned,
                     cs, vision_score, is_tracked_player)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING;
            """, (
                row["match_id"], row["puuid"], row["player_name"], row["player_tag"],
                row["champion"], row["position"], row["kills"], row["deaths"],
                row["assists"], row["win"], row["damage_dealt"], row["gold_earned"],
                row["cs"], row["vision_score"], row["is_tracked_player"]
            ))
        conn.commit()
        print(f"Loaded {len(participants_df)} participant records.")

def load(matches_df, participants_df):
    """Run the full load step."""
    conn = get_connection()
    create_tables(conn)
    load_matches(conn, matches_df)
    load_participants(conn, participants_df)
    conn.close()
    print("Load complete. Connection closed.")