from typing import Optional, List

# --- V1 "Silo" Mock Data ---
# This data simulates a live database for today's assignment.

DEMO_MATCH_DATA = {
    "match_id": 1,
    "title": "India vs Pakistan",
    "venue": "Pallekele International Cricket Stadium",
    "innings_number": 1,
    "batting_team": "India",
    "bowling_team": "Pakistan"
}

DEMO_BALL_EVENTS = [
    {"striker": "Virat Kohli", "bowler": "Shaheen Afridi", "runs_off_bat": 0, "extras": 1, "extra_type": "wide", "is_legal_delivery": False, "wicket_fell": False, "wicket_type": ""},
    {"striker": "Virat Kohli", "bowler": "Shaheen Afridi", "runs_off_bat": 4, "extras": 0, "extra_type": "", "is_legal_delivery": True, "wicket_fell": False, "wicket_type": ""},
    {"striker": "Virat Kohli", "bowler": "Shaheen Afridi", "runs_off_bat": 0, "extras": 0, "extra_type": "", "is_legal_delivery": True, "wicket_fell": True, "wicket_type": "bowled"},
    {"striker": "Rohit Sharma", "bowler": "Shaheen Afridi", "runs_off_bat": 1, "extras": 0, "extra_type": "", "is_legal_delivery": True, "wicket_fell": False, "wicket_type": ""},
    {"striker": "Rohit Sharma", "bowler": "Naseem Shah", "runs_off_bat": 6, "extras": 0, "extra_type": "", "is_legal_delivery": True, "wicket_fell": False, "wicket_type": ""},
    {"striker": "Rohit Sharma", "bowler": "Naseem Shah", "runs_off_bat": 0, "extras": 0, "extra_type": "", "is_legal_delivery": True, "wicket_fell": False, "wicket_type": ""},
]

# --- Helper Functions ---

def calculate_score(events) -> int:
    return sum(e["runs_off_bat"] + e["extras"] for e in events)

def calculate_wickets(events) -> int:
    # Filter for bowler-earned wickets (excludes run outs as per standard scoreboard logic)
    return sum(1 for e in events if e["wicket_fell"] and e["wicket_type"] not in {"run_out", "retired_out"})

def calculate_overs(events) -> str:
    legal = sum(1 for e in events if e["is_legal_delivery"])
    return f"{legal // 6}.{legal % 6}"

def calculate_run_rate(score: int, overs_str: str) -> float:
    overs, balls = map(int, overs_str.split("."))
    total_overs_decimal = overs + (balls / 6)
    return round(score / total_overs_decimal, 2) if total_overs_decimal > 0 else 0.0

def get_top_batter(events) -> dict:
    if not events: return None
    tally = {}
    for e in events:
        tally[e["striker"]] = tally.get(e["striker"], 0) + e["runs_off_bat"]
    top = max(tally, key=tally.get)
    return {"name": top, "runs": tally[top]}

def get_top_bowler(events) -> dict:
    if not events: return None
    wickets, runs = {}, {}
    for e in events:
        b = e["bowler"]
        wickets.setdefault(b, 0)
        runs.setdefault(b, 0)
        runs[b] += e["runs_off_bat"]
        if e["extra_type"] in {"wide", "no_ball"}:
            runs[b] += e["extras"]
        if e["wicket_fell"] and e["wicket_type"] not in {"run_out", "retired_out"}:
            wickets[b] += 1
    top = max(wickets, key=wickets.get)
    return {"name": top, "wickets": wickets[top], "runs": runs[top]}

def get_recent_balls(events, n: int = 6) -> list:
    # Captures last N legal deliveries
    legal = [e for e in events if e["is_legal_delivery"]]
    labels = []
    for e in legal[-n:]:
        if e["wicket_fell"]:
            labels.append("W")
        else:
            # Shows runs off bat for standard legal balls
            labels.append(str(e["runs_off_bat"]))
    return labels

# --- Main Summary Function ---

def match_scoreboard_summary(match_id: int) -> Optional[dict]:
    # Security check for demo purposes
    if match_id != DEMO_MATCH_DATA["match_id"]:
        return None

    # Handle case where match exists but no ball events have been recorded yet
    if not DEMO_BALL_EVENTS:
        return {
            **DEMO_MATCH_DATA, 
            "score": 0, "wickets": 0, "overs": "0.0",
            "run_rate": 0.0, "top_batter": None, 
            "top_bowler": None, "recent_balls": []
        }

    # Execute calculations
    score = calculate_score(DEMO_BALL_EVENTS)
    overs = calculate_overs(DEMO_BALL_EVENTS)

    return {
        "match":          DEMO_MATCH_DATA["title"],
        "venue":          DEMO_MATCH_DATA["venue"],
        "innings_number": DEMO_MATCH_DATA["innings_number"],
        "batting_team":   DEMO_MATCH_DATA["batting_team"],
        "bowling_team":   DEMO_MATCH_DATA["bowling_team"],
        "score":          score,
        "wickets":        calculate_wickets(DEMO_BALL_EVENTS),
        "overs":          overs,
        "run_rate":       calculate_run_rate(score, overs),
        "top_batter":     get_top_batter(DEMO_BALL_EVENTS),
        "top_bowler":     get_top_bowler(DEMO_BALL_EVENTS),
        "recent_balls":   get_recent_balls(DEMO_BALL_EVENTS),
    }