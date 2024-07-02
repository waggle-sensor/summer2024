import requests
from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM


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

image = input(f"Enter the image you would like to describe\n")
image = readImage(image)
model = AutoModelForCausalLM.from_pretrained("microsoft/Florence-2-base", trust_remote_code=True, revision="main").eval().cuda()
processor = AutoProcessor.from_pretrained("microsoft/Florence-2-base", trust_remote_code=True, revision="main")



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

task_prompt = '<MORE_DETAILED_CAPTION>'
description_text = run_example(task_prompt, image)
description_text = description_text[task_prompt]

#takes those details and finds labels and boxes in the image
task_prompt = '<CAPTION_TO_PHRASE_GROUNDING>'
boxed_descriptions = run_example(task_prompt, image, description_text)
#only prints out labels not bboxes
descriptions = boxed_descriptions[task_prompt]['labels']
#components_from_description = [remove_useless_phrases(label) for label in boxed_descriptions[task_prompt]['labels']]
#boxes_from_description = boxed_descriptions[task_prompt]['bboxes']

#finds other things in the image that the description did not explicitly say
task_prompt = '<DENSE_REGION_CAPTION>'
labels = run_example(task_prompt, image)
#only prints out labels not bboxes
printed_labels = labels[task_prompt]['labels']
#identified_components = [remove_useless_phrases(label) for label in labels['<DENSE_REGION_CAPTION>']['labels']]
#identified_component_boxes = labels['<DENSE_REGION_CAPTION>']['bboxes']

#puts all of the labels/boxes in a dictionary
#grouped_components = group_components(components_from_description, boxes_from_description, identified_components, identified_component_boxes)

print(description_text, descriptions, printed_labels)
