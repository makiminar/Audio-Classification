import pandas as pd
import librosa
from dtw import *
import os


#  classical, jazz, pop, metal, rock, reggae, country, disco
def load_genres(genre):
    folder = os.listdir('./data/' + genre)
    l = []
    for x in range(10):
        l.append(extract_features(folder[x]))
    return l


def extract_features(audio):
    y, sr = librosa.load(audio)
    return librosa.feature.mfcc(y=y, sr=sr)


def compute_dist(genre_files, audio):
    dist = 0
    for x in genre_files:
        dist += dtw(x, audio)
    return dist / len(genre_files)


def classify(audio):
    classical = load_genres("classical")
    country = load_genres("country")
    disco = load_genres("disco")
    hiphop = load_genres("hiphop")
    jazz = load_genres("jazz")
    metal = load_genres("metal")
    pop = load_genres("pop")
    reggae = load_genres("reggae")
    rock = load_genres("rock")

    au_mfcc = extract_features(audio)

    distances = []
    genres = [classical, country, disco, hiphop, jazz, metal, pop, reggae, rock]

    for x in genres:
        distances.append(compute_dist(x, au_mfcc))

    return distances
