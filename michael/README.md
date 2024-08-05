# SULI 2024 Michael Szostak


## Setup 
1. Clone the repository
```
git clone https://github.com/waggle-sensor/summer2024
cd summer2024/michael/
```

2. Once you have access to the `bebop.lcrc.anl.gov` server, download the datasets and model checkpoints with:

```
scp -r lcrc:/lcrc/project/waggle/summer_projects/summer2024/michael_szostak/data ./
scp -r lcrc:/lcrc/project/waggle/summer_projects/summer2024/michael_szostak/models ./
```

Make sure to unzip each dataset as well. More information describing the FUSS data and how it is used can be found [here](https://github.com/google-research/sound-separation/blob/master/datasets/fuss/FUSS_license_doc/README.md).  


3. Build and run the container:
```
sudo docker build . -t sound-separation
sudo docker run --gpus all -it sound-separation
```

Alternatively, I often found it helpful to mount a persistent, shared filesystem between the container and the host:
```
sudo docker run --gpus all -v </host/path/>:</container/path/> -it sound-separation
```

Building on a wild node (as opposed to a Dell Blade) will likely require changes to the Dockerfile to ensure compatible versions of Python and CUDA.


## Usage
### Running Inference
CLI example with 8-source model:
```
python3 inference/process_wav.py
    -m models/bird_mixit_model_checkpoints/output_sources8/
    -c models/bird_mixit_model_checkpoints/output_sources8/model-ckpt-2178900
    -ns 8
    -i /path/to/input.wav
    -o /path/to/output.wav
```

I also made changes to the [original script](https://github.com/google-research/sound-separation/blob/master/models/tools/process_wav.py) that allow for using it as part of a larger program instead:

```python
from inference.process_wav import separate

separate(input=input_wav, 
        output=output_wav,
        model_dir=model_dir,
        checkpoint=f'{model_dir}/model.ckpt-{checkpoint_id}',
        num_sources=num_sources)
```

### Training
#### FUSS
```
python3 sound-separation/models/neurips2020_mixit/train_model_on_fuss.py 
	-dd data/STUDY
	-md model_data/
```

#### Perch
```
python3 chirp/projects/main.py
	--config=path/to/my_separator_config.py
	--workdir=/path/to/save/checkpoints 
	--target=separator 
	--mode=train
```
Note that the Perch codebase is not included in this repository, it can instead be found [here](https://github.com/google-research/perch). 
Training datasets for Perch must be built with [TFDS](https://www.tensorflow.org/datasets/overview).


### Other tools
#### `get_spectrogram.py` and `get_spectrogram_peaks.py`
Uses `librosa` and `matplotlib` to compute and display spectrograms of a recording.

```
python3 tools/get_spectrogram.py -f </path/to/input.wav>
python3 tools/get_spectrogram.py -f </path/to/input.wav>
```


#### `peak_slice.py`
Uses the algorithm from `get_spectrogram_peaks.py` to preprocess a dataset, minimizing the amount of background noise present in recordings. Use `-h` or no arguments for how to use. 


#### `birdnet_classify.py`
This script was copied from the [BirdNET](https://github.com/kahst/BirdNET) documentation. It provides an approach for classifying bird species present in a recording. Note that it requires Python >= 3.9, which is not included in the Docker container by default. Usage is otherwise identical to `get_spectrogam.py`.
