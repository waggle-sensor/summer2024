from datetime import datetime, timezone
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import json
import requests
import sage_data_client 
from pathlib import Path 
import pandas as pd
from PIL import Image 
import io 
import base64

webhook_url = ""
app = App(token='')
def image_to_base64(image):
    with io.BytesIO() as buffer:
        image.save(buffer, format="JPEG")  # Ensure format matches the image type
        return base64.b64encode(buffer.getvalue()).decode('utf-8')


#takes in img url, login session, and where the img should be stored
def process_file_from_url(url):
    try:
        # Initialize a session and download the file
        username = "rrearden"
        userToken = ""
        with requests.Session() as session:
            session.auth = (username, userToken)
            response = session.get(url.strip())
            response.raise_for_status()  # Raise HTTP error for issues
            # Create an in-memory file-like object
            file_content = io.BytesIO(response.content)
            print(f'Successfully downloaded and opened file from {url}')
            
            # Example: Read the content
            file_data = file_content.read()
            print(f'File data length: {len(file_data)} bytes')
            
            # Example: For image files, use Pillow to open and display the image
            file_content.seek(0)  # Reset file pointer to the start
            try:
                filename= "tmp.jpg"
                # Open and process the image with Pillow
                image = Image.open(file_content)
                
                # Get the directory where the script is located
                script_dir = os.path.dirname(os.path.abspath(__file__))
                
                # Define the path where the image will be saved
                file_path = os.path.join(script_dir, filename)
                
                # Save the image to the specified path
                image.save(file_path)
                return file_path
            except IOError:
                print("The downloaded file is not a valid image.")
            
            return file_content  # Return the in-memory file object

    except requests.exceptions.RequestException as e:
        print(f'Failed to download {url}: {e}')
        return None

def getData(nodes):
    return pd.concat([sage_data_client.query(
        start="-1h",
        filter={
            "plugin": "registry.sagecontinuum.org/theone/imagesampler:0.3.0.*",
            "vsn": node
        }
    ) for node in nodes], ignore_index=True)

#gets all the data from the node
nodes = ["W026", "W07B", "W07A", "W01B"]

df = getData(nodes)
print(df)
#selects the time and img link for furthur processing
time_and_imgs = (df[["timestamp", "value", "meta.vsn"]])

def sendImg(image):
    app.client.files_upload_v2(
            channels="C07DJHV3E2F",
            file=image,
        )

for i in range(len(time_and_imgs['value'])):
    node = time_and_imgs['meta.vsn'][i]
    timestamp = time_and_imgs['timestamp'][i]
    image = process_file_from_url(time_and_imgs["value"][i])
    #image = image_to_base64(image)
    sendImg(image)






if __name__ == "__main__":
    # Get the app token from the environment variable
    SocketModeHandler(app, '').start()