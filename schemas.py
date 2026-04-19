from pydantic import BaseModel, Field
from typing import List, Optional

class BallEvent(BaseModel):
    striker: str
    bowler: str
    runs_off_bat: int
    extras: int
    extra_type: Optional[str] = ""
    is_legal_delivery: bool
    wicket_fell: bool
    wicket_type: Optional[str] = ""

class ScoreboardInput(BaseModel):
    match_title: str
    venue: str
    innings_number: int
    batting_team: str
    bowling_team: str
    ball_events: List[BallEvent]

class TopBatter(BaseModel):
    name: str
    runs: int

class TopBowler(BaseModel):
    name: str
    wickets: int
    runs: int

class MatchScoreboardResponse(BaseModel):
    match: str
    venue: str
    innings_number: int
    batting_team: str
    bowling_team: str
    score: int
    wickets: int
    overs: str
    run_rate: float
    top_batter: Optional[TopBatter]
    top_bowler: Optional[TopBowler]
    recent_balls: List[str]

class ErrorResponse(BaseModel):
    detail: str
