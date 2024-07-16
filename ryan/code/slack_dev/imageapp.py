import os
import json
import requests
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

image_save_directory = '/home/ryanrearden/Documents/SAGE_fromLaptop/summer2024/ryan/code/slack_dev/imgs'
def runOllama(image_path):
    # Define the URL of your local server
    url = 'http://localhost:11434/api/generate'

    # Define the data payload
    payload = {
        "model": "llava",
        "OLLAMA-DEBUG": 1,
        "image_path": image_path
    }

    # Send the POST request
    response = requests.post(url, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        response_text = []
        lines = response.text.strip().split('\n')
        last_line_data = None

        for i, line in enumerate(lines):
            json_response = json.loads(line)
            if 'response' in json_response:
                response_text.append(json_response['response'])
                if i == len(lines) - 1:
                    last_line_data = json_response

        if last_line_data:
            total_duration_s = last_line_data.get('total_duration', 0) / 1e9
            load_duration_ms = last_line_data.get('load_duration', 0) / 1e6
            eval_count = last_line_data.get('eval_count', 0)
            eval_duration_s = last_line_data.get('eval_duration', 0) / 1e9
            eval_rate = eval_count / eval_duration_s if eval_duration_s != 0 else 0

            botReply = (''.join(response_text)) + f"\n\nTotal duration: {total_duration_s}s\nLoad duration: {load_duration_ms}ms\neval rate: {eval_rate} tokens/s"
        else:
            botReply = ''.join(response_text)
        
        return botReply
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return "Null"

# Install the Slack app and get xoxb- token in advance
app = App(token=os.environ["SLACK_BOT_TOKEN"])

# Get bot ID
bot_id = app.client.auth_test()["user_id"]

@app.event("message")
def handle_message_events(body, logger, say):
    if 'files' in body["event"]:
        file_info = body["event"]["files"][0]
        file_url = file_info["url_private"]

        headers = {
            'Authorization': f'Bearer {os.environ["SLACK_BOT_TOKEN"]}'
        }
        response = requests.get(file_url, headers=headers)

        if response.status_code == 200:
            # Define the image path
            image_path = os.path.join(image_save_directory, "temp_image.jpg")
            with open(image_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        print("downloading")
            print(f"Image downloaded to: {image_path}")
            
            # Run Ollama on the image
            botReply = runOllama(image_path)
            say(text=botReply)

            # Optionally delete the temporary image file
            os.remove(image_path)
        else:
            say(text="Failed to download the image.")
    else:
        message_text = body["event"]["text"]
        if f"<@{bot_id}>" in message_text:
            say(text="Hello!")

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
