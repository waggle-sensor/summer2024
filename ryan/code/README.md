# CODE README 

Update: I am currently in the process of making code easier to find

## How things ar structured

```
|──laptop_dev
|
|──SAGE_dev
|
|──slack_dev
|
|──veryold_andor_useless
```

laptop_dev contains everything I am playing around with because I have a NVIDIA RTX 4060 on my laptop. I may also migrate some code from there to SAGE_dev when the time comes 

SAGE_dev contains everything I deploy on the nodes and blades. The goal is to directly tranfer from the node/blade files onto the nodes/blades. This way I never loose any code and have it floating around. 

slack_dev has some of my code I was using in order to figure out the Slack API 

veryold_andor_useless is for historical purposes. If, one day, someone really needs to look at TroL, my code is still in there--it may be hard to figure out and use but I felt bad deleting it. 
## Things I always forget but would be useful to remember [in no particular order (yet)]

### To port over to a node running Ollama and run llava
You have to confiugre everything first


1. First you want to ssh and port forward at the same time to be really cool. You may already have Ollama installed on your local machine. To prevent against issues, forward to a port close to it:
    - ssh waggle-dev-node-NODE -L localport:localhost:ollamaport
    - ollama port will probably be 11434
    - I like to put my localport as 11430

2. Inside of the node that has the ollama image run: 
    - sudo docker run -p 11434:11434 DOCKERIMAGEHEX ollama start

3. *THEN* on your main machine run:
    - OLLAMA_HOST="127.0.0.1:11430
    - or whatever you made your local port. 

### How to delete useless containers 

1. use sudo docker ps -a to see all of the containers you have  
    - Oh no there are so many that are useless!!

2. use the pipe and head/tails -n +- number
    - So to not see the bottom 2 use: 
        - sudo docker ps -a | head -n -2
    - play around with it to eventually see all the ones you WANT to delete

3. Then use sudo docker rm with whatever you just did
    - For example sudo docker rm $(sudo docker ps -a | head -n -2) will delete all the containers except for the bottom two
    -Make sure to run sudo docker stop ... before this--there might be an error

### How to use rsync (kind of )

rsync -avz <source_folder> <user>@<remote_host>:<destination_directory>

so if I wanted to transfer something to a waggle node I would find the directory and then (if I wanted it in the rrearden directory) 

rsync -avz folder waggle-dev-node-NODE:/home/waggle/rrearden 


### How to build for multiple platforms docker

```
docker buildx build --platform linux/amd64,linux/arm64 -t myimage:latest .
```


