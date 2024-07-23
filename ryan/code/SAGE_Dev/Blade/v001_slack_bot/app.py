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
    

