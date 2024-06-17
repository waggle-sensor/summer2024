import io
import open_clip
import torch
from PIL import Image
import requests

image_url = "https://static.wikia.nocookie.net/animals/images/4/4e/Liger.jpg"

# Download image data
img_data = requests.get(image_url).content

# Decode image data (no need to save)
image = Image.open(io.BytesIO(img_data))
image = image.convert("RGB")

# Preprocess image for OpenClip
model, _, transform = open_clip.create_model_and_transforms(
  model_name="coca_ViT-L-14",
  pretrained="mscoco_finetuned_laion2B-s13B-b90k"
)
im = transform(image).unsqueeze(0)

with torch.no_grad(), torch.cuda.amp.autocast():
  generated = model.generate(im)

print(open_clip.decode(generated[0]).split("<end_of_text>")[0].replace("<start_of_text>", ""))
