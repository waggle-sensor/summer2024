'''
The purpose of this program is to find images that match a user's text prompt
It will use some sort of algorithm to perform the search. 
'''

import json
import re
from fuzzywuzzy import fuzz
import cv2 

JSON_path = '/home/ryanrearden/gitRepos/TroL/testingImgs/data.json'
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

def search_entries(query, data):
    query = preprocess_text(query)
    results = []

    for entry in data:
        description = entry['description']
        similarity = fuzz.partial_ratio(query, description)
        if similarity > 75:  # Adjust the threshold as needed
            results.append((entry, similarity))

    # Sort results by similarity
    results.sort(key=lambda x: x[1], reverse=True)
    return [entry for entry, sim in results]

def show_image(image_path, max_width=800, max_height=600):
  """Displays an image using OpenCV, with a maximum window size"""
  img = cv2.imread(image_path)

  # Get image dimensions and calculate scaling factor if needed
  height, width = img.shape[:2]
  scale_factor = min(max_width / width, max_height / height, 1)  # Limit scaling to 1 (no scaling)

  if scale_factor < 1:  # If image is larger than max size
      # Resize image to fit within max window dimensions
      resized_width = int(width * scale_factor)
      resized_height = int(height * scale_factor)
      img = cv2.resize(img, (resized_width, resized_height))

  # Display the image
  cv2.imshow('Search Result', img)
  cv2.waitKey(0)  # Wait for a key press to close the window
  cv2.destroyAllWindows()



# Load the JSON file
with open(JSON_path, 'r') as file:
    data = json.load(file)

# Preprocess the descriptions
for entry in data:
    entry['description'] = preprocess_text(entry['description'])

query = input("Enter your search query: ")
results = search_entries(query, data)

if results:
    print("Found the following entries:")
    for result in results:
        print(result["description"])
        image_path = result["image_path"]
        show_image(image_path)

else:
    print("No matching entries found.")

