## Week 1 
### May 28th - 31st
I spent most of my time this week completing the new hire training and writing notes on ML/AI topics, including various sources I've found on my own and each of the following papers recommended by Dario.

- [https://arxiv.org/abs/1301.3781](https://arxiv.org/abs/1301.3781)
- [https://arxiv.org/abs/1409.3215](https://arxiv.org/abs/1409.3215)
- [https://arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762) 
- [https://arxiv.org/abs/1810.04805](https://arxiv.org/abs/1810.04805)
- [https://arxiv.org/abs/2304.12210](https://arxiv.org/abs/2304.12210) 
- [https://arxiv.org/abs/2002.05709](https://arxiv.org/abs/2002.05709)
- [https://arxiv.org/abs/2104.14294](https://arxiv.org/abs/2104.14294)
- [https://arxiv.org/abs/2105.04906](https://arxiv.org/abs/2105.04906) 
- [https://arxiv.org/abs/2301.08243](https://arxiv.org/abs/2301.08243)
- [https://ai.meta.com/blog/yann-lecun-ai-model-i-jepa/](https://ai.meta.com/blog/yann-lecun-ai-model-i-jepa/)


## Week 2
### June 3rd
Finished up the papers and other material from week 1. I feel that I have a much better grasp on the basics now. 

Cloned the audio separation/classification models from [Google's Perch repo](https://github.com/google-research/perch) and began setting up my environment.

### June 4th
Began learning PyTorch, including successfully running several pre-trained image and audio classifier models.

### June 5th - 7th
Set up my SSH keys and got access to `bebop` on `lcrc`. 

Continued learning PyTorch for the remainder of the week.


## Week 3
### June 10th
Went to the required writing coach meeting in the morning.

Gained SSH access to ALCF/Polaris. 

Did more work with PyTorch in the morning before speaking with Dario and narrowing the scope of my project somewhat. Instead of rewriting Google's models from Tensorflow to PyTorch, I will instead focus on implementing the existing models on the Waggle infrastructure. This seems much more feasible given the time left for this internship.

### June 11th
Began working through the edge app tutorial from the documentation on [sagecontinuum.org](https://sagecontinuum.org/docs/category/edge-apps). Waiting on access to the waggle nodes / blade servers to continue on to parts 3 and 4. 
Started learning Docker for deployment on nodes.

### June 12th
Like PyTorch, Docker was a new experience for me. But given some practice I now feel comfortable setting up new images and containers from dockerfiles and the CLI. 

I was also given access to the nodes V009-V012, V029-V039. With a proper environment set up, I should be able to make much faster progress now.

### June 13th - 14th
I understand how to run inference with the model now, but I cannot do so on my local machine as I don't have an NVIDIA GPU. I will aim to get the project containerized and running on a node.

## Week 4
### June 17th - 18th
Getting the Docker environment set up was more complex than expected. The project requires a specific, recent Python version, and the node has outdated CUDA drivers. I finally found an old base image from NVIDIA that satisfied all of the requirements: `nvcr.io/nvidia/tensorflow:23.02-tf2-py3`


### June 19th - 20th
The GPU on the node is working now. I ran inference on some audio samples, successfully separating out bird sources from other background noise in the recording. 

Also wrote a python script for displaying spectrograms from the original and separated audio files.

I suspect that inference results may be improved by training or at least finetuning a MixIT model with our own data, so I will investigate that next.

### June 20th - 21st
I've started understanding how the source code is laid out, but the lack of in-depth documentation is making progress very slow.

## Week 5
### June 24th - 26th
- `perch/chirp/train/separator.py` contains most of the relevant training functions
- in `perch/chirp/data/utils.py`, `data_utils.get_dataset()` is responsible for loading and preparing datasets
    - Preprocessioning via either a custom [TFDS](https://www.tensorflow.org/datasets/add_dataset) (`/data/tfds_builder`) or the `Pipeline` class in `/perch/chirp/preprocessing/pipeline.py`.
    - `MixAudio` provides many helpful options for manipulating audio, but notably the Morton Arboretum data I'm working with is already pre-mixed, as it is comprised of raw recordings made in the field. 

### June 27th 
Began looking at [another Google repo](https://github.com/google-research/sound-separation). Perch is a version of this base MixIT model, with classification steps added on. It may prove somewhat easier to work with this code instead, even though it is lacking in proper documentation just like Perch.

I was able to run a short training (~3 hours, batch size of 2) for the `neurips2020/mixit` model with the FUSS dataset. Inference results from this model are, of course, not great. But some separation is clearly present.

### June 28th 
Wrote the abstract for presenting my work so far, and set up another training to run on the node over the weekend.

## Week 6
### July 1st - 2nd
The training ran for a total of 74 hours. Inference results are much better, but still not quite as good as the pretrained Perch model. My next goal is to fit the Morton Arboretum dataset into the FUSS model's training pipeline. So far I am encountering a shape mismatch error between my data and what the training scripts are expecting.

### July 3rd - 5th
I returned to working with Perch. Successfully ran the preprocessing from `Pipeline` and `tfds_builder.py` to build a TFDS of the Morton Arboretum recordings. But it turns out the training scripts for Perch have even stricter requirements than the inferencing. Unfortunately it might not be feasible to run this on our current edge nodes.

## Week 7
### July 8th - 10th
I fixed the shape mismatch error I was encountering with the FUSS training scripts. It seems FUSS took a "semi-supervised" approach in which the audio mixtures were accompanied by their underlying sources, which are used for a loss calculation. By instead feeding the model with zeros or silence in place of these sources, the training should not run into shape mismatches.   

### July 10th - 12th
The Morton Arboretum recordings are all very large (1 hour long), so I thought that splitting them up before training could allow for using larger batch sizes. I wrote the `wav_slicer.py` script to trim each recording into many smaller segments. 

The nodes have all been down due to a physical migration, so I was not able to make much more progress. Raj had me help with setting up an old Gigabyte BMC server. It has two H100 GPUs, so it could be a great option for training, but I will need to fix many broken things on it first.

## Week 8 
Nodes are available again. Training with the Morton Arboretum data and FUSS scripts is working now, but unfortunately the inference results are not very good. Perhaps the changes I made to stop the shape mismatch error broke something else in the process. 

Worked on my poster for Learning on the Lawn and slides for the Waggle presentation later this week.

## Week 9
Wrote a program for finding "peaks" in recordings and slicing around them. This functions as an improved version of `wav_slicer.py`. This should solve the issue of training data being mostly comprised of background noise like wind, rain, highway sounds, etc.

## Week 10
Began offboarding. Organized all of my code, putting various parts of the project together in one place. Wrote a driver script to run the peak finder and inferencing easily. 
