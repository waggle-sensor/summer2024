import os

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import json
import requests

def runOllama(prompt):
    # Define the URL of your local server
    url = 'http://localhost:11434/api/generate'

    # Define the data payload as a dictionary
    payload = {
        "model": "llava",
        "OLLAMA-DEBUG": 1,
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

# Install the Slack app and get xoxb- token in advance
app = App(token='')
#app = App(token=os.environ["SLACK_BOT_TOKEN"])

#get bot ID
bot_id = app.client.auth_test()["user_id"]

@app.event("message")
def handle_message_events(body, logger, say):
    print(body)
    print()
    message_text = body["event"]["text"]
    #may not exist 
    #url = body["event"]["blocks"][0]["elements"][0]["elements"][0]["url"]

    #print(body["event"]["files"][0]["url_private"])
    message = message_text
    # Extract the message text from the body dictionary
    if f"<@{app.client.auth_test()['user_id']}>" in message_text:
        say("Hello!")
    else:
        botReply = runOllama(message)
        say(botReply)

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
    #SocketModeHandler(app, '').start() 







