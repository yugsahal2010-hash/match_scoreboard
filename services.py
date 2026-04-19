from typing import Dict, Any

def calculate_scoreboard(data: Dict[str, Any]) -> dict:
    events = data["ball_events"]
    
    # Core calculations
    score = sum(e.runs_off_bat + e.extras for e in events)
    legal_count = sum(1 for e in events if e.is_legal_delivery)
    overs_str = f"{legal_count // 6}.{legal_count % 6}"
    
    total_overs_decimal = (legal_count // 6) + ((legal_count % 6) / 6)
    run_rate = round(score / total_overs_decimal, 2) if total_overs_decimal > 0 else 0.0

    # Aggregations
    batters = {}
    bowlers = {}
    for e in events:
        batters[e.striker] = batters.get(e.striker, 0) + e.runs_off_bat
        b = e.bowler
        bowlers.setdefault(b, {"wickets": 0, "runs": 0})
        bowlers[b]["runs"] += (e.runs_off_bat + (e.extras if e.extra_type in ["wide", "no_ball"] else 0))
        if e.wicket_fell and e.wicket_type not in ["run_out", "retired_out"]:
            bowlers[b]["wickets"] += 1

    top_batter = max(batters, key=batters.get) if batters else None
    top_bowler = max(bowlers, key=lambda x: bowlers[x]["wickets"]) if bowlers else None

    # Format recent delivery labels
    legal = [e for e in events if e.is_legal_delivery]
    recent = ["W" if e.wicket_fell else str(e.runs_off_bat) for e in legal[-6:]]

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
        "top_batter": {"name": top_batter, "runs": batters[top_batter]} if top_batter else None,
        "top_bowler": {"name": top_bowler, **bowlers[top_bowler]} if top_bowler else None,
        "recent_balls": recent
    }
