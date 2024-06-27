from transformers import AutoProcessor, AutoModelForCausalLM  
from PIL import Image
import requests
import matplotlib.pyplot as plt  
import matplotlib.patches as patches  
import pandas as pd
from pathlib import Path 
import json
import sage_data_client


model_id = 'microsoft/Florence-2-base'
model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True).eval().cuda()
processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)


#Where to store data after processing it
json_file_path = "/home/ryanrearden/Documents/SAGE_fromLaptop/summer2024/ryan/code/scripts/SAGE/SageSearch/data.json"

#where to store downloaded images
img_download_path = Path("/home/ryanrearden/Documents/SAGE_fromLaptop/summer2024/ryan/code/scripts/SAGE/SageSearch/moreSagePics")

#grabs other node info
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
      start="2024-06-04T18:00:00.000Z",
      end="2024-06-05T09:00:00.000Z",
      filter={
          "plugin": "registry.sagecontinuum.org/theone/imagesampler:0.3.0.*",
          "vsn": node
      }
  ) for node in nodes], ignore_index=True)

#takes in a lot of node img info plus where the json file is. Adds to the json file
def jsonIT(node, focus, gps_lat, gps_lon, address, timestamp, img_path, description_text, identified_components, identified_component_boxes, json_file_path):
    # Keeps data JSON-friendly 
    img_path = img_path.as_posix()
    timestamp = timestamp.isoformat()

    # Create a dictionary to hold the new data
    new_data = {
        "node": node,
        "timestamp": timestamp,
        "image_path": img_path, 
        "focus": focus,
        "gps_lat": gps_lat,
        "gps_lon": gps_lon,
        "address": address,
        "identified_components": identified_components, 
        "identified_component_boxes": identified_component_boxes,
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

def run_example(task_prompt, image, text_input=None):
    if text_input is None:
        prompt = task_prompt
    else:
        prompt = task_prompt + text_input
    inputs = processor(text=prompt, images=image, return_tensors="pt")
    generated_ids = model.generate(
      input_ids=inputs["input_ids"].cuda(),
      pixel_values=inputs["pixel_values"].cuda(),
      max_new_tokens=1024,
      early_stopping=False,
      do_sample=False,
      num_beams=3,
    )
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]
    parsed_answer = processor.post_process_generation(
        generated_text, 
        task=task_prompt, 
        image_size=(image.width, image.height)
    )

    return parsed_answer

def readImage(imgIpt):
  #a horrible hackish way to determine if its an URL or a downloaded img
  if "http" in imgIpt:
    return Image.open(requests.get(imgIpt, stream=True).raw)
    

  else:
    #opens image if its already on the computer
    image = Image.open(f'{imgIpt}')
    image = image.convert("RGB")
  
  #Printed to know how long it takes
  print("finished downloading image :)")
  
  return image

def plot_bbox(image, data):
   # Create a figure and axes  
    fig, ax = plt.subplots()  
      
    # Display the image  
    ax.imshow(image)  
      
    # Plot each bounding box  
    for bbox, label in zip(data['bboxes'], data['labels']):  
        # Unpack the bounding box coordinates  
        x1, y1, x2, y2 = bbox  
        # Create a Rectangle patch  
        rect = patches.Rectangle((x1, y1), x2-x1, y2-y1, linewidth=1, edgecolor='r', facecolor='none')  
        # Add the rectangle to the Axes  
        ax.add_patch(rect)  
        # Annotate the label  
        plt.text(x1, y1, label, color='white', fontsize=8, bbox=dict(facecolor='red', alpha=0.5))  
      
    # Remove the axis ticks and labels  
    ax.axis('off')  
      
    # Show the plot  
    plt.show()  

def remove_useless_phrases(label):
  #Florence likes to use these phrases but they are not needed
  #No one cares florence -- sorry 
  useless_phrases = ["at night", "CCTV footage of", "CCTV image of", "CCTV camera of", "CCTV surveillance image of"]
  for phrase in useless_phrases:
    if phrase in label:
      label = label.replace(phrase, "")
      #removes space at start if it gets messed up
      if label[0] == " ":
         label = label[1:]
  return label


#Gets user parameters
username = input(f"\nPlease input your username: \n")
userToken = input(f"\nPlease input your user token: \n")
#shhh this is my usertoken 
print("Don't foget to add your usertoken ")
all_sage_info = download_and_store_SAGEinfo() 

#make session for later
with requests.Session() as session:
    session.auth = (username, userToken)

#gets all the data from the node
nodes = ["W026", "W07B", "W07A", "W01B"]

df = getData(nodes)
print(df)
#selects the time and img link for furthur processing
time_and_imgs = (df[["timestamp", "value", "meta.vsn"]])


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

    image = Image.open(img_path).convert("RGB")
    task_prompt = '<MORE_DETAILED_CAPTION>'
    description_text = run_example(task_prompt, image)
    description_text = description_text[task_prompt]

    labels = run_example('<DENSE_REGION_CAPTION>', image)


    identified_components = [remove_useless_phrases(label) for label in labels['<DENSE_REGION_CAPTION>']['labels']]
    identified_component_boxes = labels['<DENSE_REGION_CAPTION>']['bboxes']

    jsonIT(node, focus, gps_lat, gps_lon, address, timestamp, img_path, description_text, identified_components, identified_component_boxes, json_file_path)
