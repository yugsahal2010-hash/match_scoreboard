from pydantic import BaseModel
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
    innings_started: bool = True        # False = match exists but no innings yet
    innings_number: Optional[int] = None
    batting_team: Optional[str] = None
    bowling_team: Optional[str] = None
    score: Optional[int] = None
    wickets: Optional[int] = None
    overs: Optional[str] = None
    top_batter: Optional[TopBatter] = None
    top_bowler: Optional[TopBowler] = None
    recent_balls: List[str] = []


class MatchScoreboardResponse(BaseModel):
    match: str
    venue: str
    innings_number: Optional[int]
    batting_team: Optional[str]
    bowling_team: Optional[str]
    score: Optional[int]
    wickets: Optional[int]
    overs: Optional[str]
    run_rate: Optional[float]
    top_batter: Optional[TopBatter]
    top_bowler: Optional[TopBowler]
    recent_balls: List[str]
    status: str


class ErrorResponse(BaseModel):
    detail: str
