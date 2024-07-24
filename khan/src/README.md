# Guide

## Directory Structure and Use

- `diagram`: Contains the long-term usage of the repository.
- `dockerfiles`: Contains the files to build containers.
- `gradio`: Contains the interface(s) along with the algorithms.
- `integrate_next`: Contains the next item(s) to integrate.
- `model_inference`: Contains the model scripts to perform inference.

## Running Files

Currently, the main components and test files are in `gradio`. These will integrate with the `model_inference` files by merging them. As a result, each Python file can be run individually.

## Media Location

LCRC contains a media folder within my folder and can be used to obtain media for testing. The media can also be replaced with any other sample as needed.

## Models Outside of Packages

The models are separate and each has its own instructions.

### For LLaVA

Install `ollama`, serve, and run the LLaVA model.

### For VILA1.5

Here are some issues that may be helpful to refer to:

- [Issue #41 on NVlabs/VILA](https://github.com/NVlabs/VILA/issues/41), about backwards compatibility fix.
- [Issue #36 on NVlabs/VILA](https://github.com/NVlabs/VILA/issues/36), about fixed torch version.
- [Issue #81 on mit-han-lab/llm-awq](https://github.com/mit-han-lab/llm-awq/issues/81), about NVCC compilation.
- [Issue #184 on mit-han-lab/llm-awq](https://github.com/mit-han-lab/llm-awq/issues/184), about missing file or directory.

This uses multiple repositories. As these repositories are out of sync, it is not suggested to use them until VILA and llm-awq are in sync due to dependency resolution issues. Use the `Dockerfile_vila1.5` if an environment is needed that is already set. However, here is how to run it:

```bash
cd integrate_next
bash vila_awq.sh
```

Below is the `vila_awq.sh` script, where `vila_launcher.sh` is inside `vila_awq.sh` and runs multiple scripts within it:

```bash
conda create -n AWQ-VILA python=3.10 -y
conda activate AWQ-VILA
pip install --upgrade pip

git clone https://github.com/NVlabs/VILA
cd VILA
pip install -e .
cd ..

git clone -b nv_laptop https://github.com/mit-han-lab/llm-awq
cd llm-awq
bash install.sh
cd vila_helper

bash download_vila.sh VILA1.5-3b-s2-AWQ

bash vila_launcher.sh VILA1.5-3b-s2-AWQ/
```

If an error occurs, manually run each script that `vila_launcher.sh` executes. Here are the commands you may need if you cannot open `vila_launcher.sh`:

```bash
python -m tinychat.serve.controller --host 0.0.0.0 --port 10000
python -m tinychat.serve.gradio_web_server --controller http://localhost:10000 --model-list-mode reload --share --auto-pad-image-token
python -m tinychat.serve.model_worker_new --host 0.0.0.0 --controller http://localhost:10000 --port 40000 --worker http://localhost:40000 --model-path <path-to-fp16-hf-model> --quant-path <path-to-awq-checkpoint>
```
