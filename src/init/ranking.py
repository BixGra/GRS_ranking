import sqlite3 as sl
from datetime import datetime, timedelta

import pandas as pd

base = "./src/data2"

con = sl.connect(f"{base}/ranking.db")
cur = con.cursor()

db_players = pd.read_sql_query("""SELECT * FROM PLAYERS""", con)
db_mapping = pd.read_sql_query("""SELECT * FROM MAPPING""", con)
db_distributions = pd.read_sql_query("""SELECT * FROM DISTRIBUTIONS""", con)
db_tournaments = pd.read_sql_query("""SELECT * FROM TOURNAMENTS""", con)
db_results = pd.read_sql_query("""SELECT * FROM RESULTS""", con)

players = {}
for player in db_players.iloc:
    player_id = player[0]
    player_name = player[1]
    player_country = player[2]
    player_team = player[3]
    players[player_id] = {
        "name": player_name,
        "country": player_country,
        "team": player_team,
        "points": 0
    }

mappings = {}
for mapping in db_mapping.iloc:
    tournament_id = mapping[0]
    tournament_tier = mapping[1]
    mappings[tournament_id] = tournament_tier

distributions = {}
for distribution_id in db_distributions["tier_id"].unique():
    db_distributions_tmp = db_distributions[db_distributions["tier_id"] == distribution_id]
    distribution_ = {}
    for distribution in db_distributions_tmp.iloc:
        rank = distribution[1]
        points = distribution[2]
        distribution_[rank] = points
    distributions[distribution_id] = distribution_

tournaments = {}
for tournament in db_tournaments.iloc:
    tournament_id = tournament[0]
    tournament_name = tournament[1]
    ts = datetime.strptime(str(tournament[2]), '%Y%m%d').date()
    # if ts - datetime.now() < timedelta(days=365):
    try:
        tournament_tier = mappings[tournament_id]
        tournaments[tournament_id] = {
            "name": tournament_name,
            "ts": ts,
            "distribution_id": tournament_tier
        }
    except KeyError:
        pass

for result in db_results.iloc:
    tournament_id = result[0]
    try:
        tournament = tournaments[tournament_id]
        distribution_id = tournament["distribution_id"]
        distribution = distributions[distribution_id]
        player_id = result[1]
        rank = result[2]
        if rank <= 16:
            players[player_id]["points"] += distribution[rank]  # Top 16
        elif rank <= 32:
            players[player_id]["points"] += distribution[17]  # Top 17-32
        elif rank <= 64:
            players[player_id]["points"] += distribution[33]  # Top 33-64
        else:
            players[player_id]["points"] += distribution[65]  # Top 65+
    except KeyError:
        pass

players_ranking = [[player["name"], player["country"], player["team"], player["points"]] for player in players.values()]
players_ranking = sorted(players_ranking, key=lambda x: x[3], reverse=True)

df_ranking = pd.DataFrame(players_ranking, columns=["name", "county", "team", "points"]).reset_index().rename(columns={"index": "rank"})
df_ranking.to_csv(f"{base}/ranking.csv", index=False)

sql_results = """
    INSERT INTO RANKING (rank, name, country, team, points) values(?, ?, ?, ?, ?)
"""
df_results = pd.read_csv(f"{base}/ranking.csv")
results = [(int(result[0]), result[1], result[2], result[3], int(result[4])) for result in df_ranking.iloc]
with con:
    con.executemany(sql_results, results)

con.close()
