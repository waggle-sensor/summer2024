FROM nvcr.io/nvidia/tensorflow:23.02-tf2-py3

RUN apt-get update -y && apt-get upgrade -y

WORKDIR /app
ADD . /app

RUN pip3 install immutabledict argparse librosa soundfile pydub 

ENTRYPOINT [ "/bin/bash" ]