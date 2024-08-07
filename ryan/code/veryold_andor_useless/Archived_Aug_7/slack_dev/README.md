# Slack Documentation

## Setup 

To download the slack API, go to:
https://api.slack.com/automation/quickstart

Then run 
```
slack login
```

and perform the steps in order to get access. 

run
```
pip install slack_sdk
```

- In OAuth & Permissions go to Scopes.
- Add
    - chat:write
    - im:history
    - im:read
    - im:write
- Copy the Bot User OAuthToken and export it as SLACK_BOT_TOKEN
- Go to App-Level Tokens inside of Basic Information
- If you haven't already generated a Token, go ahead and do that. Select all of the scopes and then make that token into SLACK_APP_TOKEN      

```
export SLACK_BOT_TOKEN='xoxb-XXXXXXXXXXXX-xxxxxxxxxxxx-XXXXXXXXXXXXXXXXXXXXXXXX'

export SLACK_APP_TOKEN='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
```


