import json
import os
from PIL import Image, ImageDraw, ImageFont
import gradio as gr



def plot_bbox(image, item, i):
    draw = ImageDraw.Draw(image)
    bbox = item['identified_component_boxes'][i]
    label = item['identified_components'][i]
    x1, y1, x2, y2 = bbox

    # Increase box width
    box_width = 10  # Adjust this value for desired box thickness

    # Use a larger font
    font = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu/UbuntuMono-B.ttf", 50)  # Change font name and size as needed

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
data_file_path = "/home/ryanrearden/Documents/SAGE_fromLaptop/summer2024/ryan/code/scripts/SAGE/SageSearch/data.json"

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
        for term in search_terms:
            for i, component in enumerate(item["identified_components"]):
                if term in component.lower():
                    results.append((image_path, item, i))
            if term in item['description'].lower():
                results.append((image_path, item, None))
    
    images = []
    for img_path, item, bbox_index in results:
        image = Image.open(img_path).convert("RGB")
        if bbox_index is not None:
            image = plot_bbox(image, item, bbox_index)
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
).launch()
