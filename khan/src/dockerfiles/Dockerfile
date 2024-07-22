# syntax=docker/dockerfile:1

FROM python:3.10.14-bullseye
RUN apt-get update && apt-get install -y \
    ffmpeg libsm6 libxext6 libhdf5-dev

WORKDIR /app
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

# Install specific PyTorch version
RUN pip install pytorch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 pytorch-cuda=11.7 -c pytorch -c nvidia

RUN pip install pywaggle[all]

RUN pip install h5py

# Fix numpy compatibility issue
RUN pip install "numpy<2"

CMD ["/bin/sh", "-c", "bash"]
