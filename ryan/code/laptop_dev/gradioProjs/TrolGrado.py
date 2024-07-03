import json
import re
import cv2
import torch
from config import *
from utils.utils import *
from trol.load_trol import load_trol
import gradio as gr
from pathlib import Path  

JSON_path = '/home/ryanrearden/gitRepos/TroL/testingImgs/data.json'

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

def show_image(image_path, max_width=800, max_height=600):
    img = cv2.imread(image_path)
    height, width = img.shape[:2]
    scale_factor = min(max_width / width, max_height / height, 1)
    if scale_factor < 1:
        resized_width = int(width * scale_factor)
        resized_height = int(height * scale_factor)
        img = cv2.resize(img, (resized_width, resized_height))
    resized_image_path = f"/tmp/resized_{Path(image_path).name}"
    cv2.imwrite(resized_image_path, img)
    return resized_image_path

# Load model
link = "TroL-3.8B"
model, tokenizer = load_trol(link=link)
for param in model.parameters():
    if not param.is_cuda:
        param.data = param.to('cuda:0')

def find_matching_images(prompt):
    results = []
    prompt = preprocess_text(prompt)

    with open(JSON_path, 'r') as file:
        data = json.load(file)

    for entry in data:
        description = preprocess_text(entry['description'])
        question = f"Based on this information: {description}, is the following in the given information: {prompt}. Return 1 for yes and 0 for no. DO NOT SAY ANYTHING ELSE."
        inputs = [{'question': question}]
        with torch.inference_mode():
            _inputs = model.eval_process(inputs=inputs, data='demo', tokenizer=tokenizer, device='cuda:0', img_token_number=None)
            generate_ids = model.generate(**_inputs, max_new_tokens=256, use_cache=True)
            response = output_filtering(tokenizer.batch_decode(generate_ids, skip_special_tokens=False)[0], model)
        if response == "1":
            results.append(entry)
    
    if results:
        images = [show_image(result["image_path"]) for result in results]
        descriptions = [result["description"] for result in results]
        return descriptions, images
    else:
        return "No matching entries found.", []

# Create the Gradio interface
interface = gr.Interface(
    fn=find_matching_images,
    inputs=gr.Textbox(lines=2, placeholder="Enter your prompt here..."),
    outputs=[gr.Textbox(label="Descriptions"), gr.Gallery(label="Images")],
    title="Image Search Based on Text Prompt",
    description="Enter a text prompt to find matching images."
)

interface.launch()
