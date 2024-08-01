import os
from inference.process_wav import separate
from tools.peak_slice import process_directory

raw_input_dir = '/app/data/demo',  # field recordings
artifacts_dir = '/app/data/artifacts',  # output  
model_dir = '/app/models/bird_mixit_model_checkpoints/output_sources8',
checkpoint_id = '2178900',
num_sources = 8,
delta = 0.85,  # sensitivity for detecting peaks
slice_duration = 25  # length in seconds for trimming around peaks


if __name__ == '__main__':
    peaks_dir = f'{artifacts_dir}/peaks'
    process_directory(input_dir=raw_input_dir, output_dir=peaks_dir)

    # separation inference on each peak
    for filename in os.listdir(peaks_dir):
        path = os.path.join(peaks_dir, filename)
        output_path = f'{output_dir}/separated/{filename.replace(".wav", "")}/{filename}'

        separate(input=path, 
                output=output_path,
                model_dir=model_dir,
                checkpoint=f'{model_dir}/model.ckpt-{checkpoint_id}',
                num_sources=num_sources)

        print(f'\nRan inference on {filename} successully. Check {output_path} for results.')
