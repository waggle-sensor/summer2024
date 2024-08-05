import os
import argparse
import numpy as np
from pydub import AudioSegment
import soundfile as sf
import librosa


def split_large_files(wav, output_dir, max_duration=60*20):
    """Splits large input files into smaller segments, to reduce memory load"""

    os.makedirs(output_dir, exist_ok=True)
    
    max_duration *= 1000  # convert to ms
    audio = AudioSegment.from_wav(wav)
    total_duration = len(audio)

    if total_duration <= max_duration:
        return [wav]

    num_chunks = int(np.ceil(total_duration / max_duration))
    chunks = []

    for i in range(num_chunks):
        start = i * max_duration
        end = min((i + 1) * max_duration, total_duration)
        
        chunk = audio[start:end]
        chunk_file = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(wav))[0]}.{i + 1}.wav")
        chunk.export(chunk_file, format="wav")
        chunks.append(chunk_file)
    
    return chunks


def find_peaks_and_slice(wav, output_dir, delta=0.75, slice_duration=25, max_duration=60*20):
    """Calculates notable audio events in input file(s), and saves slices to output_dir
       See https://librosa.org/doc/latest/generated/librosa.util.peak_pick.html
    """

    wavs = split_large_files(wav, output_dir, max_duration)
    
    for chunk in wavs:
        print(f'\nProcessing chunk {chunk}')
        y, sr = librosa.load(chunk)
        onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=512, aggregate=np.median)
        peaks = librosa.util.peak_pick(onset_env, pre_max=3, post_max=3, pre_avg=3, post_avg=5, delta=delta, wait=10)
        times = librosa.times_like(onset_env, sr=sr, hop_length=512)
        last_end_time = 0

        for i, peak in enumerate(peaks):
            peak_time = times[peak]
            start_time = max(0, peak_time - slice_duration / 2)
            end_time = min(y.shape[0] / sr, peak_time + slice_duration / 2)

            # prevent overlap with the previous slice
            if start_time < last_end_time:
                continue

            start_sample = int(start_time * sr)
            end_sample = int(end_time * sr)

            # save slice to new file
            slice_y = y[start_sample:end_sample]
            output_file = os.path.join(output_dir, f"{os.path.basename(chunk).replace('.wav', '')}.{i+1}.wav")
            sf.write(output_file, slice_y, sr)
            print(f"Saved {output_file}")

            last_end_time = end_time

        # Remove the intermediary chunks after processing, if applicable
        if chunk != wav:
            os.remove(chunk)


def process_directory(input_dir, output_dir, delta=0.75, slice_duration=25, max_duration=60*20):
    """Process all wav files in a directory"""
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.wav'):
            input_path = os.path.join(input_dir, filename)
            find_peaks_and_slice(input_path, output_dir, delta, slice_duration, max_duration)
            print(f'{input_path} processed successfully')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, help='Path to a single input wav file')
    parser.add_argument('-d', '--dir', type=str, help='Path to input directory')
    parser.add_argument('-o', '--output_dir', type=str, default='peaks', help='Path to output directory')
    parser.add_argument('--delta', type=float, default=0.75, help='Sensitivity of the peak-finding algorithm')
    parser.add_argument('--slice_duration', type=int, default=25, help='Length of output slices in seconds')
    parser.add_argument('--max', type=int, default=20, help='Length in minutes for chunking')
    args = parser.parse_args()

    if args.dir:
        process_directory(args.dir, args.output_dir, args.delta, args.slice_duration, max_duration=60*args.max)
    elif args.file:
        find_peaks_and_slice(args.file, args.output_dir, args.delta, args.slice_duration, max_duration=60*args.max)
    else:
        print(parser.parse_args(['-h']))
