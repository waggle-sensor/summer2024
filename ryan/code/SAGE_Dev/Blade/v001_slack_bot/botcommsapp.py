import os

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import json
import requests

def runOllama(prompt, isNode=False):
    # Define the URL of your local server
    url = 'http://localhost:11434/api/generate'

    # Define the data payload as a dictionary
    if isNode:
        payload = {
            "model": "llava",
            "prompt": prompt
        }
    else:
         payload = {
            "model": "gemma2",
            "prompt": prompt
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

            '''
        if last_line_data:
            total_duration_s = last_line_data['total_duration'] / 1e9
            load_duration_ms = last_line_data['load_duration'] / 1e6
            prompt_eval_duration_ms = last_line_data['prompt_eval_duration'] / 1e6
            eval_count = last_line_data['eval_count']
            eval_duration_s = last_line_data['eval_duration'] / 1e9
            eval_rate = eval_count / eval_duration_s
            '''



        botReply = (''.join(response_text)) #+ f"\n\nTotal duration: {total_duration_s}s\nLoad duration: {load_duration_ms}ms\neval rate: {eval_rate} tokens\s"
        #botReply = (''.join(verbose_text))

        return botReply
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return "Null"
    
app = App(token=os.environ["SLACK_BOT_TOKEN"])
webhook_url = "https://hooks.slack.com/services/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"

#get bot ID
bot_id = app.client.auth_test()["user_id"]

botcomms_channel_id = "C07DJHV3E2F"

def send_message_via_webhook(message):
    payload = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": message
                }
            }
        ]
    }
    response = requests.post(webhook_url, json=payload)
    if response.status_code != 200:
        raise ValueError(f"Request to Slack returned an error {response.status_code}, the response is: {response.text}")

def channel_event(channel_id):
    def decorator(func):
        def wrapper(body, logger, say):
            event = body["event"]
            if event["channel"] == channel_id:
                func(body, logger, say)
        return wrapper
    return decorator

@app.event("message")
#@channel_event(botcomms_channel_id)
def handle_message_events(body, logger, say):
    message_text = body["event"]["text"]
    event = body["event"]
    #if event.get("subtype") == "bot_message":
        #print("LETS GO")
    
    # Extract the message text from the body dictionary
    if "FROM NODE TO SERVER" in message_text:
        print('got llava mssg')
        message_text = message_text[19:]
        message = runOllama(message_text)
        send_message_via_webhook(f"FROM SERVER TO NODE\n" + message)
        app.client.chat_postMessage(channel=botcomms_channel_id, text=message)

    elif "FROM SERVER TO NODE" in message_text:
        print("got server messg")
        message_text = message_text[19:]
        message = runOllama(message_text, isNode=True)
        send_message_via_webhook(f"FROM NODE TO SERVER\n" + message)

    else:
        say(message_text)

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()








