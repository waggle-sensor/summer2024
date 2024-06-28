# Aristotle's 10 categories:
#(1) substance
#(2) quantity
#(3) quality
#(4) relatives
#(5) somewhere
#(6) sometime
#(7) being in a position
#(8) having
#(9) acting
#(10) being acted upon 

import requests
from PIL import Image, ImageFont, ImageDraw
import torch
import io
from transformers import BitsAndBytesConfig, pipeline
import time 
torch.cuda.empty_cache()

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

max_new_tokens = 1000

userQ = input(f"What can I help with?: \n")


aristotle = "In detail. Describe this image but place your description into Aristotle's 10 categories. Here are Aristotle's 10 categories: (1) substance; (2) quantity; (3) quality; (4) relatives; (5) somewhere; (6) sometime; (7) being in a position; (8) having; (9) acting upon; and (10) being acted upon. HerMake yours accurate to the image. And put each category on a new line. "
aristotle2 = "You are an intelligent system designed to analyze images according to Aristotle's 10 categories. Given the following image, describe the image using each of Aristotle's 10 categories: The primary entities present in this image are: ___. The number of each primary entity present is: ___. The attributes or characteristics of the primary entities are: ___. The spatial relationships between the primary entities are: ___. The location or setting of the primary entities is: ___. The temporal aspect or action occurring with the primary entities is: ___. The stance or posture of the primary entities is: ___. The primary entities possess or experience: ___. The actions performed by the primary entities are: ___. The external influences acting on the primary entities are: ___. (1) Substance: Describe the primary entities present in the image. (2) Quantity: Specify the number of each primary entity present. (3) Quality: Describe the attributes or characteristics of the primary entities. (4) Relatives: Explain the spatial relationships between the primary entities. (5) Somewhere: Describe the location or setting of the primary entities. (6) Sometime: Describe the temporal aspect or action occurring with the primary entities. (7) Being in a Position: Describe the stance or posture of the primary entities. (8) Having: Describe what the primary entities possess or experience. (9) Acting: Describe the actions performed by the primary entities. (10) Being Acted Upon: Describe the external influences acting on the primary entities."


prompt = f"USER: <image>\n You are an advanced image analysis system designed to describe images in exhaustive and incredible detail. Analyze the following image \nASSISTANT:"
outputs = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 1000})

generated_text = (outputs[0]["generated_text"])
response = generated_text[len(prompt)+2:]

print(response)

prompt = f"USER: <image>\n Here is the description of the image: {response} {aristotle2} \nASSISTANT:"
outputs = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 1000})

generated_text = (outputs[0]["generated_text"])

response = generated_text[len(prompt)+2:]

print(response)
#Describe each thing happening in this image but filter it within Aristotle's 10 categories. So put Subatance: and then list the things of substance, Quantity:  and then list the things of quantity etc Here are the 10 categories in full: (1) substance; (2) quantity; (3) quality; (4) relatives; (5) somewhere; (6) sometime; (7) being in a position; (8) having; (9) acting; and (10) being acted upon. 
"""
In detail. Describe this image but place your description into Aristotle's 10 categories. Here are Aristotle's 10 categories: (1) substance; (2) quantity; (3) quality; (4) relatives; (5) somewhere; (6) sometime; (7) being in a position; (8) having; (9) acting upon; and (10) being acted upon. HerMake yours accurate to the image. And put each category on a new line. 

Generated by ChatGPT below. (much better than mine lol)
You are an intelligent system designed to analyze images according to Aristotle's 10 categories. Given the following image, describe the image using each of Aristotle's 10 categories: Image Description: (1) Substance: Describe the primary entities present in the image. (2) Quantity: Specify the number of each primary entity present. (3) Quality: Describe the attributes or characteristics of the primary entities. (4) Relatives: Explain the spatial relationships between the primary entities. (5) Somewhere: Describe the location or setting of the primary entities. (6) Sometime: Describe the temporal aspect or action occurring with the primary entities. (7) Being in a Position: Describe the stance or posture of the primary entities. (8) Having: Describe what the primary entities possess or experience. (9) Acting: Describe the actions performed by the primary entities. (10) Being Acted Upon: Describe the external influences acting on the primary entities.
"""
