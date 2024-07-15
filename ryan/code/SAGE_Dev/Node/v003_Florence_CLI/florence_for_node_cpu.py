from pathlib import Path
import requests
from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM
import time 
import os 
import json

#where all of the cool info is stored
json_file_path = "data.json"

def jsonIT(img_path, description, avg_tps, completeTime, json_file_path):
    # Keeps data JSON-friendly 
    #img_path = img_path.as_posix()


    # Create a dictionary to hold the new data
    new_data = {
        "image": img_path,
        "description": description,
        "tokens per second": avg_tps,
        #Total time = from image to description
        "Total Time": completeTime,
  
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
#takes in an image url/dir returns an readable image 
def readImage(imgIpt):
    #opens image if its already on the computer
    image = Image.open(f'{imgIpt}')
    image = image.convert("RGB")
    
    return image


#takes in a task prompt and image, returns an answer 
def run_example(task_prompt, image, text_input=None):
    if text_input is None:
        prompt = task_prompt
    else:
        prompt = task_prompt + text_input
    inputs = processor(text=prompt, images=image, return_tensors="pt")
    
    start_time = time.time()  # Start timing
    generated_ids = model.generate(
      input_ids=inputs["input_ids"],
      pixel_values=inputs["pixel_values"],
      max_new_tokens=1024,
      early_stopping=False,
      do_sample=False,
      num_beams=3,
    )
    end_time = time.time()  # End timing
    
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]
    parsed_answer = processor.post_process_generation(
        generated_text, 
        task=task_prompt, 
        image_size=(image.width, image.height)
    )
    
    # Calculate tokens per second
    num_tokens = len(generated_ids[0])
    time_taken = end_time - start_time
    tokens_per_second = num_tokens / time_taken

    return parsed_answer, num_tokens, time_taken, tokens_per_second

#loads the model and processor from directory 
model = AutoModelForCausalLM.from_pretrained("./Florence-2-base", local_files_only=True, trust_remote_code=True)
processor = AutoProcessor.from_pretrained("./Florence-2-base", local_files_only=True, trust_remote_code=True)


#gets the images
image_directory = "./testphotos"

#lists the images
image_files = [f for f in os.listdir(image_directory)]

for image in image_files: 
  img_path = os.path.join(image_directory, image)
  startprogram = time.time()

  image = readImage(img_path)

  #gives a few descriptive sentences
  task_prompt = '<MORE_DETAILED_CAPTION>'
  description_text, numtokens_mdc, timetaken_mdc, tps_mdc = run_example(task_prompt, image)
  description_text = description_text[task_prompt]

  #takes those details from the setences and finds labels and boxes in the image
  task_prompt = '<CAPTION_TO_PHRASE_GROUNDING>'
  boxed_descriptions, numtokens_ctpg, timetaken_ctpg, tps_ctpg = run_example(task_prompt, image, description_text)

  #only prints out labels not bboxes
  descriptions = boxed_descriptions[task_prompt]['labels']


  #finds other things in the image that the description did not explicitly say
  task_prompt = '<DENSE_REGION_CAPTION>'
  labels, numtokens_drc, timetaken_drc, tps_drc = run_example(task_prompt, image)

  #only prints out labels not bboxes
  printed_labels = labels[task_prompt]['labels']

  #little timer just to know a little more about what is going on 
  endprogram = time.time()

  completeTime = endprogram-startprogram

  avg_tps = ((tps_mdc + tps_drc + tps_ctpg) / 3) 
  
  description = "".join([item for sublist in [description_text, descriptions, printed_labels] for item in sublist])
  #description = " ".join(description_text + descriptions + printed_labels)

  jsonIT(img_path, description, avg_tps, completeTime, json_file_path)




