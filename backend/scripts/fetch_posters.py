import os
import sqlite3
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")

API_KEY = os.getenv("TMDB_API_KEY")
DB_PATH = ROOT / "backend" / "movies.db"
IMG = "https://image.tmdb.org/t/p"

if not API_KEY or API_KEY == "teri_key_yaha":
    sys.exit("TMDB_API_KEY .env mein daal pehle.")

limit = int(sys.argv[1]) if len(sys.argv) > 1 else None

conn = sqlite3.connect(DB_PATH)
sql = "SELECT tmdb_id FROM movies WHERE poster_url IS NULL"
if limit:
    sql += f" LIMIT {limit}"
ids = [r[0] for r in conn.execute(sql)]
print(f"{len(ids)} movies process hongi")

session = requests.Session()
done = 0
for tmdb_id in ids:
    try:
        r = session.get(
            f"https://api.themoviedb.org/3/movie/{tmdb_id}",
            params={"api_key": API_KEY},
            timeout=10,
        )
        if r.status_code == 429:
            time.sleep(2)
            continue
        if r.status_code != 200:
            print("skip", tmdb_id, r.status_code)
            continue
        d = r.json()
        poster = f"{IMG}/w500{d['poster_path']}" if d.get("poster_path") else ""
        backdrop = f"{IMG}/w1280{d['backdrop_path']}" if d.get("backdrop_path") else ""
        conn.execute(
            "UPDATE movies SET poster_url=?, backdrop_url=? WHERE tmdb_id=?",
            (poster, backdrop, tmdb_id),
        )
        done += 1
        if done % 50 == 0:
            conn.commit()
            print(done, "done")
    except requests.RequestException as e:
        print("error", tmdb_id, e)

conn.commit()
conn.close()
print("Finished:", done)