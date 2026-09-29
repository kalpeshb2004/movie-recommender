import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")

DB_PATH = ROOT / "backend" / "movies.db"
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
JWT_SECRET = os.getenv("JWT_SECRET")