from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["https://lihongfei.com", "http://lihongfei.com"],
    allow_methods = ['GET'],
    allow_headers = ['*']
)

@app.get('/')
def get_root():
    return {'Chords': ['F', 'G', 'E', 'A', 'D', 'G', 'C']}

@app.get('/chords')
def get_chords(song_name: str):
    return {'Chords': ['D', 'G', 'C', 'C']}