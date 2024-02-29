import difflib
import json
import sqlite3 as sl

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.requests import Request

from tools.ranking import Ranking

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

con = sl.connect("data/ranking.db")
cur = con.cursor()

res = cur.execute("""SELECT * FROM PLAYERS""").fetchall()
PLAYERS = {k: v for d in list(map(lambda x: {x[1]: x[2]}, res)) for k, v in d.items()}
PLAYERS_KEYS = PLAYERS.keys()

res = cur.execute("""SELECT * FROM TOURNAMENTS""").fetchall()
TOURNAMENTS = {k: v for d in list(map(lambda x: {x[1]: x[2]}, res)) for k, v in d.items()}
TOURNAMENTS_KEYS = TOURNAMENTS.keys()

LATEST_TOURNAMENTS = cur.execute("""SELECT * FROM TOURNAMENTS ORDER BY ts DESC LIMIT 5""").fetchall()


@app.post("/search-player")
async def post_method(request: Request):
    data = await request.body()
    data = json.loads(data)
    name = data.get("name", "")
    result = difflib.get_close_matches(name, PLAYERS_KEYS, n=3, cutoff=0)
    return JSONResponse([[str(i), r, PLAYERS[r]] for i, r in enumerate(result)])


@app.post("/search-tournament")
async def post_method(request: Request):
    data = await request.body()
    data = json.loads(data)
    name = data.get("name", "")
    result = difflib.get_close_matches(name, TOURNAMENTS_KEYS, n=5, cutoff=0)
    return JSONResponse([[str(i), r, TOURNAMENTS[r]] for i, r in enumerate(result)])


@app.post("/last-tournaments")
async def post_method(request: Request):
    data = await request.body()
    return JSONResponse([[str(i+3), r[1], r[2]] for i, r in enumerate(LATEST_TOURNAMENTS)])


@app.post("/get-ranking")
async def post_method(request: Request):
    data = await request.body()
    data = json.loads(data)
    size = data.get("size", 20)
    result = ranking(size=size)
    return JSONResponse([[str(i+1), r[0], r[1], str(r[2])] for i, r in enumerate(result)])


@app.post("/add-player")
async def post_method(request: Request):
    data = await request.body()
    data = json.loads(data)
    name = data.get("name", False)
    country = data.get("country", False)
    s = "error"
    if name and country:
        with con:
            con.execute(f"""
                INSERT INTO PLAYERS (name, country) values('{name}', '{country}')
            """)
        s = "success"
    return JSONResponse([s])


# uvicorn search:app --reload
