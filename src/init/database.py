import sqlite3 as sl

import pandas as pd
from loguru import logger

base = f"./src/data2"

con = sl.connect(f"{base}/ranking.db")

logger.info("Created Database")
logger.info("Creating Players table")

# Players
with con:
    con.execute("""
        CREATE TABLE IF NOT EXISTS PLAYERS (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            country TEXT,
            team TEXT
        );
    """)

logger.info("Created Players table")
logger.info("Populating Players table")

sql_players = """
    INSERT INTO PLAYERS (id, name, country, team) values(?, ?, ?, ?)
"""
df_players = pd.read_csv(f"{base}/players.csv")
players = [(int(player[0]), player[1], player[2], player[3]) for player in df_players.iloc]
with con:
    con.executemany(sql_players, players)

logger.info("Players table ready")
logger.info("Creating Tournaments table")

# Tournaments
with con:
    con.execute("""
        CREATE TABLE IF NOT EXISTS TOURNAMENTS (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            ts INTEGER
        );
    """)

logger.info("Created Tournaments table")
logger.info("Populating Tournaments table")

sql_tournaments = """
    INSERT INTO TOURNAMENTS (id, name, ts) values(?, ?, ?)
"""
df_tournaments = pd.read_csv(f"{base}/tournaments.csv")
tournaments = [(int(tournament[0]), tournament[1], int(tournament[2])) for tournament in df_tournaments.iloc]
with con:
    con.executemany(sql_tournaments, tournaments)

logger.info("Tournaments table ready")
logger.info("Creating Tiers table")

# Tiers
with con:
    con.execute("""
        CREATE TABLE IF NOT EXISTS TIERS (
            id INTEGER,
            name TEXT,
            description TEXT
        );
    """)

logger.info("Created Tiers table")
logger.info("Populating Tiers table")

sql_tiers = """
    INSERT INTO TIERS (id, name, description) values(?, ?, ?)
"""
df_tiers = pd.read_csv(f"{base}/tiers.csv")
tiers = [(int(tier[0]), tier[1], tier[2]) for tier in df_tiers.iloc]
with con:
    con.executemany(sql_tiers, tiers)

logger.info("Tiers table ready")
logger.info("Creating Mapping table")

# Mapping
with con:
    con.execute("""
        CREATE TABLE IF NOT EXISTS MAPPING (
            tournament_id INTEGER,
            tier_id INTEGER
        );
    """)

logger.info("Created Mapping table")
logger.info("Populating Mapping table")

sql_mapping = """
    INSERT INTO MAPPING (tournament_id, tier_id) values(?, ?)
"""
df_mapping = pd.read_csv(f"{base}/mapping.csv")
mapping = [(int(mapping_[0]), int(mapping_[1])) for mapping_ in df_mapping.iloc]
with con:
    con.executemany(sql_mapping, mapping)

logger.info("Mapping table ready")
logger.info("Creating Distributions table")

# Distributions
with con:
    con.execute("""
        CREATE TABLE IF NOT EXISTS DISTRIBUTIONS (
            tier_id INTEGER,
            rank INTEGER,
            points INTEGER
        );
    """)

logger.info("Created Distributions table")
logger.info("Populating Distributions table")

sql_distributions = """
    INSERT INTO DISTRIBUTIONS (tier_id, rank, points) values(?, ?, ?)
"""
df_distributions = pd.read_csv(f"{base}/distributions.csv")
distributions = [(int(distribution[0]), int(distribution[1]), int(distribution[2])) for distribution in df_distributions.iloc]
with con:
    con.executemany(sql_distributions, distributions)

logger.info("Distributions table ready")
logger.info("Creating Results table")

# Results
with con:
    con.execute("""
        CREATE TABLE IF NOT EXISTS RESULTS (
            tournament_id INTEGER,
            player_id INTEGER,
            rank INTEGER
        );
    """)

logger.info("Created Results table")
logger.info("Populating Results table")

sql_results = """
    INSERT INTO RESULTS (tournament_id, player_id, rank) values(?, ?, ?)
"""
df_results = pd.read_csv(f"{base}/results.csv")
results = [(int(result[0]), int(result[1]), int(result[2])) for result in df_results.iloc]
with con:
    con.executemany(sql_results, results)

logger.info("Results table ready")
logger.info("Creating Ranking table")

# Results
with con:
    con.execute("""
        CREATE TABLE IF NOT EXISTS RANKING (
            rank INTEGER,
            name TEXT,
            country TEXT,
            team TEXT,
            points INTEGER
        );
    """)

logger.info("Created Ranking table")
logger.info("Ranking table ready")

con.close()
