import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import requests
import json


SAGE_INFO = "/home/ryanrearden/Documents/SAGE_fromLaptop/summer2024/ryan/code/SAGE_Dev/Blade/v002_slack_bot/sageinfo.json"
USER_DATA = "/home/ryanrearden/Documents/SAGE_fromLaptop/summer2024/ryan/code/SAGE_Dev/Blade/v002_slack_bot/user_data.json"
#SAGE_INFO = "/app/data/sageinfo.json"
#USER_DATA = "/app/data/user_data.json"
OLLAMA_SERVER = "http://localhost:11433/api/generate"

# see README if unsure what this means
app = App(token=os.environ["SLACK_BOT_TOKEN"])


#This is how Gemma2 is accessed
def runOllama(prompt):

    # Define the data payload as a dictionary
    #the model we have is gemma2
    #Use the prompt as the thing to ask the LLM
    payload = {
        "model": "gemma2:latest",
        "prompt": prompt
    }

    # Send the POST request to the server
    response = requests.post(OLLAMA_SERVER, json=payload)

    # Check if the request was successful
    #and gets the text
    if response.status_code == 200:
        #The text is generated in a weird way (word by word) so each word has to be captured
        response_text = []
        lines = response.text.strip().split('\n')


        for i, line in enumerate(lines):
            json_response = json.loads(line)
            if 'response' in json_response:
                response_text.append(json_response['response'])
    #join the entire response into one string for usability
    botReply = (''.join(response_text))
    return botReply

#Gets all of the node information from a JSON file 
#Used later to check if the user asked for a location we can access
def loadSageData():
    try:
        with open(SAGE_INFO, "r") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print(f"Error: Could not find local SAGEinfo file: {SAGE_INFO}")
        return {}
    except json.JSOND: #this "else" function can return "None" which then just stops the processeError
        print(f"Error: Invalid JSON format in local SAGEinfo file: {SAGE_INFO}")
        return {}

#takes in location and sageData. Returns a list of nodes
#So when I say "Chicago", this will find all of the nodes in Chicago
#TODO get it to do the same with states. Right now you have to specify IL and it won't understand Illinois (because of how the file lists states)
def getnodes(location, sageData):
    nodes = []
    print(location)
    for item in sageData:
        address = item.get("address", "_")
        vsn = item.get("vsn", "_")

        #If the location is an address, add the node from that address
        if location != "" and location.lower() in address.lower():
            nodes.append(vsn)

        #if the location IS a node, append it and return 
        #TODO allow the user to ask for more than one node
        if location != "" and location.lower()==vsn.lower():
            nodes.append(vsn)
            return nodes
    return nodes 

#Try to read the user data
#If it doesn't exist, make a JSONable object
with open(USER_DATA, 'r') as f:
    try:
        user_data = json.load(f)
    except Exception as e:
        user_data = {}

#load all the data up
sageData = loadSageData()

#these two events handle if someone sends a message via private DM or public channel inside of Slack
@app.event("message")
@app.event("app_mention")
def handle_message_events(body, logger, say):
    # Extract the message text from the body dictionary
    message_text = body["event"]["text"]

    #prints for debugging
    print(body)

    #IDs are in the form <@...>
    bot_ID = "<@" + body["authorizations"][0]["user_id"] + ">"
    user_ID = "<@" + body["event"]["user"] + ">"

    #channel IDs are hexadecimals
    channel_ID = body["event"]["channel"]

    #Bot gets confused when you give it the bot ID. better to just not
    #TODO find the bot ID in the message rather than just assume it is at the front
    message_text = message_text[(len(bot_ID) + 1):]

    try: 
        #Prompt engineering plus Ollama
        botReply = runOllama(f"Please only reply with with what the user is searching for and where. Reply specifically what there user is looking for as well as the location they are looking for it on a new line: If the user asked Tell me when you see a car in Chicago, print car, then on a newline print Chicago. If the user asks When there is a dog on the street in W026, print dog on the street and then on a newline print W026. Perform like that. Now go ahead with this one: {message_text}")
        #bot will reply with noun\nlocation
        #seperating by newline will split these

        #So if I said "Tell me when there is a dragon in Norway", Ollama would output:
        #dragon
        #Norway
        #then the lines are split and made into importantWords = ["dragon", "Norway"]
        importantWords = botReply.splitlines()

        
        try:
            #the first item is the word
            #the second item is the location
            #TODO allow the user to look for multiple words in multiple locations
            lookFor = importantWords[0] if importantWords[0] else ""  # None if empty
            location = importantWords[1].replace(" ", "") if len(importantWords) > 1 else ""  # Check list length
        # Safety Checks if Gemma messes up
        except IndexError:
            print("Error: importantWords has less than two elements. Skipping processing.")
            lookFor = ""
            location = ""

        #mentions the user
        say(user_ID)
        #if it is a node
        node_list = getnodes(location, sageData)
        if isinstance(node_list, list) and len(node_list) > 0:
            #if everything is right with the list, tell the user what you are about to do
            #Deploying at Norway and looking for dragon
            say(f"Deploying at {location} and looking for {lookFor}")

            #then dump all of that info into a json file so that serverToUser.py can pick it up later when stuff comes
            #in through the plugin
            with open(USER_DATA, 'w') as f:

                #the JSON order goes: node, thing, channel, user 
                for location in node_list:
                    if location not in user_data:
                        user_data[location] = {}
                    if lookFor not in user_data[location]:
                        user_data[location][lookFor] = {}
                    if channel_ID not in user_data[location][lookFor]:
                        user_data[location][lookFor][channel_ID] = []
                    if user_ID not in user_data[location][lookFor][channel_ID]:
                        user_data[location][lookFor][channel_ID].append(user_ID)
                json.dump(user_data, f, indent=4)
                '''
            ********The JSON file could, for example, look like this*****
            *    {                                                      *
            *    "W0B3": {                                              *
            *        "yellow": {                                        *
            *            "C07DJHV3E2F": [                               *
            *                "<@P176B3NUDR9>"                           *
            *            ]                                              *
            *       }                                                   *
            *   }                                                       *
            *}                                                          *
            *************************************************************
                '''
        else:
            say("No matching nodes found. Please try again")
            
    #say if something messed up
    except Exception as error:
        print(error)
        say(error)

if __name__ == "__main__":
    # Get the app token from the environment variable
    #see README if needed
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()