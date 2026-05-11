import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RIOT_API_KEY")

HEADERS = {
    "X-Riot-Token": API_KEY
}

def get_puuid(game_name, tag_line, region="asia"):
    """Convert Riot ID to puuid."""
    url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()["puuid"]

def get_match_ids(puuid, region="sea", count=10):
    """Get list of recent match IDs."""
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    params = {
        "count": count
    }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()

def get_match_detail(match_id, region="sea"):
    """Get full stats for a single match."""
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def extract(game_name, tag_line, count=10):
    """Run the full extract — returns a list of raw match detail dicts."""
    print(f"Fetching puuid for {game_name}#{tag_line}...")
    puuid = get_puuid(game_name, tag_line)

    print(f"Fetching {count} recent match IDs...")
    match_ids = get_match_ids(puuid, count=count)

    matches = []
    for match_id in match_ids:
        print(f"  Fetching match {match_id}...")
        detail = get_match_detail(match_id)
        matches.append(detail)

    print(f"Extract complete. {len(matches)} matches retrieved.")
    return matches, puuid