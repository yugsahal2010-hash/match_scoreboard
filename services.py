from typing import Dict, Any


def _parse_overs_to_decimal(overs_str: str) -> float:
    """Convert overs string like '12.3' to decimal (12.5) for run rate calc."""
    try:
        parts = overs_str.split(".")
        full_overs = int(parts[0])
        balls = int(parts[1]) if len(parts) > 1 else 0
        return full_overs + (balls / 6)
    except (ValueError, IndexError):
        return 0.0


def calculate_scoreboard(data: Dict[str, Any]) -> dict:
    # Handle the case where no innings has been created yet
    if not data.get("innings_started"):
        return {
            "match": data["match"],
            "venue": data["venue"],
            "innings_number": None,
            "batting_team": None,
            "bowling_team": None,
            "score": None,
            "wickets": None,
            "overs": None,
            "run_rate": None,
            "top_batter": None,
            "top_bowler": None,
            "recent_balls": [],
            "status": "Innings not yet started"
        }

    overs_decimal = _parse_overs_to_decimal(data["overs"])
    run_rate = round(data["score"] / overs_decimal, 2) if overs_decimal > 0 else 0.0

    return {
        "match": data["match"],
        "venue": data["venue"],
        "innings_number": data["innings_number"],
        "batting_team": data["batting_team"],
        "bowling_team": data["bowling_team"],
        "score": data["score"],
        "wickets": data["wickets"],
        "overs": data["overs"],
        "run_rate": run_rate,
        "top_batter": data.get("top_batter"),
        "top_bowler": data.get("top_bowler"),
        "recent_balls": data["recent_balls"],
        "status": "Live"
    }
