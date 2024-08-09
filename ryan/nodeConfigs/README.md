# Using Florence on different GPUS


## Jetson Nano

Failed...
core dumped probably because of pytorch

Will try to look for different version of pytorch that will be compatable. 



## Jetson NX

Trying to install with the base container: nvcr.io/nvidia/l4t-pytorch:r35.2.1-pth2.0-py3
Ran into a problem:
```
AttributeError: partially initialized module 'cv2' has no attribute '_registerMatType' (most likely due to a circular import)
```
Changing to a more simplified version of the code (without waggle capturing script) to see if that changes anything

Changed to simple version. FlashAttention is only supported for CUDA 11.6 and above. We have 11.4  ...

Update: Trying shubhamgupto/jp5.1-cuda11.8-cudnn9-trt8.5

## Jetson Orin

## Dell Blade 
v033
Made a script that works with GPU. Currenrly running with base image of: nvcr.io/nvidia/pytorch:24.01-py3

Accepts -steam (untested) or -url (tested). If you go the route of the url, make sure that it is an image. Some images may not work. 
I know that this one works because I tested it: https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Marmota_monax_UL_04.jpg/800px-Marmota_monax_UL_04.jpg?20130707224617

### Strange CUDA problem 
There was a strange problem with pytorch and CUDA. If you ran 
```
sudo docker run --gpus all NAME -url URL  
```
Then it didn't work and said the CUDA version was too old

But if you ran
```
sudo docker run -it --gpus all --entrypoint NAME /bin/bash
* you are now in the container *
python3 app.py
```
Then it did work

Special thanks for Yufeng for pointing out there may be a difference in the /bin/bash python and the python the container normally wants to run. That ended up being the issue. 
The dockerfile entry point is now 
```
ENTRYPOINT ["/bin/bash", "/app/start.sh"]
```
with start.sh being
```
exec python3 /app/app.py "$@"
```

That did the trick

## TODO log 


- NX: Run shubhamgupto/jp5.1-cuda11.8-cudnn9-trt8.5
    - pip in not installed with this container
         - pip fixed with apt-get install -y python3-pip
    - flash_attn module causing error "no module named packaging"
            -installed setuptools fixed the issue
        - flash_attn needs torch

- BLADE: Make a dockerfile for Blade that runs florence
    - Blade V033 has a T4 and CUDA 11.6
    - Blade works with image: nvcr.io/nvidia/pytorch:24.01-py3
        - This image is huge. At another time, we should build an optomized image with components of this one. 

