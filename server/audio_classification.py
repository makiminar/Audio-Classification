import pandas as pd
import librosa
import os
import numpy as np
import random


#  classical, jazz, pop, metal, rock, reggae, country, disco

class AudioClassifier:
    def __init__(self, genres_names=None, n_mfcc=3, window_size=5, train_size=None, metric="l2"):
        self.n_mfcc = n_mfcc
        self.window_size = window_size
        self.genres = []
        if genres_names is None:
            genres_names = ["classical", "country", "disco", "hiphop", "jazz", "metal", "pop", "reggae", "rock",
                            "blues"]
        self.genres_names = genres_names
        self.train_size = train_size
        self.metric = metric

        self.genres = []
        for genre in genres_names:
            self.genres.append(self.load_genre(genre))

    def load_genre(self, genre):
        l = []
        if self.train_size:
            directory_path = './data/train/' + genre
            filenames = random.sample(os.listdir(directory_path), self.train_size)
            for fname in filenames:
                try:
                    l.append(self.extract_features('./data/train/' + genre + "/" + str(fname)))
                except:
                    print(f"Error during load of a song: ./data/train/ {genre}/{str(fname)}")
        else:
            for file in os.listdir('./data/train/' + genre):
                try:
                    l.append(self.extract_features('./data/train/' + genre + "/" + str(file)))
                except:
                    print(f"Error during load of a song: ./data/train/ {genre}/{str(file)}")
        return l

    def normalize(self, dist):
        norm_dict = {}
        sm = np.array(dist).sum()

        for x in range(len(dist)):
            norm_dict[self.genres_names[x]] = (dist[x] / sm) * 100
        return dict(sorted(norm_dict.items(), key=lambda item: item[1], reverse=True))

    def l_metrics(self, arg1, arg2, exp=2):
        sm = 0
        for x in range(len(arg1)):
            sm += abs(arg1[x] - arg2[x]) ** exp
        return sm ** (1.0 / exp)

    def l_max(self, arg1, arg2):
        max = 0
        for x in range(len(arg1)):
            if abs(arg1[x] - arg2[x]) > max:
                max = abs(arg1[x] - arg2[x])
        return max

    def dtw_distance(self, arg1, arg2):
        n, m = arg1.shape[1], arg2.shape[1]
        w = np.max([self.window_size, abs(n - m)])

        # initialize DTW array
        DTW = np.zeros((n + 1, m + 1))
        DTW[:, :] = np.inf
        DTW[0, 0] = 0

        for i in range(1, n + 1):
            for j in range(np.max([1, i - w]), np.min([m, i + w]) + 1):
                DTW[i, j] = 0

        for i in range(1, n + 1):
            for j in range(np.max([1, i - w]), np.min([m, i + w]) + 1):
                if self.metric == "l1":
                    cost = self.l_metrics(arg1[:, i - 1], arg2[:, j - 1], exp=1)
                elif self.metric == "l2":
                    cost = self.l_metrics(arg1[:, i - 1], arg2[:, j - 1], exp=2)
                elif self.metric == "l3":
                    cost = self.l_metrics(arg1[:, i - 1], arg2[:, j - 1], exp=3)
                elif self.metric == "l_max":
                    cost = self.l_max(arg1[:, i - 1], arg2[:, j - 1])
                else:
                    cost = self.l_metrics(arg1[:, i - 1], arg2[:, j - 1], exp=2)
                DTW[i, j] = cost + np.min([DTW[i - 1, j], DTW[i, j - 1], DTW[i - 1, j - 1]])

        return DTW[n, m]

    def extract_features(self, audio):
        y, sr = librosa.load(audio)
        return librosa.feature.mfcc(y=y, sr=sr, n_mfcc=self.n_mfcc)

    def compute_dist(self, genre_files, audio):
        dist = 0
        for x in genre_files:
            dist += (self.dtw_distance(x, audio))
            # D, wp = librosa.sequence.dtw(x, audio)
            # dist += D[-1, -1]
        return dist / len(genre_files)

    def classify(self, audio, test=False):
        au_mfcc = self.extract_features(audio)
        distances = []

        for x in self.genres:
            w = self.compute_dist(x, au_mfcc)
            if not test:
                print(w)
            distances.append((1 / w))

        if test:
            argmax = np.argmax(distances)
            return self.genres_names[argmax]
        else:
            return self.normalize(distances)

    def test(self, test_size=10, metric="l2"):
        self.metric = metric
        succ = 0
        all = 0
        for genre in self.genres_names:
            tmp_succ = 0
            tmp_all = 0
            directory_path = './data/test/' + genre
            filenames = random.sample(os.listdir(directory_path), test_size)
            for song in filenames:
                song_path = directory_path + "/" + song
                result = self.classify(song_path, test=True)
                tmp_all += 1
                if result == genre:
                    tmp_succ += 1
            succ += tmp_succ
            all += tmp_all
            print(f"Genre: {genre} completed, Accuracy for genre: {tmp_succ / tmp_all * 100}%")
        accuracy = succ / all
        print(f"--------------------------------------")
        print(f"Metric: {self.metric}, N_mfcc: {self.n_mfcc}, Train_size: {self.train_size}, Test_size: {test_size}, "
              f"Window_size: {self.window_size}")
        print(f"Final Accuracy: {accuracy * 100}%")
        print(f"--------------------------------------")
        return accuracy
