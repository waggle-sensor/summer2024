FROM python:3.10-slim-buster

RUN apt-get update && apt-get install -y git wget
RUN apt-get -y install python3-pip

WORKDIR /app
COPY SUPIR /app/SUPIR
WORKDIR /app/SUPIR

RUN file="$(ls)" && echo $file
RUN pip install -r requirements.txt --break-system-packages

WORKDIR SUPIR

# # Download SDXL CLIP Encoder-1
# RUN git clone https://huggingface.co/openai/clip-vit-large-patch14

# # Download CLIP-ViT-bigG-14-laion2B-39B-b160k model
# RUN wget -P SDXL_CLIP https://huggingface.co/laion/CLIP-ViT-bigG-14-laion2B-39B-b160k/blob/main/open_clip_pytorch_model.bin

# # Download an SDXL model (e.g., Juggernaut)
# RUN wget -P SDXL_MODEL https://civitai.com/models/133005?modelVersionId=348913

# # Download SUPIR-v0Q and SUPIR-v0F
# RUN wget -P SUPIR_DATA https://drive.google.com/drive/folders/1yELzm5SvAi9e7kPcO_jPp2XkTs4vK6aR

# # Modify CKPT_PTH.py and SUPIR_v0.yaml for local paths
# COPY CKPT_PTH.py .
# COPY SUPIR_v0.yaml .
# RUN # add your modification commands here

CMD ["python", "gradio_demo.py", "--use_tile_vae", "--no_llava", "--use_image_slider", "--loading_half_params"]
