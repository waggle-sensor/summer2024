How to run 

```
 $ sudo docker build -t NAME .
 $ sudo docker run --gpus all -p 7860:7860 name
```

This assumes you want to make a tunnel from the node port to the gradio script inside of the container the same
AND that the gradio port is 7860


Then, open another terminal on your machine and type:
ssh waggle-dev-node-NODE -L 7860:localhost:7860


This will make a tunnel from your local machine port to the port in the node.
The last part reads: -L LOCALPORT:localhost:NODEPORT 