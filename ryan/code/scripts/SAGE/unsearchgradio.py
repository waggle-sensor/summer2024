import json
import matplotlib.pyplot as plt  
import matplotlib.patches as patches  
from PIL import Image
import gradio as gr

def plot_bbox(image, item, i):
    fig, ax = plt.subplots()
    ax.imshow(image)
    bbox = item['identified_component_boxes'][i]
    label = item['identified_components'][i]
    x1, y1, x2, y2 = bbox
    rect = patches.Rectangle((x1, y1), x2-x1, y2-y1, linewidth=1, edgecolor='r', facecolor='none')
    ax.add_patch(rect)
    plt.text(x1, y1, label, color='white', fontsize=8, bbox=dict(facecolor='red', alpha=0.5))
    ax.axis('off')
    plt.show()

# Load descriptions from JSON file
with open("/home/ryanrearden/Documents/SAGE_fromLaptop/summer2024/ryan/code/scripts/SAGE/SageSearch/data.json", "r") as f:
    data = json.load(f)

def search_images(search_term):
    search_terms = [term.strip().lower() for term in search_term.split(",")]
    results = []
    
    for item in data:
        image_path = item['image_path']
        image = Image.open(image_path).convert("RGB")
        for term in search_terms:
            for i, component in enumerate(item["identified_components"]):
                if term in component.lower():
                    results.append((image_path, i))
            if term in item['description'].lower():
                results.append((image_path, None))
    
    if results:
        # Display the first matching result
        img_path, bbox_index = results[0]
        image = Image.open(img_path).convert("RGB")
        if bbox_index is not None:
            plot_bbox(image, item, bbox_index)
        else:
            plt.imshow(image)
            plt.axis('off')
            plt.show()
        return img_path
    else:
        return "No matches found"

# Gradio interface
def gradio_search_images(search_term):
    img_path = search_images(search_term)
    if img_path == "No matches found":
        return None
    return img_path

gr.Interface(
    fn=gradio_search_images,
    inputs="text",
    outputs="image",
    title="Image Search",
    description="Enter search terms separated by commas to find images."
).launch()
