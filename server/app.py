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
    method = request.form.get('method')
    print(method)
    if not audio:
        return "Failed during loading file."
    genres_names = ["classical", "country", "jazz", "metal", "pop"]
    if method == "Aggregated Mfccs":
        return AudioClassifierAggregatedMfccs(genres_names=genres_names).classify(audio)
    elif method == "Song-wise Mfccs":
        return AudioClassifier(genres_names=genres_names, train_size=10).classify(audio)
    else:
        return "Method not supported."
    # python -m flask --app app run