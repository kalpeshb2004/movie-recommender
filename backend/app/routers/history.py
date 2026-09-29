from fastapi import APIRouter, Depends

from ..database import get_db
from .auth import get_current_user

router = APIRouter(prefix="/history", tags=["history"])


@router.post("/{movie_id}")
def log_search(movie_id: int, user_id: int = Depends(get_current_user), db=Depends(get_db)):
    db.execute(
        "INSERT INTO search_history (user_id, movie_id) VALUES (?, ?)", (user_id, movie_id)
    )
    db.commit()
    return {"status": "logged"}


@router.get("")
def get_history(user_id: int = Depends(get_current_user), db=Depends(get_db)):
    rows = db.execute(
        """SELECT DISTINCT m.id, m.title, m.poster_url
           FROM search_history h JOIN movies m ON m.id = h.movie_id
           WHERE h.user_id = ? ORDER BY h.searched_at DESC LIMIT 10""",
        (user_id,),
    ).fetchall()
    return [dict(r) for r in rows]