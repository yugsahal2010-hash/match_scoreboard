from pydantic import BaseModel, Field
from typing import List, Optional


class TopBatter(BaseModel):
    name: str
    runs: int


class TopBowler(BaseModel):
    name: str
    wickets: int
    runs: int


class ScoreboardInput(BaseModel):
    match: str
    venue: str
    innings_number: int
    batting_team: str
    bowling_team: str
    score: int
    wickets: int
    overs: str
    top_batter: Optional[TopBatter] = None
    top_bowler: Optional[TopBowler] = None
    recent_balls: List[str]


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
