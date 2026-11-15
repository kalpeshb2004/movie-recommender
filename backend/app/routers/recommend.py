from fastapi import APIRouter, Depends, HTTPException

from ..database import get_db
from ..services.recommender import get_similar, get_similar_for_many
from .auth import get_current_user

router = APIRouter(prefix="/movies", tags=["recommend"])
personal_router = APIRouter(prefix="/me", tags=["personal"])

CARD = "id, tmdb_id, title, genres, release_date, vote_average, poster_url, backdrop_url"


def fetch_cards(db, ids):
    if not ids:
        return []
    placeholders = ",".join("?" * len(ids))
    rows = db.execute(
        f"SELECT {CARD} FROM movies WHERE id IN ({placeholders})", ids
    ).fetchall()
    order = {mid: i for i, mid in enumerate(ids)}
    result = [dict(r) for r in rows]
    result.sort(key=lambda r: order[r["id"]])
    return result


@router.get("/{movie_id}/recommend")
def recommend(movie_id: int, limit: int = 10, db=Depends(get_db)):
    exists = db.execute("SELECT id FROM movies WHERE id = ?", (movie_id,)).fetchone()
    if exists is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return fetch_cards(db, get_similar(movie_id, top_n=limit))


@personal_router.get("/recommendations")
def my_recommendations(
    limit: int = 20,
    user_id: int = Depends(get_current_user),
    db=Depends(get_db),
):
    history = db.execute(
        "SELECT movie_id FROM search_history WHERE user_id = ? ORDER BY id DESC LIMIT 15",
        (user_id,),
    ).fetchall()
    watchlist = db.execute(
        "SELECT movie_id FROM watchlist WHERE user_id = ?", (user_id,)
    ).fetchall()

    weights = {}
    for rank, r in enumerate(history):
        weights[r["movie_id"]] = weights.get(r["movie_id"], 0) + 1.0 / (1 + 0.15 * rank)
    for r in watchlist:
        weights[r["movie_id"]] = weights.get(r["movie_id"], 0) + 2.0

    if not weights:
        return []
    return fetch_cards(db, get_similar_for_many(weights, top_n=limit))