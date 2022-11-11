import pandas as pd
import librosa
import os
import numpy as np


#  classical, jazz, pop, metal, rock, reggae, country, disco
def load_genres(genre):
    l = []
    data_dir = os.listdir('./data/' + genre)
    for file in data_dir[:10]:
        l.append(extract_features('./data/' + genre + "/" + str(file)))
    return l


def normalize(dist):
    norm_dist = []
    sm = np.array(dist).sum()

    for x in dist:
        norm_dist.append(np.round((x/sm)*100))
    return norm_dist


def euclidean(arg1, arg2):
    sm = 0
    for x in range(len(arg1)):
        sm += (arg1[x] - arg2[x]) ** 2
    return np.sqrt(sm)


def dtw_distance(arg1, arg2, window):
    n, m = arg1.shape[1], arg2.shape[1]
    w = np.max([window, abs(n - m)])

    # initialize DTW array
    DTW = np.zeros((n + 1, m + 1))
    DTW[:, :] = np.inf
    DTW[0, 0] = 0

    for i in range(1, n + 1):
        for j in range(np.max([1, i - w]), np.min([m, i + w]) + 1):
            DTW[i, j] = 0

    for i in range(1, n + 1):
        for j in range(np.max([1, i - w]), np.min([m, i + w]) + 1):
            cost = euclidean(arg1[:, i - 1], arg2[:, j - 1])
            DTW[i, j] = cost + np.min([DTW[i - 1, j], DTW[i, j - 1], DTW[i - 1, j - 1]])

    return DTW[n, m]


def extract_features(audio):
    y, sr = librosa.load(audio)
    return librosa.feature.mfcc(y=y, sr=sr)


def compute_dist(genre_files, audio):
    dist = 0
    for x in genre_files:
        dist += (dtw_distance(x, audio, 5))
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
        w = compute_dist(x, au_mfcc)
        print(w)
        distances.append((1/w))

    return normalize(distances)
