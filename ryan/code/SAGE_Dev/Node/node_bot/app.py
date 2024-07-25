import requests
import json

def sendMessage(text):
    
    headers = {'Content-type': 'application/json'}
    data = {'text': text}

    response = requests.post(url, headers=headers, data=json.dumps(data))


text = "I'll be back"

sendMessage(text)