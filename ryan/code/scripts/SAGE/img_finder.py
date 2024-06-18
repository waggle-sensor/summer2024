import torch
from PIL import Image
import open_clip
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from os import walk

print(f"loading files...\n\n\n")
filenames = next(walk('/home/ryanrearden/Documents/SAGE_fromLaptop/summer2024/ryan/code/scripts/SAGE/SageImgs/'), (None, None, []))[2]
print("all files loaded")

user_description = input("Please provide a breif description of the image you are looking for:\n")
print() 


model, _, preprocess = open_clip.create_model_and_transforms('ViT-B-32', pretrained='laion2b_s34b_b79k')
model.eval()  # model in train mode by default, impacts some models with BatchNorm or stochastic depth active
tokenizer = open_clip.get_tokenizer('ViT-B-32')

descriptions = [user_description, "an image of the street", "", "night", "day"]
text = tokenizer(descriptions)

with torch.no_grad(), torch.cuda.amp.autocast():
    text_features = model.encode_text(text)
    text_features /= text_features.norm(dim=-1, keepdim=True)

for file in filenames:
    print("new image approaching")
    image = (f'/home/ryanrearden/Documents/SAGE_fromLaptop/summer2024/ryan/code/scripts/SAGE/SageImgs/{file}')
    raw_image = Image.open(image)
    image = raw_image.convert("RGB")
    image = preprocess(image).unsqueeze(0)

    with torch.no_grad(), torch.cuda.amp.autocast():
        image_features = model.encode_image(image)
        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_probs = (100.0 * image_features @ text_features.T).softmax(dim=-1)

    #finds the most likely description 
    most_likely = descriptions[torch.argmax(text_probs)]

    if most_likely == user_description:
        print()
        print("Looks like: ", most_likely)
        imgplot = plt.imshow(raw_image)
        plt.axis('off')
        plt.show()
        plt.bar(descriptions, text_probs.squeeze().detach().cpu().numpy())
        plt.xticks(rotation=45)
        plt.ylabel('Probability (%)')
        plt.show()

