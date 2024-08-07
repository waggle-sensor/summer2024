import cv2 
from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM
#where all of the cool info is stored
from waggle.plugin import Plugin
from waggle.data.vision import Camera
TOPIC_TEMPLATE = "Sage Search"

#loads the model and processor from directory 
model = AutoModelForCausalLM.from_pretrained("./Florence-2-base", local_files_only=True, trust_remote_code=True)
processor = AutoProcessor.from_pretrained("./Florence-2-base", local_files_only=True, trust_remote_code=True)


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
    
    # Calculate tokens per second



    return parsed_answer

def readImage(imgIpt):
    #opens image if its already on the computer
    image = Image.open(f'{imgIpt}')
    image = image.convert("RGB")
    
    return image


def run(args):
    with Plugin() as plugin, Camera(args.stream) as camera:
        for sample in camera.stream():
            frame = sample.data
            image = readImage(frame)
            #gives a few descriptive sentences
            task_prompt = '<MORE_DETAILED_CAPTION>'
            description_text, numtokens_mdc, timetaken_mdc, tps_mdc = run_example(task_prompt, image)
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
            
            description = "".join([item for sublist in [description_text, descriptions, printed_labels] for item in sublist])

            
            sample.data = frame
            sample.save(f'sample.jpg')
            plugin.upload_file(f'sample.jpg', timestamp=sample.timestamp)
            plugin.publish(f'{TOPIC_TEMPLATE}',description, timestamp=sample.timestamp)




