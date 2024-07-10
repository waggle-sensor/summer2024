import json
import os
from PIL import Image, ImageDraw, ImageFont
import gradio as gr

def plot_bbox(image, boxes, label, font_size=50, box_width=10):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu/UbuntuMono-B.ttf", font_size)  # Use a larger font
    for bbox in boxes:
        x1, y1, x2, y2 = bbox
        draw.rectangle([x1, y1, x2, y2], outline="red", width=box_width)
        text_bbox = draw.textbbox((x1, y1), label, font=font)
        text_size = (text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1])
        text_location = [x1, y1 - text_size[1]]
        if text_location[1] < 0:
            text_location[1] = y1 + text_size[1]
        draw.rectangle([tuple(text_location), (text_location[0] + text_size[0], text_location[1] + text_size[1])], fill="red")
        draw.text((x1, y1 - text_size[1]), label, fill="white", font=font)
    return image

# Load descriptions from JSON file
data_file_path = "/home/ryanrearden/Documents/SAGE_fromLaptop/summer2024/ryan/code/SAGE_Dev/External/data.json"

if not os.path.exists(data_file_path):
    raise FileNotFoundError(f"JSON file not found: {data_file_path}")

if os.path.getsize(data_file_path) == 0:
    raise ValueError(f"JSON file is empty: {data_file_path}")

try:
    with open(data_file_path, "r") as f:
        data = json.load(f)
except json.JSONDecodeError as e:
    raise ValueError(f"Error decoding JSON file: {e}")

def search_images(search_term):
    search_terms = [term.strip().lower() for term in search_term.split(",")]
    results = []
    
    for item in data:
        image_path = item['image_path']
        matched_boxes = {}
        for term in search_terms:
            for component, boxes in item["components"].items():
                if term in component.lower():
                    if component not in matched_boxes:
                        matched_boxes[component] = []
                    matched_boxes[component].extend(boxes)
                    
        if matched_boxes:
            results.append((image_path, matched_boxes))
    
    images = []
    for img_path, matched_boxes in results:
        image = Image.open(img_path).convert("RGB")
        for label, boxes in matched_boxes.items():
            image = plot_bbox(image, boxes, label)
        images.append(image)
    return images

# Gradio interface
def gradio_search_images(search_term):
    images = search_images(search_term)
    if not images:
        return None
    return images

gr.Interface(
    fn=gradio_search_images,
    inputs="text",
    outputs=gr.Gallery(label="Results"),
    title="Image Search",
    description="Enter search terms separated by commas to find images.",
   # share=True  # Enable sharing to create a public link
).launch()
