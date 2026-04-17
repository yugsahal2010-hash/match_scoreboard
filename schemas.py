# schemas.py
from typing import Optional, List
from pydantic import BaseModel, Field


class TopBatter(BaseModel):
    name: str = Field(..., description="Batter name")
    runs: int = Field(..., description="Runs scored")


class TopBowler(BaseModel):
    name: str  = Field(..., description="Bowler name")
    wickets: int = Field(..., description="Wickets taken")
    runs: int = Field(..., description="Runs conceded")


class MatchScoreboardResponse(BaseModel):
    match: str = Field(..., description="Match title")
    venue: str = Field(..., description="Venue name")
    innings_number: Optional[int] = Field(..., description="Current innings number, null if not started")
    batting_team: str = Field(..., description="Batting team name")
    bowling_team: str = Field(..., description="Bowling team name")
    score: int = Field(..., description="Total runs scored including extras")
    wickets: int = Field(..., description="Wickets fallen")
    overs: str = Field(..., description="Overs bowled e.g. 2.4")
    run_rate: float = Field(..., description="Current run rate")
    top_batter: Optional[TopBatter] = Field(..., description="Batter with most runs, null if innings not started")
    top_bowler: Optional[TopBowler] = Field(..., description="Bowler with most wickets, null if innings not started")
    recent_balls: List[str] = Field(..., description="Last 6 legal deliveries as labels e.g. 0 1 4 6 W")


class ErrorResponse(BaseModel):
    detail: str