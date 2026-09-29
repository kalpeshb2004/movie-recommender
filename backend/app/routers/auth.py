from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ..database import get_db
from ..schemas import LoginIn, SignupIn
from ..services.auth_utils import create_token, decode_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()


@router.post("/signup")
def signup(body: SignupIn, db=Depends(get_db)):
    exists = db.execute(
        "SELECT id FROM users WHERE email = ? OR username = ?",
        (body.email, body.username),
    ).fetchone()
    if exists:
        raise HTTPException(status_code=400, detail="Email or username already used")

    cur = db.execute(
        "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
        (body.username, body.email, hash_password(body.password)),
    )
    db.commit()
    token = create_token(cur.lastrowid)
    return {"token": token, "username": body.username}


@router.post("/login")
def login(body: LoginIn, db=Depends(get_db)):
    row = db.execute(
        "SELECT id, username, password_hash FROM users WHERE email = ?", (body.email,)
    ).fetchone()
    if row is None or not verify_password(body.password, row["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_token(row["id"])
    return {"token": token, "username": row["username"]}


def get_current_user(creds: HTTPAuthorizationCredentials = Depends(security)) -> int:
    try:
        return decode_token(creds.credentials)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")