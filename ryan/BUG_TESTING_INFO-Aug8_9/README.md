# Using Florence on different GPUS

### important docker info:
These images are now available: 
- rrearden/waggleflorence:bladeT4cu116
    - takes arguments of either -url or -stream
    - If it is a URL it does not publish to the sagewebsite
    - Some URL images don't work for some reason. See blade readme for a link that does work

- rrearden/waggleflorence:plugin-capture-describe-cpu
    - Untested but should contain a fully working plugin that takes images from stream and generates a description. All of that will be published to the cloud
    - There is probably some weird issue in here. Refer to ryan/code/capture-describe-deliver/capture-and-describe-plugin/runme.sh to manually make it work on the node of your choice. 



## Jetson Nano

Failed...
core dumped probably because of pytorch

Will try to look for different version of pytorch that will be compatable. 

I isolated it down to 
```
from transformers import AutoProcessor, AutoModelForCausalLM
```
I think it may be a memory issue. The nano is so small it can't even load this in a python script.

HOW I ISOLATED IT:
```
#Code that works:
print("hi)

#code that doesn't work
from transformers import AutoProcessor, AutoModelForCausalLM
print("hi")
```
Base image of python:3.11 seems to work fine

Maybe this would help
https://benjcunningham.org/installing-transformers-on-jetson-nano.html
Maybe not though
## Jetson NX

Trying to install with the base container: nvcr.io/nvidia/l4t-pytorch:r35.2.1-pth2.0-py3
Ran into a problem:
```
AttributeError: partially initialized module 'cv2' has no attribute '_registerMatType' (most likely due to a circular import)
```
Changing to a more simplified version of the code (without waggle capturing script) to see if that changes anything

Changed to simple version. FlashAttention is only supported for CUDA 11.6 and above. We have 11.4  ...

Update: Trying shubhamgupto/jp5.1-cuda11.8-cudnn9-trt8.5

- NX: Run shubhamgupto/jp5.1-cuda11.8-cudnn9-trt8.5
    - pip in not installed with this container
         - pip fixed with apt-get install -y python3-pip
    - flash_attn module causing error "no module named packaging"
            -installed setuptools fixed the issue
        - flash_attn needs torch

## Jetson Orin

## Dell Blade 
v033
Made a script that works with GPU. Currenrly running with base image of: nvcr.io/nvidia/pytorch:24.01-py3

Accepts -steam (untested) or -url (tested). If you go the route of the url, make sure that it is an image. Some images may not work. 
I know that this one works because I tested it: https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Marmota_monax_UL_04.jpg/800px-Marmota_monax_UL_04.jpg?20130707224617

- BLADE: Make a dockerfile for Blade that runs florence
    - Blade V033 has a T4 and CUDA 11.6
    - Blade works with image: nvcr.io/nvidia/pytorch:24.01-py3
        - This image is huge. At another time, we should build an optomized image with components of this one. 


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
:) 


