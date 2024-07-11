import os

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import json
import requests

def runOllama(prompt):
    # Define the URL of your local server
    url = 'http://localhost:11433/api/generate'

    # Define the data payload as a dictionary
    payload = {
        "model": "gemma2:latest",
        "prompt": prompt
    }

    # Send the POST request
    response = requests.post(url, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        response_text = []
        lines = response.text.strip().split('\n')

        for line in lines:
            json_response = json.loads(line)
            if 'response'  in json_response:
                response_text.append(json_response['response'])

        botReply = (''.join(response_text))

        return botReply
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return "Null"

# Install the Slack app and get xoxb- token in advance
app = App(token=os.environ["SLACK_BOT_TOKEN"])


@app.event("message")
def handle_message_events(body, logger, say):
    # Extract the message text from the body dictionary
    message_text = body["event"]["text"]
    botReply = runOllama(message_text)

    say(botReply)

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()








