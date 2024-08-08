import requests
from PIL import Image
import torch
from transformers import AutoProcessor, AutoModelForCausalLM
import time 
import os 


device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32


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
      inputs = processor(text=prompt, images=image, return_tensors="pt").to(device)
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


#loads the model and processor
model = AutoModelForCausalLM.from_pretrained("./Florence-2-base", local_files_only=True, trust_remote_code=True).to(device)
processor = AutoProcessor.from_pretrained("./Florence-2-base", local_files_only=True, trust_remote_code=True)

#gets the images
image_directory = "/app/testphotos"

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

  #prints the info 
  print(description_text, descriptions, printed_labels)



