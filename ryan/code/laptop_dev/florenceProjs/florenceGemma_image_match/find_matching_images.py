import requests
from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM
import time 
import os 
import json

device = "cpu"
#takes in an image url/dir returns an readable image 
def readImage(imgIpt):
    #a horrible hackish way to determine if its an URL or a downloaded img
    if "http" in imgIpt:
      return Image.open(requests.get(imgIpt, stream=True).raw)
      
    else:
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
      generated_ids = model.generate(
        input_ids=inputs["input_ids"],
        pixel_values=inputs["pixel_values"],
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

def runOllama(user_description, image_description):
    # Define the URL of your local server
    url = 'http://localhost:11434/api/generate'

    # Define the data payload as a dictionary
    payload = {
        "model": "gemma2:latest",
        "prompt": f"The user asks {user_description} An image came back with the description: {image_description} Do you think the user would like to see the image attached to the description based on what the user wants and what the description is? If you are unsure, error on the side of no. Say ONLY True or False based on what you think"
    }

    # Send the POST request
    response = requests.post(url, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        response_text = []
        lines = response.text.strip().split('\n')

        for line in lines:
            json_response = json.loads(line)
            if 'response'  in json_response:
                response_text.append(json_response['response'])

        isValid = (''.join(response_text))

        print(isValid)
        return isValid
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return "Null"

#loads the model and processor
model = AutoModelForCausalLM.from_pretrained("microsoft/Florence-2-base", trust_remote_code=True, revision="main")
processor = AutoProcessor.from_pretrained("microsoft/Florence-2-base", trust_remote_code=True, revision="main")
#gets the images
image_directory = "/home/ryanrearden/Documents/SAGE_fromLaptop/summer2024/ryan/images/sagePhotos"

#lists the images
image_files = [f for f in os.listdir(image_directory)]

for image in image_files: 
  image = os.path.join(image_directory, image)
  startprogram = time.time()

  image = readImage(image)
  

  #gives a few descriptive sentences
  task_prompt = '<MORE_DETAILED_CAPTION>'
  description_text = run_example(task_prompt, image)
  description_text = description_text[task_prompt]

  #takes those details from the setences and finds labels and boxes in the image
  task_prompt = '<CAPTION_TO_PHRASE_GROUNDING>'
  boxed_descriptions = run_example(task_prompt, image, description_text)

  #only prints out labels not bboxes
  descriptions = boxed_descriptions[task_prompt]['labels']


  #finds other things in the image that the description did not explicitly say
  task_prompt = '<DENSE_REGION_CAPTION>'
  labels = run_example(task_prompt, image)

  #only prints out labels not bboxes
  printed_labels = labels[task_prompt]['labels']

  #little timer just to know a little more about what is going on 
  endprogram = time.time()
  print(f"Time took running the program: ", (endprogram-startprogram), " seconds\n\n")

  image_description = (description_text, descriptions, printed_labels)
  
  #prints the info 
  print(image_description)


  user_description = "Let me know when a dangerous car is on the road"
  isValid = runOllama(user_description, image_description)

  if "True" in isValid:
      image.show()




