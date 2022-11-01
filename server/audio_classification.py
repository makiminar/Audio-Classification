import pandas as pd
import librosa
import os
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
import numpy as np


#  classical, jazz, pop, metal, rock, reggae, country, disco
def load_genres(genre):
    l = []
    for file in os.listdir('./data/' + genre):
        l.append(extract_features('./data/' + genre + "/" + str(file)))
    return l


def dtw_distance(arg1, arg2):
    distance, path = fastdtw(arg1, arg2, dist=euclidean)
    return distance


def extract_features(audio):
    y, sr = librosa.load(audio)
    return librosa.feature.mfcc(y=y, sr=sr).T


def compute_dist(genre_files, audio):
    dist = 0
    for x in genre_files:
        dist += dtw_distance(x, audio)
    return dist / len(genre_files)


def classify(audio):
    classical = load_genres("classical")
    # country = load_genres("country")
    # disco = load_genres("disco")
    # hiphop = load_genres("hiphop")
    # jazz = load_genres("jazz")
    # metal = load_genres("metal")
    # pop = load_genres("pop")
    # reggae = load_genres("reggae")
    # rock = load_genres("rock")

    au_mfcc = extract_features(audio)

    distances = []
    # genres = [classical, country, disco, hiphop, jazz, metal, pop, reggae, rock]
    genres = [classical]

    for x in genres:
        distances.append(compute_dist(x, au_mfcc))

    return distances
