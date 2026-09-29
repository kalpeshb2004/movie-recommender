from fastapi import APIRouter, Depends, HTTPException

from ..database import get_db
from ..services.recommender import get_similar

router = APIRouter(prefix="/movies", tags=["recommend"])

CARD = "id, tmdb_id, title, genres, release_date, vote_average, poster_url, backdrop_url"


@router.get("/{movie_id}/recommend")
def recommend(movie_id: int, limit: int = 10, db=Depends(get_db)):
    exists = db.execute("SELECT id FROM movies WHERE id = ?", (movie_id,)).fetchone()
    if exists is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    similar_ids = get_similar(movie_id, top_n=limit)
    if not similar_ids:
        return []

    placeholders = ",".join("?" * len(similar_ids))
    rows = db.execute(
        f"SELECT {CARD} FROM movies WHERE id IN ({placeholders})", similar_ids
    ).fetchall()

    order = {mid: i for i, mid in enumerate(similar_ids)}
    result = [dict(r) for r in rows]
    result.sort(key=lambda r: order[r["id"]])
    return result