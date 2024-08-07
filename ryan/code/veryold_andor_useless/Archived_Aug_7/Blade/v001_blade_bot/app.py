import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Initialize the Bolt App with your bot token and signing secret
app = App(token="")#, signing_secret=os.environ.get("SLACK_SIGNING_SECRET"))

# Basic listener that triggers and says "hello" when the script runs
@app.event("app_mention")
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

# Start your app and trigger the mention event
if __name__ == "__main__":
    "hello"
    trigger_mention()
    handler = SocketModeHandler(app, "")
    handler.start()

