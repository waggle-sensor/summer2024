import torch
from config import *
from PIL import Image
from utils.utils import *
import torch.nn.functional as F
from trol.load_trol import load_trol
from torchvision.transforms.functional import pil_to_tensor
#Note to self: DON'T forget to add this to dockerfile: pip install sage-data-client 
import sage_data_client
#and this
import requests 
from pathlib import Path 
from fuzzywuzzy import fuzz 
import json 
import pandas as pd


#Where to store data after processing it
json_file_path = "/home/ryanrearden/gitRepos/TroL/testingImgs/data.json"

#where to store downloaded images
img_download_path = Path("/home/ryanrearden/gitRepos/TroL/testingImgs")

def download_and_store_SAGEinfo():
    url = "https://auth.sagecontinuum.org/api/v-beta/nodes/?format=json"
    response = requests.get(url)

    if response.status_code == 200:
        content = response.text
        data =json.loads(content) 

        with open("sageinfo.json", "w") as f:
            json.dump(data, f)
    
    else:
        print(f"ERROR  {response.status_code}")
    return data 

#takes in img url, login session, and where the img should be stored
def download_file(url, session, output_dir):
    try:
        response = session.get(url.strip())
        #raise HTTP error for issues
        response.raise_for_status()  

        # Extract the filename from the URL
        filename = url.strip().split('/')[-1]
        file_path = output_dir / filename

        # Write the content to a file
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f'Successfully downloaded {filename}')
        return file_path 
    except requests.exceptions.RequestException as e:
        print(f'Failed to download {url}: {e}')

#Takes in nodes. Returns df
def getData(nodes):
  return pd.concat([sage_data_client.query(
      start="2024-06-04T21:00:00.000Z",
      end="2024-06-05T03:00:00.000Z",
      filter={
          "plugin": "registry.sagecontinuum.org/theone/imagesampler:0.3.0.*",
          "vsn": node
      }
  ) for node in nodes], ignore_index=True)

#takes in the description text of the image, what the user wants to find, img path. Returns img path
def identify_element(description_text, element_to_find, threshold=80):

  # Lowercase both strings for case-insensitive matching
  description_text = description_text.lower()
  element_to_find = element_to_find.lower()

  # Check if the element is present using fuzzy matching (ratio)
  score = fuzz.ratio(description_text, element_to_find)
  if score >= threshold:
    return description_text
  else:
    return ""

#takes in a lot of node img info plus where the json file is. Adds to the json file
def jsonIT(node, focus, gps_lat, gps_lon, address, timestamp, img_path, description_text, json_file_path):
    # Keeps data JSON-friendly 
    img_path = img_path.as_posix()
    timestamp = timestamp.isoformat()

    # Create a dictionary to hold the new data
    new_data = {
        "node": node,
        "focus": focus,
        "gps_lat": gps_lat,
        "gps_lon": gps_lon,
        "address": address,
        "timestamp": timestamp,
        "image_path": img_path,
        "description": description_text
    }

    # Read and update the existing data from the JSON file
    if Path(json_file_path).exists():
        with open(json_file_path, "r+") as file:
            try:
                existing_data = json.load(file)
                if not isinstance(existing_data, list):
                    existing_data = []
            except json.JSONDecodeError:
                existing_data = []
            
            # Append the new data
            existing_data.append(new_data)

            # Move the file pointer to the beginning and truncate the file
            file.seek(0)
            file.truncate()
            json.dump(existing_data, file, indent=4)
    else:
        # If the file doesn't exist, create it and write the new data
        with open(json_file_path, "w") as file:
            json.dump([new_data], file, indent=4)

    print("JSON data appended and written")

#Gets user parameters
username = input(f"\nPlease input your username: \n")
userToken = input(f"\nPlease input your user token: \n")
#shhh this is my usertoken 

all_sage_info = download_and_store_SAGEinfo() 

#make session for later
with requests.Session() as session:
    session.auth = (username, userToken)

#gets all the data from the node
nodes = ["W026", "W07B", "W01B"]

df = getData(nodes)
print(df)
#selects the time and img link for furthur processing
time_and_imgs = (df[["timestamp", "value", "meta.vsn"]])



### This is where the LLM code begins ###

link = "TroL-3.8B" # [Select One] 'TroL-1.8B' | 'TroL-3.8B' | 'TroL-7B'

#Prompt to generate description
question = "You are an intelligent watchman overlooking the scene. Describe the objects and interactions in precise detail"

# loading model
model, tokenizer = load_trol(link=link)
    
# cpu -> gpu
for param in model.parameters():
    if not param.is_cuda:
        param.data = param.to('cuda:0')

# prompt type -> input prompt
image_token_number = None

pastnode = ""
for i in range(len(time_and_imgs['value'])):
    node = time_and_imgs['meta.vsn'][i]
    timestamp = time_and_imgs['timestamp'][i]
    img = download_file(time_and_imgs['value'][i], session, img_download_path)

    #sets the right gps and address for the node (does it once per node)
    if pastnode != node:
        focus = next((item["focus"] for item in all_sage_info if item["vsn"] == node), None)
        gps_lat = next((item["gps_lat"] for item in all_sage_info if item["vsn"] == node), None)
        gps_lon = next((item["gps_lon"] for item in all_sage_info if item["vsn"] == node), None)
        address = next((item["address"] for item in all_sage_info if item["vsn"] == node), None)
        
        pastnode = node 
    img_path= img

    # Image Load
    image = pil_to_tensor(Image.open(img_path).convert("RGB"))
    if not "3.8B" in link:
        image_token_number = 1225
        image = F.interpolate(image.unsqueeze(0), size=(490, 490), mode='bicubic').squeeze(0)
    inputs = [{'image': image, 'question': question}]

    # Generate
    with torch.inference_mode():
        _inputs = model.eval_process(inputs=inputs,
                                    data='demo',
                                    tokenizer=tokenizer,
                                    device='cuda:0',
                                    img_token_number=image_token_number)
        generate_ids = model.generate(**_inputs, max_new_tokens=512, use_cache=True)
        description_text = output_filtering(tokenizer.batch_decode(generate_ids, skip_special_tokens=False)[0], model)

    #Puts the infomration about the img into a JSON file 
    jsonIT(node, focus, gps_lat, gps_lon, address, timestamp, img_path, description_text, json_file_path)



'''
# Example usage
description_text = response 

element_to_find = "a lane for cyclist"  # Example with slightly different wording


identified_text = identify_element(description_text, element_to_find)

if identified_text:
  print("The description mentions a lane for bicycles (loose match).")
else:
  print("The description does not mention a lane for bicycles.")
'''
