import io
import requests
import torch
from PIL import Image
import open_clip


#takes in a string and returns an preprocessed image
def readImage(imgIpt):
  #a horrible hackish way to determine if its an URL or a downloaded img
  if "http" in imgIpt:
    #does URL things
    image = (f'{imgIpt}')
    # Download image data
    img_data = requests.get(image).content
    #Decode image data (no need to save)
    image = Image.open(io.BytesIO(img_data))
    image = image.convert("RGB")



  else:
    #opens image if its already on the computer
    image = Image.open(f'{imgIpt}')
    image = image.convert("RGB")

    #Printed to know how long it takes
    print()
    print()
    print("*****************************")
    print("*                           *")
    print("* finished opening image :) *")
    print("*                           *")
    print("*****************************")
    print()
    print()
  

  
  return image


imgIpt = input("\n \n \n Please input the link or full path:\n")

image = readImage(imgIpt)

model, _, preprocess = open_clip.create_model_and_transforms('ViT-B-32', pretrained='laion2b_s34b_b79k')
model.eval()  # model in train mode by default, impacts some models with BatchNorm or stochastic depth active
tokenizer = open_clip.get_tokenizer('ViT-B-32')


image = preprocess(image).unsqueeze(0)

user_description = input("Please provide a breif description of the image you are looking for:\n")
print() 

descriptions = [user_description, "an image of the street", "", "four way intersection in a city", "day"]
text = tokenizer(descriptions)

with torch.no_grad(), torch.cuda.amp.autocast():
    image_features = model.encode_image(image)
    text_features = model.encode_text(text)
    image_features /= image_features.norm(dim=-1, keepdim=True)
    text_features /= text_features.norm(dim=-1, keepdim=True)

    text_probs = (100.0 * image_features @ text_features.T).softmax(dim=-1)
    print(text_probs)

#finds the most likely description 
most_likely = descriptions[torch.argmax(text_probs)]

if most_likely == "":
   most_likely = "not the user description"

print()
print("Looks like: ", most_likely)

