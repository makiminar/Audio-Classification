import os
import random
from audio_classifier import AudioClassifier


#  classical, jazz, pop, metal, rock, reggae, country, disco

class SongWiseClassifier(AudioClassifier):
    def __init__(self, genres_names=None, n_mfcc=3, window_size=5, train_size=None, metric="l2"):
        super().__init__(genres_names, n_mfcc, window_size, train_size, metric)

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
