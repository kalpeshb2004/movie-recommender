CREATE TABLE IF NOT EXISTS movies (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    tmdb_id       INTEGER UNIQUE,
    title         TEXT NOT NULL,
    overview      TEXT,
    genres        TEXT,
    keywords      TEXT,
    cast_names    TEXT,
    director      TEXT,
    release_date  TEXT,
    vote_average  REAL,
    vote_count    INTEGER,
    popularity    REAL,
    poster_url    TEXT,
    backdrop_url  TEXT
);

CREATE TABLE IF NOT EXISTS users (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    username       TEXT UNIQUE NOT NULL,
    email          TEXT UNIQUE NOT NULL,
    password_hash  TEXT NOT NULL,
    created_at     TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS watchlist (
    user_id   INTEGER NOT NULL,
    movie_id  INTEGER NOT NULL,
    added_at  TEXT DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, movie_id),
    FOREIGN KEY (user_id)  REFERENCES users(id),
    FOREIGN KEY (movie_id) REFERENCES movies(id)
);

CREATE TABLE IF NOT EXISTS search_history (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER NOT NULL,
    movie_id     INTEGER NOT NULL,
    searched_at  TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id)  REFERENCES users(id),
    FOREIGN KEY (movie_id) REFERENCES movies(id)
);

CREATE INDEX IF NOT EXISTS idx_movies_title ON movies(title);