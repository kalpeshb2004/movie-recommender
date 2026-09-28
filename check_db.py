import sqlite3

c = sqlite3.connect("backend/movies.db")
null = c.execute("SELECT COUNT(*) FROM movies WHERE poster_url IS NULL").fetchone()[0]
empty = c.execute("SELECT COUNT(*) FROM movies WHERE poster_url = ''").fetchone()[0]
total = c.execute("SELECT COUNT(*) FROM movies").fetchone()[0]
print("total:", total, "| NULL:", null, "| empty:", empty)