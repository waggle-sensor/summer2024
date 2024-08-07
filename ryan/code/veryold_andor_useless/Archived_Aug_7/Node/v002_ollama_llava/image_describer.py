import os
import json
import requests
import base64
from pathlib import Path
import datetime

json_file_path = "data.json"
img_dir = "./sagePhotos"

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def jsonIT(img_path, description, avg_tps, completeTime, timestamp, json_file_path):
    # Keeps data JSON-friendly 
    #img_path = img_path.as_posix()


    # Create a dictionary to hold the new data
    new_data = {
        "image": img_path,
        "description": description,
        "tokens per second": avg_tps,
        #Total time = from image to description
        "Total Time": completeTime,
        "timestamp": timestamp
  
    }

    # Read and update the existing data from the JSON file
    if Path(json_file_path).exists():
        with open(json_file_path, "r+") as f:
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
    print(f"that took {completeTime} s")

def runOllama(img_path):
     
    with open(img_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    url = 'http://localhost:11434/api/generate'

    payload = {
        "model": "llava",
        "OLLAMA-DEBUG": 1,
        "prompt": "Please describe the contents and scene of this image in detail.",
        "stream": False, 
        "images": [encoded_image]
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        response_text = []
        lines = response.text.strip().split('\n')
        last_line_data = None

        for i, line in enumerate(lines):
            json_response = json.loads(line)
            if 'response' in json_response:
                response_text.append(json_response['response'])
                if i == len(lines) - 1:
                    last_line_data = json_response

        if last_line_data:
            #try to print these but if it they are not there print zero
            total_duration_s = last_line_data.get('total_duration', 0) / 1e9
            load_duration_ms = last_line_data.get('load_duration', 0) / 1e6
            eval_count = last_line_data.get('eval_count', 0)
            eval_duration_s = last_line_data.get('eval_duration', 0) / 1e9
            eval_rate = eval_count / eval_duration_s if eval_duration_s != 0 else 0

            #zero means something went wrong
            if total_duration_s == 0:
                return "Null"
        
        return response_text, eval_rate, total_duration_s
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return "Null"

img_files = [f for f in os.listdir(img_dir) if f.endswith('.jpg')]

#takes all of the images and attempts to describe them
for file in img_files:
    img_path = os.path.join(img_dir, file)
    description, avg_tps, completeTime = runOllama(img_path)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    jsonIT(img_path, description, avg_tps, completeTime, timestamp, json_file_path)
