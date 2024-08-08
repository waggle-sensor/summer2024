# Using Florence on different GPUS

## Jetson Nano

## Jetson NX

Trying to install with the base container: nvcr.io/nvidia/l4t-pytorch:r35.2.1-pth2.0-py3
Ran into a problem:
```
AttributeError: partially initialized module 'cv2' has no attribute '_registerMatType' (most likely due to a circular import)
```
Changing to a more simplified version of the code (without waggle capturing script) to see if that changes anything

Changed to simple version. FlashAttention is only supported for CUDA 11.6 and above. We have 11.4  ...

## Jetson Orin