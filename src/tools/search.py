import sqlite3 as sl
from datetime import datetime

import pandas as pd

from src.tools.format import ranking_row, tournaments_row, results_row

base = "./src/data"


class Ranking:
    def __init__(self):
        self.con = sl.connect(f"{base}/ranking.db")
        self.cur = self.con.cursor()

    def get_ranking(self, size: int = None) -> str:
        if size:
            db_ranking = pd.read_sql_query(
                f"""SELECT * FROM RANKING WHERE points > 0 LIMIT {size};""",
                self.con
            )
        else:
            db_ranking = pd.read_sql_query(
                f"""SELECT * FROM RANKING WHERE points > 0;""",
                self.con
            )
        table_ranking = [ranking_row(*row) for row in db_ranking.iloc]
        return "".join(table_ranking)

    def get_tournaments(self, size: int = None) -> str:
        ts = datetime.now().strftime("%Y%m%d")
        if size:
            db_tournaments = pd.read_sql_query(
                f"""SELECT id, name, ts FROM TOURNAMENTS WHERE ts < {ts} ORDER BY ts DESC LIMIT {size};""",
                self.con
            )
        else:
            db_tournaments = pd.read_sql_query(
                f"""SELECT id, name, ts FROM TOURNAMENTS WHERE ts < {ts} ORDER BY ts DESC;""",
                self.con
            )
        table_tournaments = [tournaments_row(*row) for row in db_tournaments.iloc]
        return "".join(table_tournaments)

    def get_results(self, tournament_id: int = -1) -> str:
        ts = datetime.now().strftime("%Y%m%d")
        if tournament_id == -1:
            tmp = pd.read_sql_query(
                f"""SELECT id FROM TOURNAMENTS WHERE ts < {ts} ORDER BY ts DESC LIMIT 1;""",
                self.con
            )
            tournament_id = int(tmp.iloc[0])
        db_results = pd.read_sql_query(
            f"""SELECT RESULTS.rank, PLAYERS.name, DISTRIBUTIONS.points
            FROM RESULTS
            JOIN PLAYERS ON PLAYERS.id = RESULTS.player_id
            JOIN DISTRIBUTIONS on RESULTS.rank = DISTRIBUTIONS.rank 
            WHERE RESULTS.tournament_id = {tournament_id}
            AND DISTRIBUTIONS.tier_id = (
                SELECT MAPPING.tier_id FROM MAPPING WHERE MAPPING.tournament_id = {tournament_id}
            );""",
            self.con
        )
        table_results = [results_row(*row) for row in db_results.iloc]
        return "".join(table_results)

    def get_tournament_name(self, tournament_id: int = -1) -> str:
        if tournament_id == -1:
            db_name = pd.read_sql_query(
                f"""SELECT name FROM TOURNAMENTS ORDER BY ts DESC LIMIT 1;""",
                self.con
            )
        else:
            db_name = pd.read_sql_query(
                f"""SELECT name FROM TOURNAMENTS WHERE id = {tournament_id} LIMIT 1;""",
                self.con
            )
        table_name = db_name.iloc[0]["name"]
        return "".join(table_name)
