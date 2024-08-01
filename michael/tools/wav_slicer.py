# Split large wav files into smaller segments.

import os
import argparse
import random
from pydub import AudioSegment


def split_wav_file(input_file, output_dir, min_duration=3, max_duration=30):
    audio = AudioSegment.from_wav(input_file)
    total_duration = len(audio)
    
    start = 0
    counter = 0
    
    while start < total_duration:
        segment_duration = random.randint(min_duration * 1000, max_duration * 1000)
        end = min(start + segment_duration, total_duration)
        
        segment = audio[start:end]

        output_filename = f'{os.path.splitext(os.path.basename(input_file))[0]}_{counter:04d}.wav'
        output_path = os.path.join(output_dir, output_filename)
        
        segment.export(output_path, format="wav")
        start = end
        counter += 1


def process_directory(input_dir, output_dir, min_duration=3, max_duration=30):
    os.makedirs(output_dir, exist_ok=True)
    
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.wav'):
            input_path = os.path.join(input_dir, filename)
            split_wav_file(input_path, output_dir, min_duration, max_duration)
            print(f'{input_path} processed successfully')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='Path to a single WAV file')
    parser.add_argument('-d', help='Path to a directory of WAV files')
    parser.add_argument('-o', help='Path to desired output directory')
    parser.add_argument('--min', type=int, default=10, help='Minimum duration of slices in seconds')
    parser.add_argument('--max', type=int, default=30, help='Maximum duration of slices in seconds')
    args = parser.parse_args()
    
    if args.f:
        split_wav_file(args.f, args.o)
    elif args.d:
        process_directory(args.d, args.o)
