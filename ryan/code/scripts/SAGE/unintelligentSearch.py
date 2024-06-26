import json
import matplotlib.pyplot as plt  
import matplotlib.patches as patches  
import os
from PIL import Image


def plot_bbox(image, item, i):
    #image = Image.open(image).convert("RGB")
   # Create a figure and axes  
    fig, ax = plt.subplots()  
      
    # Display the image  
    ax.imshow(image)  
      
    # Plot each bounding box  
    bbox = item['identified_component_boxes'][i]
    label = item['identified_components'][i]
    # Unpack the bounding box coordinates  
    x1, y1, x2, y2 = bbox  
    # Create a Rectangle patch  
    rect = patches.Rectangle((x1, y1), x2-x1, y2-y1, linewidth=1, edgecolor='r', facecolor='none')  
    # Add the rectangle to the Axes  
    ax.add_patch(rect)  
    # Annotate the label  
    plt.text(x1, y1, label, color='white', fontsize=8, bbox=dict(facecolor='red', alpha=0.5))  
      
    # Remove the axis ticks and labels  
    ax.axis('off')  
      
    # Show the plot  
    plt.show()  

# Load descriptions from JSON file
with open("/home/ryanrearden/Documents/SAGE_fromLaptop/summer2024/ryan/code/scripts/SAGE/SageSearch/data.json", "r") as f:
    data = json.load(f)

# Preprocess descriptions and get embeddings
search_term = input("Please input the search term you are looking for separated by a comma: ")
search_terms = [term.strip().lower() for term in search_term.split(",")]

for item in data:
    image = Image.open(item['image_path']).convert("RGB")
    for term in search_terms:
        for (i, component) in enumerate(item["identified_components"], start = 0):
            if (term in component.lower()):
                print(component)
                plot_bbox(image, item, i)
        if term in item['description']:
            plt.imshow(image) 
            plt.show()



