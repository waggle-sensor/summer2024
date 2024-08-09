# Exploration of Super Resolution Image Enhancement by Alexander Nishio

## Introduction
Super Resolution is an Image Enhancement Technique, where the goal is to take a low-resolution image and increase its resolution to improve its quality. In contrast with the reverse operation called the downscaling task, where a large area of pixels is converted into a small area of pixels, Super Resolution is a difficult task to execute: there are limited pixels on the original image to work with and the model must then predict and generate artificial data to create an improved image. 

**This project serves to explore different types of super-resolution models and understand the feasibility of deploying such models into laboratory systems.**

## Motivation
Super Resolution plays a critical role in various fields restoring old images to learn more about the history of our world, analyzing satellite images to create improved maps, and analyzing microscopic organisms in medical diagnoses. As technological and scientific advancements continue to improve, there is an increase in demand for image enhancement tools: the aid of AI in enhancing images helps play a pivotal role in decreasing the costs of developing advanced microscopes, telescopes, and cameras.

## Methods
From the research that I have collected, GAN (Generative Adversarial Network) methods and Diffusion methods are the best methods for Super Resolution at the moment. The following resources were very helpful in learning about each of the methods. Feel free to check out my sage website [here](https://github.com/kneshio/sage-website/blob/main/src/pages/science/super-resolution.md#methods) for a brief overview of the methods or to confirm your understanding.
- **GAN**
  - [IBM's Article](https://developer.ibm.com/articles/generative-adversarial-networks-explained/#introduction-to-gans0)
  - [Computerphile's YouTube video](https://www.youtube.com/watch?v=Sw9r8CL98N0)
  - [Google's Course](https://developers.google.com/machine-learning/gan)
- **Diffusion**
  - [AssemblyAI's Article](https://www.assemblyai.com/blog/how-physics-advanced-generative-ai/#generative-ai-with-thermodynamics)
  - [Computerphile's YouTube video](https://www.youtube.com/watch?v=1CIpzeNxIhU)

## Models
Real-ESRGAN and SUPIR were the two models that I found to be the best revolutionary models in each of the GAN and Diffusion Model fields. Below are some resources to learn more about them and how to implement them into systems.

For comprehensive results on each of the models, feel free to check out my sage website [here](https://github.com/kneshio/sage-website/blob/main/src/pages/science/super-resolution.md#results).

- **Real-ESRGAN (July 2021 GAN Model)**
  - [Official GitHub](https://github.com/xinntao/Real-ESRGAN)
  - [Paper](https://arxiv.org/abs/2107.10833)
  - [Hugging Face Demo](https://huggingface.co/spaces/akhaliq/Real-ESRGAN)
  - [Other Links](https://github.com/xinntao/Real-ESRGAN?tab=readme-ov-file#-real-esrgan-training-real-world-blind-super-resolution-with-pure-synthetic-data)
- **SUPIR (January 2024 Diffusion Model)**
  - [Official GitHub](https://github.com/Fanghua-Yu/SUPIR)
  - [Paper](https://arxiv.org/abs/2401.13627)
  - [Two Minute Papers Video](https://www.youtube.com/watch?v=POJ1w8H8OjY)
  - [Hugging Face Demo](https://huggingface.co/spaces/Fabrice-TIERCELIN/SUPIR) (*Currently down due to Updated GitHub*)
  - [Reddit Tutorial](https://www.reddit.com/r/StableDiffusion/comments/1b37h5z/supir_super_resolution_tutorial_to_run_it_locally/)   (*Might not need because of Updated GitHub Instructions*)
  - [Other Links](https://github.com/Fanghua-Yu/SUPIR?tab=readme-ov-file#cvpr2024-scaling-up-to-excellence-practicing-model-scaling-for-photo-realistic-image-restoration-in-the-wild)

## Installation

*Disclaimer: I did not get very far in the building process and was not able to get the python scripts running due to not having a base image, so please refer back to the official GitHub pages respectively in the event that the code fails to run*

### Real-ESRGAN

**Direct download to the Docker container**

**Building the container**

1. Clone the official Real-ESRGAN repository
   
   ```
   git clone https://github.com/xinntao/Real-ESRGAN.git
   cd Real-ESRGAN
   ```

2. Download the Dockerfile [here](https://github.com/kneshio/summer2024/tree/main/alex/week_1_to_5_super_resolution/real-esrgan) and place it in the Real-ESRGAN folder

3. Build the docker container
   
    ```
    sudo docker build . -t real-esrgan
    sudo docker run --gpus all -it real-esrgan
    ```

**Usage**

### SUPIR

1. Clone the official SUPIR repository
   
   ```
   git clone https://github.com/Fanghua-Yu/SUPIR.git
   cd SUPIR
   ```

2. Download the Dockerfile [here](https://github.com/kneshio/summer2024/tree/main/alex/week_1_to_5_super_resolution/supir) and place it in the Real-ESRGAN folder
   
3. Download Models (referenced from [reddit](https://www.reddit.com/r/StableDiffusion/comments/1b37h5z/supir_super_resolution_tutorial_to_run_it_locally/) page)

   1. Download SDXL CLIP Encoder-1: ```git clone https://huggingface.co/openai/clip-vit-large-patch14```
   2. Download https://huggingface.co/laion/CLIP-ViT-bigG-14-laion2B-39B-b160k/blob/main/open_clip_pytorch_model.bin (just this one file)
   3. Download a (Juggernaut) SDXL model (https://civitai.com/models/133005?modelVersionId=348913 ) No Lightning or LCM
   4. Skip LLaVA Stuff (saves memory)
   5. Download SUPIR-v0Q (https://drive.google.com/drive/folders/1yELzm5SvAi9e7kPcO_jPp2XkTs4vK6aR?usp=sharing)
   6. Download SUPIR-v0F (https://drive.google.com/drive/folders/1yELzm5SvAi9e7kPcO_jPp2XkTs4vK6aR?usp=sharing)
   7. Modify CKPT_PTH.py for the local paths for the SDXL CLIP files you downloaded (directory for CLIP1 and .bin file for CLIP2)
   8. Modify SUPIR_v0.yaml for local paths for the other files you downloaded, at the end of the file, SDXL_CKPT, SUPIR_CKPT_F, SUPIR_CKPT_Q (file location for all 3)

4. Build the docker container
   
    ```
    sudo docker build . -t supir
    sudo docker run --gpus all -it supir
    ```

**Usage**

## Future Resources for Research
Feel free to use the following to research improved models
 - [Two Minute Papers YouTube Channel](https://www.youtube.com/@TwoMinutePapers)    (*Best Link to start*)
 - [Papers with Code: Super Resolution](https://paperswithcode.com/task/super-resolution/latest)
 - [Papers with Code: Image Restoration](https://paperswithcode.com/task/image-restoration/latest)
