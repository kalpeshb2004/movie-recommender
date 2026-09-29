from fastapi import APIRouter, Depends

from ..database import get_db
from .auth import get_current_user

router = APIRouter(prefix="/watchlist", tags=["watchlist"])

CARD = "id, title, genres, release_date, vote_average, poster_url"


@router.get("")
def list_watchlist(user_id: int = Depends(get_current_user), db=Depends(get_db)):
    rows = db.execute(
        f"""SELECT m.{CARD.replace(", ", ", m.")}
            FROM watchlist w JOIN movies m ON m.id = w.movie_id
            WHERE w.user_id = ? ORDER BY w.added_at DESC""",
        (user_id,),
    ).fetchall()
    return [dict(r) for r in rows]


@router.post("/{movie_id}")
def add_watchlist(movie_id: int, user_id: int = Depends(get_current_user), db=Depends(get_db)):
    db.execute(
        "INSERT OR IGNORE INTO watchlist (user_id, movie_id) VALUES (?, ?)",
        (user_id, movie_id),
    )
    db.commit()
    return {"status": "added"}


@router.delete("/{movie_id}")
def remove_watchlist(movie_id: int, user_id: int = Depends(get_current_user), db=Depends(get_db)):
    db.execute(
        "DELETE FROM watchlist WHERE user_id = ? AND movie_id = ?", (user_id, movie_id)
    )
    db.commit()
    return {"status": "removed"}