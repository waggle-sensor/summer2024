# Computes and displays the mel-spectrogram of an audio file.

import librosa, librosa.display
import matplotlib.pyplot as plt
import numpy as np
import os 
import argparse


def display_mel_spectrogram(file, n_mels=256, n_fft=2048, hop_length=32, dpi=100):
    # load file and compute spectrogram
    y, sr = librosa.load(file)
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels, n_fft=n_fft, hop_length=hop_length)
    S_dB = librosa.power_to_db(S, ref=np.max)

    # display
    plt.figure(figsize=(15, 7), dpi=dpi)
    librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='mel')
    plt.colorbar(format='%+2.0f dB')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='Path to target file')
    parser.add_argument('--start')
    parser.add_argument('--stop')
    args = parser.parse_args()

    if args.start or args.stop:
        #display_mel_spectrogram(args.f, int(args.start), int(args.stop))
        raise NotImplementedError
    else:
        display_mel_spectrogram(args.f)
