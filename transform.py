import pandas as pd

def transform(matches, puuid):
    """
    Takes raw match data and returns two clean DataFrames:
    - matches_df: one row per match (game-level info)
    - participants_df: one row per player per match (player-level stats)
    """

    match_rows = []
    participant_rows = []

    for match in matches:
        # --- Pull match-level info ---
        info = match["info"]
        metadata = match["metadata"]

        match_row = {
            "match_id":     metadata["matchId"],
            "game_mode":    info["gameMode"],
            "queue_id":     info["queueId"],
            "game_version": info["gameVersion"],
            "duration_sec": info["gameDuration"],
        }
        match_rows.append(match_row)

        # --- Pull player-level info (one row per participant) ---
        for player in info["participants"]:
            participant_row = {
                "match_id":          metadata["matchId"],
                "puuid":             player["puuid"],
                "player_name":       player["riotIdGameName"],
                "player_tag":        player["riotIdTagline"],
                "champion":          player["championName"],
                "position":          player["teamPosition"],
                "kills":             player["kills"],
                "deaths":            player["deaths"],
                "assists":           player["assists"],
                "win":               player["win"],
                "damage_dealt":      player["totalDamageDealtToChampions"],
                "gold_earned":       player["goldEarned"],
                "cs":                player["totalMinionsKilled"],
                "vision_score":      player["visionScore"],
                "is_tracked_player": player["puuid"] == puuid,
            }
            participant_rows.append(participant_row)

    # Convert lists of dicts into DataFrames
    matches_df = pd.DataFrame(match_rows)
    participants_df = pd.DataFrame(participant_rows)

    print(f"Transformed {len(matches_df)} matches, {len(participants_df)} participant records.")
    return matches_df, participants_df