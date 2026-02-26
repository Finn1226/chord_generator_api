from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def get_root():
    return {'Chords': ['F', 'G', 'E', 'A', 'D', 'G', 'C']}

@app.get('/chords')
def get_chords(song_name: str):
    return {'Chords': ['D', 'G', 'C', 'C']}