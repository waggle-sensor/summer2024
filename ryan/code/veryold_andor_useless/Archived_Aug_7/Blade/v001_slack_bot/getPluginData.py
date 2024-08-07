import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import requests
import sage_data_client 
from PIL import Image 
import io 

# see README if unsure what this means
app = App(token=os.environ["SLACK_BOT_TOKEN"])

#takes in img url, login session, and where the img should be stored
#basically downloads one image at a time and names it tmp.jpg so that Slack can send it
def process_file_from_url(url):
    try:
        # Initialize a session and download the file
        username = "rrearden"
        userToken = 
        with requests.Session() as session:
            session.auth = (username, userToken)
            response = session.get(url.strip())
            response.raise_for_status()  # Raise HTTP error for issues
            # Create an in-memory file-like object
            file_content = io.BytesIO(response.content)
            print(f'Successfully downloaded and opened file from {url}')
            file_data = file_content.read()
            file_content.seek(0)  # Reset file pointer to the start
            
            try:
                print(file_content)
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
            
            return file_content  # Return the in-memory file object

    except requests.exceptions.RequestException as e:
        print(f'Failed to download {url}: {e}')
        return None

#sage data client stuff
def getData():
    df = sage_data_client.query(
    start="-1h40m", 
    filter={
        "plugin": "10.31.81.1:5000/local/capture-and-describe-plugin"
    }
)
    return df

def sendToSlack(image, des):
    channel = "C07DJHV3E2F"

    #sends image

    app.client.files_upload_v2(
                channels=channel,
                file=image,
            )
    
    #sends description
    app.client.chat_postMessage(
        channel=channel,
        text=f"Found a match!\n{des}",
        )

#this is only used if the the matching image timestamp is not above or below the description timestamp. 
def find_upload_by_timestamp(timestamp, exclude_index):
    matches = imgs_and_des[(imgs_and_des['timestamp'] == timestamp) & (imgs_and_des['name'] == 'upload')].drop(index=exclude_index)
    return matches['value'].iloc[0] if not matches.empty else None


#selects the time and img link for furthur processing
try: 
    df = getData()
    print(df)
    imgs_and_des = (df[["timestamp", "name", "value", "meta.vsn"]])

        
    for i, row in imgs_and_des[imgs_and_des['name'] == 'description'].iterrows():
        if "yellow" in row['value']:
            des = row['value']
            upload_value = (
                #gets the image url that matches the description
                #if there is more than 1 value and the matching timestamp is above or below the description timestamp,
                #otherwise, try to hunt it down in another index. 
                imgs_and_des.iloc[i-1]['value'] if i > 0 and imgs_and_des.iloc[i-1]['timestamp'] == row['timestamp'] and imgs_and_des.iloc[i-1]['name'] == 'upload'
                else imgs_and_des.iloc[i+1]['value'] if i < len(imgs_and_des) - 1 and imgs_and_des.iloc[i+1]['timestamp'] == row['timestamp'] and imgs_and_des.iloc[i+1]['name'] == 'upload'
                else find_upload_by_timestamp(row['timestamp'], i)
            )
            #if there is a matching image URL, return the image and the description
            if upload_value:
                print(f"Found matching upload value: {upload_value}")
                image = process_file_from_url(upload_value)
                sendToSlack(image, des)

#say if anything goes wrong 
except Exception as e:
    print("ERROR ", e)




if __name__ == "__main__":
    # Get the app token from the environment variable
    #see README if needed
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
