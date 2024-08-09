FROM python:3.11

RUN apt-get update -y && apt-get upgrade -y

WORKDIR /app
ADD . /app

RUN pip3 install basicsr facexlib gfpgan
RUN pip3 install --no-cache-dir -U -r ./requirements.txt

CMD ["python", "setup.py", "develop"]
CMD ["python", "inference_realesrgan.py", "-n", "RealESRGAN_x4plus", "-i", "inputs", "--face_enhance"]
