from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from pydantic import BaseModel
from typing import Dict, List
from psycopg2.extras import Json

###
### SETTING UP
###
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

###
### GET
###
@app.get('/songs')
def get_all_chords():
    cur = conn.cursor()
    cur.execute("""
                SELECT title, artist
                FROM songs
                """)

    rows = cur.fetchall()
    return [{'title': row[0], 'artist': row[1]} for row in rows]

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

###
### POST
###
class SongCreate(BaseModel):
    title: str
    artist: str
    chords: Dict[str, List[str]]

@app.post('/songs')
def add_song(song: SongCreate):
    with conn.cursor() as cur:
        cur.execute("""
                    INSERT INTO songs (title, artist, chords)
                    VALUES (%s, %s, %s)""",
                    (song.title, song.artist, Json(song.chords))
        )
        conn.commit()

    return {
        'message': "Song created successfully",
        'title': song.title,
        'artist': song.artist,
        'chords': song.chords
    }

