from waggle.plugin import Plugin
from waggle.data.vision import Camera
from croniter import croniter
import logging
import os
import time
from datetime import datetime, timezone
import argparse
from transformers import AutoProcessor, AutoModelForCausalLM
import requests
import json
import resource
from PIL import Image



def limit_memory():
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS, (5 * 1024 * 1024 * 1024, soft))

limit_memory()

# Set CPU affinity to the first 4 cores
def set_cpu_affinity(cores):
    pid = os.getpid()
    os.sched_setaffinity(pid, cores)

set_cpu_affinity({0, 1})



url = ''
def sendMessage(text):
   
    headers = {'Content-type': 'application/json'}
    data = {'text': text}

    response = requests.post(url, headers=headers, data=json.dumps(data))

def readImage(imgIpt):
    #opens image if its already on the computer
    image = Image.open(f'{imgIpt}')
    image = image.convert("RGB")
    
    return image


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S')


model = AutoModelForCausalLM.from_pretrained("./Florence-2-base", local_files_only=True, trust_remote_code=True)
processor = AutoProcessor.from_pretrained("./Florence-2-base", local_files_only=True, trust_remote_code=True)

sendMessage("Just got started with the script on the node")
#takes in a task prompt and image, returns an answer 
def run_example(task_prompt, image, text_input=None):
    sendMessage("run_example 1/5")
    if text_input is None:
        prompt = task_prompt
    else:
        prompt = task_prompt + text_input
    inputs = processor(text=prompt, images=image, return_tensors="pt")
    try: 
        sendMessage("run_example 2/5")
        generated_ids = model.generate(
        input_ids=inputs["input_ids"],
        pixel_values=inputs["pixel_values"],
        max_new_tokens=1024,
        early_stopping=False,
        do_sample=False,
        num_beams=3,
        )
    except Exception as e:
        sendMessage(e)
    sendMessage("run_example 3/5")
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]
    sendMessage("run_example 4/5")
    parsed_answer = processor.post_process_generation(
        generated_text, 
        task=task_prompt, 
        image_size=(image.width, image.height)
    )
    sendMessage("run_example 5/5")
    return parsed_answer

#takes in an image (img), returns a description (string)
def generateDescription(image):
    task_prompt = '<MORE_DETAILED_CAPTION>'
    sendMessage("set task to MDC")
    description_text = run_example(task_prompt, image)
    description_text = description_text[task_prompt]

    #takes those details from the setences and finds labels and boxes in the image
    task_prompt = '<CAPTION_TO_PHRASE_GROUNDING>'
    boxed_descriptions = run_example(task_prompt, image, description_text)
    sendMessage("set task to CTPG")

    #only prints out labels not bboxes
    descriptions = boxed_descriptions[task_prompt]['labels']


    #finds other things in the image that the description did not explicitly say
    task_prompt = '<DENSE_REGION_CAPTION>'
    sendMessage("set task to DRC")
    labels = run_example(task_prompt, image)

    #only prints out labels not bboxes
    printed_labels = labels[task_prompt]['labels']
    
    description = "".join([item for sublist in [description_text, descriptions, printed_labels] for item in sublist])
    sendMessage("Made a description!")
    return description


def capture(plugin, cam, args):
    sample_file_name = "sample.jpg"
    text_file_name = "description.txt"
    sample = cam.snapshot()
    print(sample)
    sendMessage("Took a picture")
    if args.out_dir == "":
        sample.save(sample_file_name)
        img = readImage(sample_file_name)
        description = generateDescription(img)
        sendMessage("Finished making my description")
        with open(text_file_name, "w") as text_file:
            text_file.write(description)
        plugin.upload_file(sample_file_name)
        plugin.upload_file(text_file_name)
    else:
        dt = datetime.fromtimestamp(sample.timestamp / 1e9)
        base_dir = os.path.join(args.out_dir, dt.astimezone(timezone.utc).strftime('%Y/%m/%d/%H'))
        os.makedirs(base_dir, exist_ok=True)
        sample_path = os.path.join(base_dir, dt.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S%z.jpg'))
        text_path = os.path.join(base_dir, "description.txt")
        sample.save(sample_path)
        img = readImage(sample_file_name)
        description = generateDescription(img)
        sendMessage("Finished making my description")
        with open(text_path, "w") as text_file:
            text_file.write(description)
        sendMessage("Uploading")
        sendMessage(description)
        plugin.upload_file(sample_path)
        plugin.upload_file(text_path)

def run(args):
    logging.info("starting image sampler.")
    sendMessage("starting up in the run function")
    if args.cronjob == "":
        logging.info("capturing...")
        with Plugin() as plugin, Camera(args.stream) as cam:
            capture(plugin, cam, args)
        return 0

    logging.info("cronjob style sampling triggered")
    if not croniter.is_valid(args.cronjob):
        logging.error(f'cronjob format {args.cronjob} is not valid')
        return 1
    now = datetime.now(timezone.utc)
    cron = croniter(args.cronjob, now)
    with Plugin() as plugin:
        while True:
            n = cron.get_next(datetime).replace(tzinfo=timezone.utc)
            now = datetime.now(timezone.utc)
            next_in_seconds = (n - now).total_seconds()
            if next_in_seconds > 0:
                logging.info(f'sleeping for {next_in_seconds} seconds')
                time.sleep(next_in_seconds)
            logging.info("capturing...")
            with Camera(args.stream) as cam:
                capture(plugin, cam, args)
                sendMessage("Done with the run function")
    return 0


if __name__ == '__main__':
    sendMessage("In main")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-stream', dest='stream',
        action='store', default="camera", type=str,
        help='ID or name of a stream, e.g. sample')
    parser.add_argument(
        '-out-dir', dest='out_dir',
        action='store', default="", type=str,
        help='Path to save images locally in %Y-%m-%dT%H:%M:%S%z.jpg format')
    parser.add_argument(
        '-cronjob', dest='cronjob',
        action='store', default="", type=str,
        help='Time interval expressed in cronjob style')

    args = parser.parse_args()
    if args.out_dir != "":
        os.makedirs(args.out_dir, exist_ok=True)
    exit(run(args))
