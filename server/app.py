from flask import Flask
from flask import request
from song_wise_classifier import SongWiseClassifier
from aggregated_mfccs_classifier import AudioClassifierAggregatedMfccs
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.post("/")
def genre_post():
    # get audio file from request
    audio = request.files['audio']
    method = request.form.get('method')
    print(method)
    if not audio:
        return "Failed during loading file."
    genres_names = ["classical", "country", "jazz", "metal", "pop"]
    if method == "Centroid Mfccs":
        return AudioClassifierAggregatedMfccs(genres_names=genres_names).classify(audio)
    elif method == "Song-wise Mfccs":
        return SongWiseClassifier(genres_names=genres_names, train_size=10).classify(audio)
    else:
        return "Method not supported."
    # python -m flask --app app run