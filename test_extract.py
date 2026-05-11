from extract import extract
import os
import json
from dotenv import load_dotenv
from transform import transform
from load import load

load_dotenv()

api_key = os.getenv("RIOT_API_KEY")


matches, puuid = extract("HackDawgs", "10Der")

print(f"\nYour PUUID: {puuid}")
print(f"Total matches retrieved: {len(matches)}")

if matches:
    print(f"First match ID: {matches[0]['metadata']['matchId']}")
else:
    print("No matches found — try changing the 'type' filter in get_match_ids()")

print(json.dumps(matches[0], indent=2))
matches_df, participants_df = transform(matches, puuid)

print("\n--- Matches Table ---")
print(matches_df.head())

print("\n--- Participants Table (tracked player only) ---")
print(participants_df[participants_df["is_tracked_player"] == True])


load(matches_df, participants_df)