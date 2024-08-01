# Computes and displays a graph of the peak times in an audio file
# https://librosa.org/doc/latest/generated/librosa.util.peak_pick.html

import matplotlib.pyplot as plt
import librosa
import numpy as np


def find_peaks(file, delta=0.75):
    y, sr = librosa.load(file)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr,
                                            hop_length=512,
                                            aggregate=np.median)
    
    peaks = librosa.util.peak_pick(onset_env,
                                   pre_max=3,
                                   post_max=3,
                                   pre_avg=3,
                                   post_avg=5,
                                   delta=delta,
                                   wait=10)
    print(peaks)

    times = librosa.times_like(onset_env, sr=sr, hop_length=512)
    fig, ax = plt.subplots(nrows=2, sharex=True)
    D = np.abs(librosa.stft(y))
    librosa.display.specshow(librosa.amplitude_to_db(D, ref=np.max),
                            y_axis='log', x_axis='time', ax=ax[1])
    ax[0].plot(times, onset_env, alpha=0.8, label='Onset strength')
    ax[0].vlines(times[peaks], 0,
                onset_env.max(), color='r', alpha=0.5,
                label='Selected peaks')
    ax[0].legend(frameon=True, framealpha=0.8)
    ax[0].label_outer()

    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='Path to target file')
    args = parser.parse_args()

    find_peaks(args.f)