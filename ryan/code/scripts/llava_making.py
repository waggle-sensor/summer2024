import requests
from PIL import Image, ImageFont, ImageDraw
import torch
import io
from transformers import BitsAndBytesConfig, pipeline
import time 

#takes in the image and caption. Produces captioned image 
def autoCaption(image, caption_text):
  text_size = 30
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
  new_image.save(f"CAPTIONED-llava-{str(int(time.time()))}.jpg")

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
  
imgIpt = input("Please input the link or full path: ")

image = readImage(imgIpt)

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16
)

model_id = "llava-hf/vip-llava-7b-hf"

pipe = pipeline("image-to-text", model=model_id, model_kwargs={"quantization_config": quantization_config})

max_new_tokens = 200

userQ = input(f"What can I help with?: \n")

#prompt = "USER: <image>\An AI, HAL, found this image because a user said: {userQ}. You are a better than HAL. Is this accurate to what the user asked? Give only yes or no as an answer\nASSISTANT:"
prompt = f"USER: <image>\n {userQ} \nASSISTANT:"
outputs = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 200})

print(outputs[0]["generated_text"])

