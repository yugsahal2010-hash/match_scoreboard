from typing import Optional

# Only the fields we actually need — mirrors real Django model field names
DEMO_MATCH_DATA = {
    "match_id": 1,
    "title": "Team A vs Team B",
    "venue": "M. Chinnaswamy Stadium, Bengaluru",
    "innings_number": 1,
    "batting_team": "Team A",
    "bowling_team": "Team B",
}

DEMO_BALL_EVENTS = [
    # over 1
    {"over_number": 1, "ball_number": 1, "striker": "Rohit Sharma",  "bowler": "Jasprit Bumrah", "runs_off_bat": 4,  "extras": 0, "extra_type": "", "is_legal_delivery": True,  "wicket_fell": False, "wicket_type": ""},
    {"over_number": 1, "ball_number": 2, "striker": "Rohit Sharma",  "bowler": "Jasprit Bumrah", "runs_off_bat": 0,  "extras": 0, "extra_type": "", "is_legal_delivery": True,  "wicket_fell": False, "wicket_type": ""},
    {"over_number": 1, "ball_number": 3, "striker": "Virat Kohli",   "bowler": "Jasprit Bumrah", "runs_off_bat": 6,  "extras": 0, "extra_type": "", "is_legal_delivery": True,  "wicket_fell": False, "wicket_type": ""},
    {"over_number": 1, "ball_number": 4, "striker": "Virat Kohli",   "bowler": "Jasprit Bumrah", "runs_off_bat": 0,  "extras": 1, "extra_type": "wide", "is_legal_delivery": False, "wicket_fell": False, "wicket_type": ""},
    {"over_number": 1, "ball_number": 4, "striker": "Virat Kohli",   "bowler": "Jasprit Bumrah", "runs_off_bat": 1,  "extras": 0, "extra_type": "", "is_legal_delivery": True,  "wicket_fell": False, "wicket_type": ""},
    {"over_number": 1, "ball_number": 5, "striker": "Rohit Sharma",  "bowler": "Jasprit Bumrah", "runs_off_bat": 0,  "extras": 0, "extra_type": "", "is_legal_delivery": True,  "wicket_fell": True,  "wicket_type": "bowled"},
    {"over_number": 1, "ball_number": 6, "striker": "KL Rahul",      "bowler": "Jasprit Bumrah", "runs_off_bat": 2,  "extras": 0, "extra_type": "", "is_legal_delivery": True,  "wicket_fell": False, "wicket_type": ""},
    # over 2
    {"over_number": 2, "ball_number": 1, "striker": "Virat Kohli",   "bowler": "Mohammed Shami", "runs_off_bat": 0,  "extras": 0, "extra_type": "", "is_legal_delivery": True,  "wicket_fell": False, "wicket_type": ""},
    {"over_number": 2, "ball_number": 2, "striker": "KL Rahul",      "bowler": "Mohammed Shami", "runs_off_bat": 6,  "extras": 0, "extra_type": "", "is_legal_delivery": True,  "wicket_fell": False, "wicket_type": ""},
    {"over_number": 2, "ball_number": 3, "striker": "Virat Kohli",   "bowler": "Mohammed Shami", "runs_off_bat": 0,  "extras": 0, "extra_type": "", "is_legal_delivery": True,  "wicket_fell": True,  "wicket_type": "caught"},
    {"over_number": 2, "ball_number": 4, "striker": "KL Rahul",      "bowler": "Mohammed Shami", "runs_off_bat": 1,  "extras": 0, "extra_type": "", "is_legal_delivery": True,  "wicket_fell": False, "wicket_type": ""},
    {"over_number": 2, "ball_number": 5, "striker": "KL Rahul",      "bowler": "Mohammed Shami", "runs_off_bat": 0,  "extras": 1, "extra_type": "no_ball", "is_legal_delivery": False, "wicket_fell": False, "wicket_type": ""},
    {"over_number": 2, "ball_number": 5, "striker": "KL Rahul",      "bowler": "Mohammed Shami", "runs_off_bat": 0,  "extras": 0, "extra_type": "", "is_legal_delivery": True,  "wicket_fell": False, "wicket_type": ""},
    {"over_number": 2, "ball_number": 6, "striker": "KL Rahul",      "bowler": "Mohammed Shami", "runs_off_bat": 4,  "extras": 0, "extra_type": "", "is_legal_delivery": True,  "wicket_fell": False, "wicket_type": ""},
]


# --- calculation functions ---

def calculate_score(events) -> int:
    return sum(e["runs_off_bat"] + e["extras"] for e in events)


def calculate_wickets(events) -> int:
    return sum(
        1 for e in events
        if e["wicket_fell"] and e["wicket_type"] not in {"run_out", "retired_out"}
    )


def calculate_overs(events) -> str:
    legal = sum(1 for e in events if e["is_legal_delivery"])
    return f"{legal // 6}.{legal % 6}"


def calculate_run_rate(score: int, overs_str: str) -> float:
    overs, balls = map(int, overs_str.split("."))
    total = overs + balls / 6
    return round(score / total, 2) if total > 0 else 0.0


def get_top_batter(events) -> dict:
    tally = {}
    for e in events:
        tally[e["striker"]] = tally.get(e["striker"], 0) + e["runs_off_bat"]
    top = max(tally, key=tally.get)
    return {"name": top, "runs": tally[top]}


def get_top_bowler(events) -> dict:
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
    legal = [e for e in events if e["is_legal_delivery"]]
    labels = []
    for e in legal[-n:]:
        if e["wicket_fell"]:
            labels.append("W")
        elif e["runs_off_bat"] in {4, 6}:
            labels.append(str(e["runs_off_bat"]))
        else:
            labels.append(str(e["runs_off_bat"]))
    return labels


# --- main summary ---

def match_scoreboard_summary(match_id: int) -> Optional[dict]:
    if match_id != DEMO_MATCH_DATA["match_id"]:
        return None

    # edge case: innings not started yet
    if not DEMO_BALL_EVENTS:
        return {**DEMO_MATCH_DATA, "score": 0, "wickets": 0, "overs": "0.0",
                "run_rate": 0.0, "top_batter": None, "top_bowler": None, "recent_balls": []}

    score    = calculate_score(DEMO_BALL_EVENTS)
    wickets  = calculate_wickets(DEMO_BALL_EVENTS)
    overs    = calculate_overs(DEMO_BALL_EVENTS)

    return {
        "match":          DEMO_MATCH_DATA["title"],
        "venue":          DEMO_MATCH_DATA["venue"],
        "innings_number": DEMO_MATCH_DATA["innings_number"],
        "batting_team":   DEMO_MATCH_DATA["batting_team"],
        "bowling_team":   DEMO_MATCH_DATA["bowling_team"],
        "score":          score,
        "wickets":        wickets,
        "overs":          overs,
        "run_rate":       calculate_run_rate(score, overs),
        "top_batter":     get_top_batter(DEMO_BALL_EVENTS),
        "top_bowler":     get_top_bowler(DEMO_BALL_EVENTS),
        "recent_balls":   get_recent_balls(DEMO_BALL_EVENTS),
    }