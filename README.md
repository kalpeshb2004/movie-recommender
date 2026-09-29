# MovieFlix — Movie Recommendation System

website - 
movie-recommenderk01.netlify.app

Netflix-style movie recommendation web app.

## Stack
- Backend: Python + FastAPI
- Database: SQLite
- Frontend: HTML, CSS, JavaScript (vanilla)
- Recommendation: TF-IDF + Cosine Similarity (scikit-learn)
- Data: TMDB 5000 Movie Dataset + TMDB API (posters/backdrops)

## Features
- Search movies, view details, get similar-movie recommendations
- Trending / Top Rated / Genre rows
- User signup/login (JWT auth)
- Personal watchlist
- Search history tracking

## Setup
1. `python -m venv venv` → activate
2. `pip install -r backend/requirements.txt`
3. Add TMDB API key to `.env`
4. `python backend/scripts/import_data.py`
5. `python backend/scripts/fetch_posters.py`
6. `cd backend && uvicorn app.main:app --reload`
7. Open `frontend/index.html` via Live Server

This product uses the TMDB API but is not endorsed or certified by TMDB.
