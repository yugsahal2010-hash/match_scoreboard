# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from schemas import MatchScoreboardResponse, ErrorResponse
from services import match_scoreboard_summary

app = FastAPI(
    title="Khel AI Match Scoreboard API",
    version="1.0.0",
    description="Demo API that returns a live scoreboard for a match."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Match Scoreboard API is live",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get(
    "/api/match/{match_id}/scoreboard/",
    response_model=MatchScoreboardResponse,
    responses={404: {"model": ErrorResponse}},
)
def get_match_scoreboard(match_id: int):
    result = match_scoreboard_summary(match_id=match_id)

    if result is None:
        raise HTTPException(status_code=404, detail="No demo data found for this match")

    return result