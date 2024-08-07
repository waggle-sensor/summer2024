import os
import json
import requests
import base64
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

def runOllama(image_path):
     
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    url = 'http://localhost:11434/api/generate'

    payload = {
        "model": "llava",
        "OLLAMA-DEBUG": 1,
        "prompt": "What is in this piture?",
        "stream": False, 
        "images": [encoded_image]
    }

    response = requests.post(url, json=payload)

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
            #try to print these but if it they are not there print zero
            total_duration_s = last_line_data.get('total_duration', 0) / 1e9
            load_duration_ms = last_line_data.get('load_duration', 0) / 1e6
            eval_count = last_line_data.get('eval_count', 0)
            eval_duration_s = last_line_data.get('eval_duration', 0) / 1e9
            eval_rate = eval_count / eval_duration_s if eval_duration_s != 0 else 0

            #zero means something went wrong
            if total_duration_s == 0:
                return "Null"
            else: 
                botReply = (''.join(response_text)) + f"\n\nTotal duration: {total_duration_s}s\nLoad duration: {load_duration_ms}ms\neval rate: {eval_rate} tokens/s"
        else:
            botReply = ''.join(response_text)
        
        return botReply
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return "Null"

app = App(token=os.environ["SLACK_BOT_TOKEN"])

bot_id = app.client.auth_test()["user_id"]

@app.event("message")
def handle_message_events(body, logger, say):
    if 'files' in body["event"]:
        file_info = body["event"]["files"][0]
        file_url = file_info["url_private"]

        #must do this to prove that is allowed to download the image
        headers = {
            'Authorization': f'Bearer {os.environ["SLACK_BOT_TOKEN"]}'
        }
        response = requests.get(file_url, headers=headers)

        if response.status_code == 200:
            #if success, put the temp img in the same directory (easy)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(current_dir, "temp_image.jpg")
            try:
                #try to open it and download in smaller chunks 
                with open(image_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

            except Exception as e:
                say(text="Failed to save the image.")
                return
            #if everything works it shoudl run ollama 
            if os.path.exists(image_path):
                botReply = runOllama(image_path)
                say(text=botReply)

                os.remove(image_path)
            else:
                say(text="Failed to download the image.")
        else:
            say(text="Failed to download the image.")
    else:
        message_text = body["event"]["text"]
        if f"<@{bot_id}>" in message_text:
            say(text="Hello!")

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()