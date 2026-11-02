from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .routers import auth, history, movies, recommend, watchlist
from .services.recommender import build_model

app = FastAPI(title="Movie Recommender")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(movies.router)
app.include_router(recommend.router)
app.include_router(auth.router)
app.include_router(watchlist.router)
app.include_router(history.router)


@app.on_event("startup")
def startup():
    build_model()


# sabse last me, routers ke baad
FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")