from flask import Flask
from flask import request
from audio_classification import AudioClassifier
from audio_classification_aggregated_mfccs import AudioClassifierAggregatedMfccs
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.post("/")
def genre_post():
    # get audio file from request
    audio = request.files['audio']
    print(audio)
    if not audio:
        return "Failed during loading file."
    genres_names = ["classical", "country", "jazz", "metal", "pop"]
    # classifier = AudioClassifier(genres_names=genres_names, train_size=10)
    classifier = AudioClassifierAggregatedMfccs(genres_names=genres_names)
    # compute distances of audio from genres
    return classifier.classify(audio)
