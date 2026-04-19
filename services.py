from typing import Dict, Any

def calculate_scoreboard(data: Dict[str, Any]) -> dict:
    # 'data' is a dictionary because we called .dict() in main.py
    # However, 'ball_events' inside it is a list of Pydantic models
    events = data["ball_events"]
    
    score = sum(e.runs_off_bat + e.extras for e in events)
    legal_count = sum(1 for e in events if e.is_legal_delivery)
    overs_str = f"{legal_count // 6}.{legal_count % 6}"
    
    total_overs_decimal = (legal_count // 6) + ((legal_count % 6) / 6)
    run_rate = round(score / total_overs_decimal, 2) if total_overs_decimal > 0 else 0.0

    batters = {}
    bowlers = {}
    for e in events:
        # e is a Pydantic model object, use dot notation
        batters[e.striker] = batters.get(e.striker, 0) + e.runs_off_bat
        
        b = e.bowler
        bowlers.setdefault(b, {"wickets": 0, "runs": 0})
        bowlers[b]["runs"] += (e.runs_off_bat + (e.extras if e.extra_type in ["wide", "no_ball"] else 0))
        if e.wicket_fell and e.wicket_type not in ["run_out", "retired_out"]:
            bowlers[b]["wickets"] += 1

    top_batter_name = max(batters, key=batters.get) if batters else None
    top_bowler_name = max(bowlers, key=lambda x: bowlers[x]["wickets"]) if bowlers else None

    recent = ["W" if e.wicket_fell else str(e.runs_off_bat) for e in events if e.is_legal_delivery][-6:]

    return {
        "match": data["match_title"],
        "venue": data["venue"],
        "innings_number": data["innings_number"],
        "batting_team": data["batting_team"],
        "bowling_team": data["bowling_team"],
        "score": score,
        "wickets": sum(1 for e in events if e.wicket_fell and e.wicket_type != "run_out"),
        "overs": overs_str,
        "run_rate": run_rate,
        "top_batter": {"name": top_batter_name, "runs": batters[top_batter_name]} if top_batter_name else None,
        "top_bowler": {"name": top_bowler_name, **bowlers[top_bowler_name]} if top_bowler_name else None,
        "recent_balls": recent
    }
