import json
import sqlite3
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "backend" / "movies.db"
SCHEMA_PATH = ROOT / "backend" / "sql" / "schema.sql"

movies = pd.read_csv(ROOT / "data" / "tmdb_5000_movies.csv")
credits = pd.read_csv(ROOT / "data" / "tmdb_5000_credits.csv")

df = movies.merge(credits, left_on="id", right_on="movie_id", suffixes=("", "_c"))
df = df.fillna("")


def names(text, limit=None):
    try:
        items = json.loads(text) if text else []
    except json.JSONDecodeError:
        return ""
    out = [i["name"] for i in items]
    return ",".join(out[:limit] if limit else out)


def director(text):
    try:
        crew = json.loads(text) if text else []
    except json.JSONDecodeError:
        return ""
    for p in crew:
        if p.get("job") == "Director":
            return p["name"]
    return ""


conn = sqlite3.connect(DB_PATH)
conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
conn.execute("DELETE FROM movies")

rows = [
    (
        int(r["id"]),
        r["title"],
        r["overview"],
        names(r["genres"]),
        names(r["keywords"]),
        names(r["cast"], 5),
        director(r["crew"]),
        r["release_date"],
        float(r["vote_average"] or 0),
        int(r["vote_count"] or 0),
        float(r["popularity"] or 0),
    )
    for _, r in df.iterrows()
]

conn.executemany(
    """INSERT INTO movies
       (tmdb_id, title, overview, genres, keywords, cast_names, director,
        release_date, vote_average, vote_count, popularity)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
    rows,
)
conn.commit()
print("Imported:", conn.execute("SELECT COUNT(*) FROM movies").fetchone()[0])
conn.close()