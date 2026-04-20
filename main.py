from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import ScoreboardInput, MatchScoreboardResponse, ErrorResponse
from services import calculate_scoreboard

app = FastAPI(title="Khel AI Match Scoreboard API")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.get("/")
def home():
    return {"message": "Match Scoreboard API is live", "docs": "/docs", "health": "/health"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post(
    "/api/match/scoreboard/",
    response_model=MatchScoreboardResponse,
    responses={422: {"model": ErrorResponse}, 500: {"model": ErrorResponse}}
)
def compute_scoreboard(input_data: ScoreboardInput):
    try:
        return calculate_scoreboard(input_data.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")
