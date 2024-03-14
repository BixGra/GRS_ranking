from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse

from src.tools.search import *

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ranking = Ranking()


@app.post("/get-ranking-html")
async def post_method(request: Request):
    data = await request.json()
    size = data.get("size", None)
    output = ranking.get_ranking(size)
    return HTMLResponse(output)


@app.post("/get-tournaments-html")
async def post_method(request: Request):
    data = await request.json()
    size = data.get("size", None)
    output = ranking.get_tournaments(size)
    return HTMLResponse(output)


@app.post("/get-results-html")
async def post_method(request: Request):
    data = await request.json()
    tournament_id = data.get("tournament_id", -1)
    output = ranking.get_results(tournament_id)
    return HTMLResponse(output)


@app.post("/get-tournament-name-html")
async def post_method(request: Request):
    data = await request.json()
    tournament_id = data.get("tournament_id", -1)
    output = ranking.get_tournament_name(tournament_id)
    return HTMLResponse(output)
