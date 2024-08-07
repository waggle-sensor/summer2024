import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import requests
import sage_data_client 
from PIL import Image 
import io 
import json
import time

#global variables for safe keeping :) 
#USER_DATA = '/home/ryanrearden/Documents/SAGE_fromLaptop/summer2024/ryan/code/SAGE_Dev/Blade/v002_slack_bot/user_data.json' 
USER_DATA = '/app/data/user_data.json' 

USERNAME = App(token=os.environ["SAGE_USERNAME"])
USERTOKEN = App(token=os.environ["SAGE_USERTOKEN"])

# see README if unsure what this means
app = App(token=os.environ["SLACK_BOT_TOKEN"])

#Get the JSON file if it exists. Otherwise make something that would be JSONable 
with open(USER_DATA, 'r') as f:
    try:
        user_data = json.load(f)
    except Exception as e:
        user_data = {}

#takes in img url, login session, and where the img should be stored
#basically downloads one image at a time and names it tmp.jpg so that Slack can send it
#Someone please let me know if I can do this without downloading the image. Seems uneeded 
#TODO do this without having to download the image

def process_file_from_url(url):
    try:
        with requests.Session() as session:
            #get username and usertoken for verfication
            session.auth = (USERNAME, USERTOKEN)
            response = session.get(url.strip())
            response.raise_for_status()  # Raise HTTP error for issues
            # Create an in-memory file-like object
            file_content = io.BytesIO(response.content)
            print(f'Successfully downloaded and opened file from {url}')
            file_content.seek(0)  # Reset file pointer to the start
            
            try:
                #for debugging
                print(file_content)

                #lame name but fine
                #TODO make this name match the name on the SAGE website
                filename= "tmp.jpg"

                # Open and process the image with Pillow
                image = Image.open(file_content)
                
                # Get the directory where the script is located
                script_dir = os.path.dirname(os.path.abspath(__file__))
                
                # Define the path where the image will be saved
                file_path = os.path.join(script_dir, filename)
                
                # Save the image to the specified path
                image.save(file_path)
                return file_path
            

            except IOError:
                print("The downloaded file is not a valid.")
            
            #if it ends up just being a file but not an image, still return it
            #shouldn't be needed but you never know.
            return file_content  # Return the in-memory file object


    except requests.exceptions.RequestException as e:
        print(f'Failed to download {url}: {e}')
        return None

#sage data client stuff.
#Gets all of the info from the plugin that is needed
def getData():
    df = sage_data_client.query(
    start="-3h", 
    filter={
        "plugin": "10.31.81.1:5000/local/capture-and-describe-plugin"
    }
)
    return df



#image is open image
#des is the description generated by Florence-2
#user_description is what the user is looking for (ex. smoke)
#channel ID is used to find the right place to send the message on SLACK
    #it will be the same place the user sent the request. Wherever that is. See userToServer.py to get more info
    #TODO send the user this information in their private slack channel regardless of where they send the inital message
#user_ID is the ID of the user who sent the message. User IDs look like "<@APOKF3POI>" (something along those lines)
def sendToSlack(image, des, user_description, channel_ID, user_ID):

    channel = channel_ID

    #files_upload_v2 sends the image
    app.client.files_upload_v2(
                channels=channel,
                file=image,
            )
    
    #chat_postMessage sends the description along with the other strings
    app.client.chat_postMessage(
        channel=channel,
        text=f"{user_ID}\nFound a match for {user_description}\n{des}",
        )
    
    #Descriptions are sent faster than images. This makes it hard to know what description goes to what image
    #5 seconds is enough time to send each pair and have them together in the app
    #TODO Instead of time.sleep, have a listener that allows program continuation after the image is verfified to be in the app
    time.sleep(5)

#this is only used if the the matching image timestamp is not above or below the description timestamp. 
def find_upload_by_timestamp(timestamp, exclude_index):
    # Filter the DataFrame for matching rows
    matches = imgs_and_des[(imgs_and_des['timestamp'] == timestamp) & (imgs_and_des['name'] == 'upload')]
    
    # Check if exclude_index exists in the filtered DataFrame and drop it if present
    if exclude_index in matches.index:
        matches = matches.drop(index=exclude_index)
    
    # Return the value if matches are found, else return None
    return matches['value'].iloc[0] if not matches.empty else None

#selects the time and img link for furthur processing
#I told chatGPT to make the code with as few lines as possible. It does make it a little hard to read
#Basically checks if the new plugin data matches with any user request. If it does, the image and description are sent to the user
try: 
    df = getData()
    print(df)

    #this is from the sage.data.client info
    imgs_and_des = (df[["timestamp", "name", "value", "meta.vsn"]])

        
    # Process the DataFrame
    #take the data and check each part individually
    for i, row in imgs_and_des[imgs_and_des['name'] == 'description'].iterrows():
        #get the node (ex. W023)
        meta_vsn = row['meta.vsn']
        #if the node is found in a request continue 
        if meta_vsn in user_data:
            #check all of the user descriptions. Then channels are the next itteration so keep that just in case
            for user_description, channels in user_data[meta_vsn].items():
                #if something in the user description is in the image description, continue
                #TODO use a better search method than just "in"
                if user_description in row['value']:
                    #call the image description "des"
                    des = row['value']
                    #By this point we know an image has what the user wants. Now we have to find that image
                    #First look one above and one below the description by timestamp.
                    #The timestamps should match so this will be easy to find. If it is not above or below, check everything else
                    upload_value = (
                        imgs_and_des.iloc[i-1]['value'] if i > 0 and imgs_and_des.iloc[i-1]['timestamp'] == row['timestamp'] and imgs_and_des.iloc[i-1]['name'] == 'upload'
                        else imgs_and_des.iloc[i+1]['value'] if i < len(imgs_and_des) - 1 and imgs_and_des.iloc[i+1]['timestamp'] == row['timestamp'] and imgs_and_des.iloc[i+1]['name'] == 'upload'
                        #this "else" function *can* return "None" which then just stops the process
                        else find_upload_by_timestamp(row['timestamp'], i)
                        
                    )
                    #if the image is found, open it and send it!
                    if upload_value:
                        for channel_ID, user_IDs in channels.items():
                            for user_ID in user_IDs:
                                print(f"Timestamp: {row['timestamp']}, Channel ID: {channel_ID}, User ID: {user_ID}, Upload Value: {upload_value}")
                                image = process_file_from_url(upload_value)
                                sendToSlack(image, des, user_description, channel_ID, user_ID)


#say if anything goes wrong 
except Exception as e:
    print("ERROR ", e)



if __name__ == "__main__":
    # Get the app token from the environment variable
    #see README if needed
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()




#TODO have the user queries be deleted after a certian amount of time