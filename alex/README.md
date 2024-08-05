# Exploration of Super Resolution Image Enhancement by Alexander Nishio

## Introduction
Super Resolution is an Image Enhancement Technique, where the goal is to take a low resolution image and increase its resolution to improve its quality. It is much more difficult to execute compared to the reverse operation called the downscaling task, where a large area of pixels is converted into a small area of pixels. Super Resolution is a difficult task to execute due to the limited pixels on the original image to work with and the necessity to predict and generate artificial data to create an improved image. 

**This project serves to explore different types of super-resolution models and understand the feasibility of deploying such models into laboratory systems.**

## Motivation
Super Resolution plays a critical role in various fields for restoring old images to learn more about the history of our world, analyzing satellite images to create improved maps, and analyzing microscopic organisms in medical diagnoses. As technological and scientific advancements continue to improve, there is an increase in demand for image enhancement tools: the aid of AI in enhancing images can prove to be less costly for the development of advanced microscopes, telescopes, and cameras, and can help create additional tools in aiding in scientific discoveries.

## Methods
From the research that I have collected, GAN (Generative Adversial Network) methods and Diffusion methods are the best methods for Super Resolution at the moment. The following resources were very helpful in learning about each of the methods. Feel free to check out my poster to have a rough idea on the topic or to confirm your understandings.
- **GAN**
  - [IBM's Article](https://developer.ibm.com/articles/generative-adversarial-networks-explained/#introduction-to-gans0)
  - [Computerphile's YouTube video](https://www.youtube.com/watch?v=Sw9r8CL98N0)
  - [Google's Course](https://developers.google.com/machine-learning/gan)
- **Diffusion**
  - [Computerphile's YouTube video](https://www.youtube.com/watch?v=1CIpzeNxIhU)

## Models
Real-ESRGAN and SUPIR were the two models that I found to be the best revolutionary models in each of the GAN and Diffusion Model field. Below are some resources to learn more about them
- **Real-ESRGAN (2021 GAN Model)**
  - [Official GitHub](https://github.com/xinntao/Real-ESRGAN?tab=readme-ov-file#-updates)
  - [Hugging Face Demo](https://huggingface.co/spaces/akhaliq/Real-ESRGAN)
- **SUPIR (April 2024 Diffusion Model)**
  - [Two Minute Papers Video](https://www.youtube.com/watch?v=POJ1w8H8OjY)
  - [Official GitHub](https://github.com/Fanghua-Yu/SUPIR)
  - [Hugging Face Demo](https://huggingface.co/spaces/Fabrice-TIERCELIN/SUPIR)
  - [Reddit Tutorial](https://www.reddit.com/r/StableDiffusion/comments/1b37h5z/supir_super_resolution_tutorial_to_run_it_locally/) (You have to still create a Dockerfile to run it on the Nodes)

## Future Resources for Resarch
Feel free to use the following to research improved models
 - [Two Minute Papers YouTube Channel](https://www.youtube.com/@TwoMinutePapers)
 - [Papers with Code: Super Resolution](https://paperswithcode.com/task/super-resolution/latest)
 - [Papers with Code: Image Restoration](https://paperswithcode.com/task/image-restoration/latest)
