'''
The purpose of this program is to find images that match a user's text prompt
It will use some sort of algorithm to perform the search. 
'''
import json
import re
import cv2 
import torch
from config import *
from utils.utils import *
from trol.load_trol import load_trol


JSON_path = '/home/ryanrearden/gitRepos/TroL/testingImgs/data.json'
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

def show_image(image_path, max_width=800, max_height=600):
  """Displays an image using OpenCV, with a maximum window size"""
  img = cv2.imread(image_path)

  # Get image dimensions and calculate scaling factor if needed
  height, width = img.shape[:2]
  scale_factor = min(max_width / width, max_height / height, 1)  # Limit scaling to 1 (no scaling)

  if scale_factor < 1:  # If image is larger than max size
      # Resize image to fit within max window dimensions
      resized_width = int(width * scale_factor)
      resized_height = int(height * scale_factor)
      img = cv2.resize(img, (resized_width, resized_height))

  # Display the image
  cv2.imshow('Search Result', img)
  cv2.waitKey(0)  # Wait for a key press to close the window
  cv2.destroyAllWindows()

results = []

# model selection
link = "TroL-3.8B" # [Select One] 'TroL-1.8B' | 'TroL-3.8B' | 'TroL-7B'
# loading model
model, tokenizer = load_trol(link=link)
# User prompt
prompt_type="text_only" # Select one option "text_only", "with_image"
# cpu -> gpu
for param in model.parameters():
    if not param.is_cuda:
        param.data = param.to('cuda:0')

prompt = input(f"Please input what you are looking for: \n")

# Load the JSON file
with open(JSON_path, 'r') as file:
    data = json.load(file)

# Preprocess the descriptions
for entry in data:
    entry['description'] = preprocess_text(entry['description'])
    description = entry['description']


    question=f"Based on this information: {description}, is the following in the given information: {prompt}. Return 1 for yes and 0 for no. DO NOT SAY ANYTHING ELSE."
    inputs = [{'question': question}]

    # Generate

    with torch.inference_mode():
        _inputs = model.eval_process(inputs=inputs,
                                    data='demo',
                                    tokenizer=tokenizer,
                                    device='cuda:0',
                                    img_token_number=None)
        generate_ids = model.generate(**_inputs, max_new_tokens=256, use_cache=True)
        response = output_filtering(tokenizer.batch_decode(generate_ids, skip_special_tokens=False)[0], model)


    print(response)
    if response == "1":
        results.append(entry)
    



if results:
    print("Found the following entries:")
    for result in results:
        print(result["description"])
        image_path = result["image_path"]
        show_image(image_path)

else:
    print("No matching entries found.")

