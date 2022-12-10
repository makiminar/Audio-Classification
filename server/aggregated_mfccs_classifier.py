from collections import OrderedDict

import pandas as pd
import librosa
import os
import numpy as np
import random
from os.path import exists
from audio_classifier import AudioClassifier


#  classical, jazz, pop, metal, rock, reggae, country, disco

class AggregatedMfccsClassifier(AudioClassifier):
    def __init__(self, genres_names=None, n_mfcc=3, window_size=5, train_size=90, metric="l2"):
        super().__init__(genres_names, n_mfcc, window_size, train_size, metric)

    def load_genre(self, genre):
        # mfccs/{genre}/{n_mfcc}_{window_size}_{train_size}
        path_to_file = f'./mfccs/{genre}/{self.n_mfcc}_{self.window_size}_{self.train_size}'
        l = []
        if not exists(path_to_file + '.npy'):
            l.append(self.aggregate_mfcc(path_to_file, genre))
        else:
            l.append(self.load_aggregated_mfccs(path_to_file + '.npy'))
        return l

    def load_aggregated_mfccs(self, path_to_file):
        return np.load(path_to_file)

    def save_aggregated_mfccs(self, path_to_file, aggregated_mfccs):
        np.save(path_to_file, aggregated_mfccs)

    def aggregate_mfcc(self, path_to_file, genre):
        shortest_length = 10 ** 10
        aggregated_mfccs = np.zeros((self.n_mfcc, 10 ** 4))
        directory_path = './data/train/' + genre
        filenames = random.sample(os.listdir(directory_path), self.train_size)
        count = 0
        for fname in filenames:
            count += 1
            try:
                tmp_mfcc = super().extract_features('./data/train/' + genre + "/" + str(fname))
                if tmp_mfcc.shape[1] < shortest_length:
                    shortest_length = tmp_mfcc.shape[1]

                tmp_mfcc = tmp_mfcc.copy()
                tmp_mfcc = np.lib.pad(tmp_mfcc, ((0, 0), (0, aggregated_mfccs.shape[1] - tmp_mfcc.shape[1])),
                                      'constant', constant_values=(0))
                aggregated_mfccs += tmp_mfcc
            except:
                print(f"Error during load of a song: ./data/train/ {genre}/{str(fname)}")

        aggregated_mfccs = aggregated_mfccs[:, :shortest_length]
        if count != 0:
            aggregated_mfccs /= count

        self.save_aggregated_mfccs(path_to_file, aggregated_mfccs)
        return aggregated_mfccs
