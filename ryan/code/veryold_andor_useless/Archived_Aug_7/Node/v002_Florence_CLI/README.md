WARNING:
Never run this on a computer that has a GPU you want to use outside of docker.
It will mess everything up because of the fake flash_attn.py script

To run tests on another machine, change that python script name. Otherwise you have to restart your computer because you confused your CUDA driver

To run this you must have a directory called testphotos with photos you want to use. 

Be sure to have the huggingface transformers in a directory as well.
To download a model and processor use:

```
model.save_pretrained
and
processor.save_pretrained
```

How to run and build on node: 

```
$ sudo docker build -t NAME .
$ sudo docker run -it NAME
```
