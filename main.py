from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["https://lihongfei.com", "http://lihongfei.com"],
    allow_methods = ['GET'],
    allow_headers = ['*']
)

conn = psycopg2.connect(
    dbname = 'chordapp',
    user = 'finn',
    host = 'localhost',
    port = '5432'
)

@app.get('/songs')
def get_all_chords():
    cur = conn.cursor()
    cur.execute("""
                SELECT title, artist
                FROM songs
                """)

    rows = cur.fetchall()

    songs = [
        {'title': row[0], 'artist': row[1]} for row in rows
    ]
    return songs

@app.get('/chords')
def get_chords(song_name: str):
    cur = conn.cursor()
    cur.execute(
        """
        SELECT chords
        FROM songs
        WHERE title = %s
        """,
        (song_name,)
    )

    result = cur.fetchone()

    if result is None:
        return {'error': "song not found"}
    return result[0]