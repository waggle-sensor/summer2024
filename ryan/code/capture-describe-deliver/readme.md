# How to operate this program

## Capture and Describe Plugin

This contains all of the code that will be deployed on the Wild Sage Nodes. It uses the image sampler plugin code and then generates a description with additional code for Florence-2. All of that gets uploaded to the cloud.

If you are doing bug testing run: 

```
sudo pluginctl build -t capture-and-describe-plugin .

./runme.sh
```
If you run 
```
sudo kubectl get pods
```
You should see the plugin running! Give it some time if you don't see it running yet. 

Then run
```
sudo pluginctl exec -it PLUGINAME /bin/bash
##now you are inside the container##
python3 app.py -stream bottom_camera
```

Give it a little bit of time and it should finish in 2-3 minutes. An image and description will be on the plugin page! 

## Slack Server

This is the folder that goes on the blade that is running the slack part of the program

It has one image with two containers:
- usertoserver
- servertouser 

There is one volume shared between these two containers that contains the userdata (user_data.json)

run with docker-compose

```
sudo docker-compose build
```