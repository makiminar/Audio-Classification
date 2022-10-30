from flask import Flask
from flask import request
import audio_classification

app = Flask(__name__)


@app.post("/")
def genre_post():
    # get audio file from request
    audio = request.args.get('audio')

    # compute distances of audio from genres
    dist = audio_classification.classify(audio)

    # normalize distances to 1

    return "<h1>No genre, yet!</h1>"

