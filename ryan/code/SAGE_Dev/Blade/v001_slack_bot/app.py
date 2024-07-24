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
        #"OLLAMA-DEBUG": 1,
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



        #botReply = (''.join(response_text)) + f"\n\nTotal duration: {total_duration_s}s\nLoad duration: {load_duration_ms}ms\neval rate: {eval_rate} tokens\s"
        #botReply = (''.join(verbose_text))
    botReply = (''.join(response_text))
    return botReply

    '''
            if last_line_data:
                total_duration_s = last_line_data['total_duration'] / 1e9
                load_duration_ms = last_line_data['load_duration'] / 1e6
                prompt_eval_duration_ms = last_line_data['prompt_eval_duration'] / 1e6
                eval_count = last_line_data['eval_count']
                eval_duration_s = last_line_data['eval_duration'] / 1e9
                eval_rate = eval_count / eval_duration_s
    '''

    '''
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return "Null"
    '''

def loadSageData():
    filename = "/home/ryanrearden/Documents/SAGE_fromLaptop/sageinfo.json"
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print(f"Error: Could not find local SAGEinfo file: {filename}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in local SAGEinfo file: {filename}")
        return None

#takes in location and sageData. Returns a list of nodes
def getnodes(location, sageData):
    nodes = []
    print(location)
    for item in sageData:
        address = item.get("address", "_")
        vsn = item.get("vsn", "_")
        if location != "" and location.lower() in address.lower():
            nodes.append(vsn)

        if location != "" and location.lower()==vsn.lower():
            nodes.append(vsn)
            return nodes
    return nodes 
    
# Install the Slack app and get xoxb- token in advance
app = App(token='')
#app = App(token=os.environ["SLACK_BOT_TOKEN"])

sageData = loadSageData()

@app.event("message")
def handle_message_events(body, logger, say):
    # Extract the message text from the body dictionary
    message_text = body["event"]["text"]
    print(body)

    #To at, it is in the form <@...>
    bot_ID = "<@" + body["authorizations"][0]["user_id"] + ">"
    user_ID = "<@" + body["event"]["user"] + ">"

    #Bot gets confused when you give it the bot ID. better to just not
    message_text = message_text[(len(bot_ID) + 1):]

    try: 
        #Prompt engineering plus Ollama
        botReply = runOllama(f"Please only reply with with what the user is searching for and where. Reply specifically what there user is looking for as well as the location they are looking for it on a new line: If the user asked Tell me when you see a car in Chicago, print car, then on a newline print Chicago. If the user asks When there is a dog on the street in W026, print dog on the street and then on a newline print W026. Perform like that. Now go ahead with this one: {message_text}")
        #bot will reply with noun\nlocation
        #seperating by newline will split these
        importantWords = botReply.splitlines()

        # Safety Checks
        try:
            lookFor = importantWords[0] if importantWords[0] else ""  # None if empty
            location = importantWords[1].replace(" ", "") if len(importantWords) > 1 else ""  # Check list length
        except IndexError:
            print("Error: importantWords has less than two elements. Skipping processing.")
            lookFor = ""
            location = ""
        say(user_ID)
        #if it is a node
        node_list = getnodes(location, sageData)
        if isinstance(node_list, list) and len(node_list) > 0:
            say(f"Deploying at {location} and looking for {lookFor}")
        else:
            say("No matching nodes found. Please try again")
            

    except Exception as error:
        print(error)
        say(error)

if __name__ == "__main__":
 #   SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
    SocketModeHandler(app, '').start()


'''
# Basic listener that triggers and says "hello" when the script runs
@app.event("message")
def handle_app_mention(event, say):
    say("hello")

# Function to trigger an event to run the say command
def trigger_mention():
    # Using app.client to send a message that mentions the app, which triggers the event listener
    user_id = app.client.auth_test()["user_id"]
    app.client.chat_postMessage(
        channel=user_id,
        text=f"<@{user_id}>"
    )
'''