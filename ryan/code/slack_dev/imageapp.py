import os

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import json
import requests
from PIL import Image
import io 


app = App(token=os.environ["SLACK_BOT_TOKEN"])

# Function to download the image from Slack
def download_image(image_url, headers):
    response = requests.get(image_url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to download image: {response.status_code}")
    return response.content

# Event handler for message events
@app.event("message")
def handle_file_shared(body, logger):
    headers = {"Authorization": f"Bearer {os.getenv('SLACK_BOT_TOKEN')}"}
    # Extract the file ID from the event data
    file_id = body["event"]["files"][0]["url_private"]
    image_data = download_image(file_id, headers)

    
    # Use files_remote_info to get file information
    try:
        response = app.client.files_remote_info(file=image_data)
        logger.info(response)
    except Exception as e:
        logger.error(f"Error retrieving file info: {str(e)}")


if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()