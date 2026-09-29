from fastapi import APIRouter, Depends, HTTPException, Query

from ..database import get_db

router = APIRouter(prefix="/movies", tags=["movies"])

CARD = "id, tmdb_id, title, genres, release_date, vote_average, poster_url, backdrop_url"


@router.get("/search")
def search(q: str = Query(..., min_length=1), limit: int = 20, db=Depends(get_db)):
    rows = db.execute(
        f"SELECT {CARD} FROM movies WHERE title LIKE ? ORDER BY popularity DESC LIMIT ?",
        (f"%{q}%", limit),
    ).fetchall()
    return [dict(r) for r in rows]


@router.get("/trending")
def trending(limit: int = 20, db=Depends(get_db)):
    rows = db.execute(
        f"SELECT {CARD} FROM movies ORDER BY popularity DESC LIMIT ?", (limit,)
    ).fetchall()
    return [dict(r) for r in rows]


@router.get("/top-rated")
def top_rated(limit: int = 20, db=Depends(get_db)):
    rows = db.execute(
        f"SELECT {CARD} FROM movies WHERE vote_count >= 500 "
        "ORDER BY vote_average DESC LIMIT ?",
        (limit,),
    ).fetchall()
    return [dict(r) for r in rows]


@router.get("/genre/{genre}")
def by_genre(genre: str, limit: int = 20, db=Depends(get_db)):
    rows = db.execute(
        f"SELECT {CARD} FROM movies WHERE genres LIKE ? ORDER BY popularity DESC LIMIT ?",
        (f"%{genre}%", limit),
    ).fetchall()
    return [dict(r) for r in rows]


@router.get("/{movie_id}")
def detail(movie_id: int, db=Depends(get_db)):
    row = db.execute("SELECT * FROM movies WHERE id = ?", (movie_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return dict(row)