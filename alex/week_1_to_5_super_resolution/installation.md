## Installation

*Disclaimer: I did not get very far in the building process and was not able to get the python scripts running due to not having a base image, so please refer back to the official GitHub pages respectively in the event that the code fails to run*

### Real-ESRGAN

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

To run,
```bash
sudo docker run -ti --rm real-esrgan python inference_realesrgan.py -n RealESRGAN_x4plus -i inputs --face_enhance
```

### SUPIR

**Direct download to the Docker container**

**Building the container**

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

To run,
```bash
sudo docker run -d --name supir -p 6688:6688 supir
```
open your browser and go to https://localhost:6688
