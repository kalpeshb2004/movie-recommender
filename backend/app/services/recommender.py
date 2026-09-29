import sqlite3

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from ..config import DB_PATH

_movie_ids = []
_sim_matrix = None


def build_model():
    global _movie_ids, _sim_matrix

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT id, genres, keywords, cast_names, director, overview FROM movies"
    ).fetchall()
    conn.close()

    _movie_ids = [r["id"] for r in rows]
    soup = [
        f"{r['genres']} {r['keywords']} {r['cast_names']} {r['director']} {r['overview']}"
        for r in rows
    ]

    tfidf = TfidfVectorizer(stop_words="english")
    matrix = tfidf.fit_transform(soup)
    _sim_matrix = cosine_similarity(matrix)
    print("Recommender model ready:", len(_movie_ids), "movies")


def get_similar(movie_id: int, top_n: int = 10):
    if _sim_matrix is None:
        build_model()
    if movie_id not in _movie_ids:
        return []
    idx = _movie_ids.index(movie_id)
    scores = list(enumerate(_sim_matrix[idx]))
    scores.sort(key=lambda x: x[1], reverse=True)
    top = [s for s in scores if s[0] != idx][:top_n]
    return [_movie_ids[i] for i, _ in top]