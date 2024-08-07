WARNING:
Never run this on a computer that has a GPU you want to use outside of docker.
It will mess everything up because of the fake flash_attn.py script

To run tests on another machine, change that python script name. Otherwise you have to restart your computer because you confused your CUDA driver

To run this you must have a directory called testphotos with photos you want to use. 

How to run and build on node: 

```
$ sudo docker build -t NAME .
$ sudo docker run -it -v /home/waggle/.cache/huggingface:/hf_cache NAME
```
