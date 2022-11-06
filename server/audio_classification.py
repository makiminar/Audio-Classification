import pandas as pd
import librosa
import os
import numpy as np


#  classical, jazz, pop, metal, rock, reggae, country, disco
def load_genres(genre):
    l = []
    for file in os.listdir('./data/' + genre):
        l.append(extract_features('./data/' + genre + "/" + str(file)))
    return l


# dtw for 2 sequences
def dtw_distance(arg1, arg2, window):
    n, m = len(arg1), len(arg2)
    print("n: ", n)
    print("m: ", m)

    w = np.max([window, abs(n - m)])

    # initialize DTW array
    DTW = np.zeros((n + 1, m + 1))
    DTW[0, :] = np.inf
    DTW[:, 0] = np.inf
    DTW[0, 0] = 0

    print(DTW.shape)

    for i in range(1, n + 1):
        for j in range(np.max([1, i - w]), np.min([m, i + w]) + 1):
            DTW[i, j] = 0

    for i in range(1, n + 1):
        for j in range(np.max([1, i - w]), np.min([m, i + w]) + 1):
            cost = np.linalg.norm(arg1[i-1] - arg2[j-1])
            DTW[i, j] = cost + np.min([DTW[i - 1, j], DTW[i, j - 1], DTW[i - 1, j - 1]])
            print(DTW[i, j])

    return DTW[n, m]


def extract_features(audio):
    y, sr = librosa.load(audio)
    return librosa.feature.mfcc(y=y, sr=sr)


def compute_dist(genre_files, audio):
    dist = 0
    for x in genre_files:
        dist += dtw_distance(x, audio, 3)
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

    # for x in genres:
    #   distances.append(compute_dist(x, au_mfcc))

    return distances
