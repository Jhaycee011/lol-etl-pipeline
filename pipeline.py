from extract import extract
from transform import transform
from load import load

def run_pipeline(game_name, tag_line, count=10):
    """
    Runs the full ETL pipeline for a given player.
    E → T → L
    """
    print("=" * 40)
    print(f"Starting pipeline for {game_name}#{tag_line}")
    print("=" * 40)

    # --- EXTRACT ---
    print("\n[1/3] Extracting...")
    matches, puuid = extract(game_name, tag_line, count)

    # --- TRANSFORM ---
    print("\n[2/3] Transforming...")
    matches_df, participants_df = transform(matches, puuid)

    # --- LOAD ---
    print("\n[3/3] Loading...")
    load(matches_df, participants_df)

    print("\n" + "=" * 40)
    print("Pipeline complete!")
    print("=" * 40)

if __name__ == "__main__":
    run_pipeline("HackDawgs", "10Der", count=40)