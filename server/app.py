from flask import Flask
from flask import request
import pandas as pd
import librosa

app = Flask(__name__)


@app.post("/")
def genre_post():
    # funkce na podobnostni vyhledavani
    audio = request.args.get('audio')
    return "<h1>No genre, yet!</h1>"

