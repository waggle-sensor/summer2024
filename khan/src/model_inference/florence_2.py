import torch
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import gradio as gr
from transformers import AutoProcessor, AutoModelForCausalLM
from PIL import Image


model_id = 'microsoft/Florence-2-base'
model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True).eval().cuda()
processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)

def process_image(image):
    # tokenize image
    inputs = processor(image, return_tensors='pt', padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    # extract information
    captions = processor.decode(outputs.logits.argmax(dim=-1))
    # sample bounding box coordinates
    bbox_coords = [(100, 100, 200, 200), (300, 300, 400, 400)]

    for x1, y1, x2, y2 in bbox_coords:
        rect = patches.Rectangle((x1, y1), x2 - x1, y2 - y1, linewidth=1, edgecolor='r', facecolor='none')
        plt.gca().add_patch(rect)
    plt.imshow(image)
    plt.axis('off')
    plt.show()
    return captions

iface = gr.Interface(fn=process_image, inputs="image", outputs="text")
iface.launch()
