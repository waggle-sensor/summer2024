import io
import open_clip
import torch
from PIL import Image, ImageFont, ImageDraw
import requests
import time
from os import walk

print(f"loading files...\n\n\n")
filenames = next(walk('/home/ryanrearden/Documents/SAGE_fromLaptop/summer2024/ryan/code/scripts/SAGE/SageImgs/'), (None, None, []))[2]
print("all files loaded")

i = 0
#takes in the image and caption. Produces captioned image 
def autoCaption(image, caption_text, i):
  text_size = 40
  font = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf", text_size)

  # Get image dimensions and text width
  image_width, image_height = image.size
  text_bbox = font.getbbox(caption_text)
  text_width = text_bbox[2] - text_bbox[0]
  text_height = text_bbox[3] - text_bbox[1] 

  # Create a new image with enough height to accommodate both
  new_height = image_height + text_height + 10  # Add some padding

  new_image = Image.new("RGB", (image_width, new_height))

  # Paste the original image
  new_image.paste(image, (0, 0))

  #center the text
  text_center_x = (image_width - text_width) // 2  # Integer division for center position

  # Draw the caption text below the image with some padding
  draw = ImageDraw.Draw(new_image)
  draw.text((text_center_x, image_height + 5), caption_text, font=font, fill=(255, 255, 255))  # Adjust positioning and color

  # Save the new image with caption
  new_image.save(f"/home/ryanrearden/Documents/SAGE_fromLaptop/summer2024/ryan/code/scripts/SAGE/captioned/{i}.jpg")

  print(f"saved image {i}")

#takes in a string and returns an preprocessed image
def readImage(imgIpt):
  #a horrible hackish way to determine if its an URL or a downloaded img
  if "http" in imgIpt:
    #does URL things
    image = (f'{imgIpt}')
    # Download image data
    img_data = requests.get(image).content
    #Decode image data (no need to save)
    image = Image.open(io.BytesIO(img_data))
    image = image.convert("RGB")

  else:
    #opens image if its already on the computer
    image = Image.open(f'{imgIpt}')
    image = image.convert("RGB")
  
  #Printed to know how long it takes
  print("finished downloading image :)")
  
  return image
  



# Preprocess image for OpenClip
model, _, preprocess = open_clip.create_model_and_transforms(
  model_name="coca_ViT-B-32",
  pretrained="mscoco_finetuned_laion2b_s13b_b90k"
)

for file in filenames:
  image = readImage((f'/home/ryanrearden/Documents/SAGE_fromLaptop/summer2024/ryan/code/scripts/SAGE/SageImgs/{file}'))
  im = preprocess(image).unsqueeze(0)

  #Times the img -> text rate
  start_time = time.time()
  with torch.no_grad(), torch.cuda.amp.autocast():
    generated = model.generate(im)
  end_time = time.time()

  print(f"generated text in ", round(end_time - start_time, 2), "ish seconds")
  caption = open_clip.decode(generated[0]).split("<end_of_text>")[0].replace("<start_of_text>", "")

  i += 1
  autoCaption(image, caption, i)
