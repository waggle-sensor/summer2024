# Daily logs

Link to the code repository I'm working on: [PTZJEPA](https://github.com/Brookluo/PTZJEPA)
These codes are merged into the [main waggle repository](https://github.com/waggle-sensor/PTZJEPA)

## Week 08/05 -- 08/11

### 08/03 Mon

- After many iterations of the lifelong learning, the model finally starts to show some interesting behavior, such as moving the camera in an unexpected pattern. I changed the reward from max to min, so the model should minimize the reward rather than maximize it. Something might be wrong when the model tries to maximize the reward
- Added another analysis suite to read the tracking results data and make pointings, embeddings, and commands plots with rewards.

## Week 07/29 -- 08/04

### 08/02 Fri

- Finished coding the analysis tool for the learning results
- Found the embeddings and the pointings have some interesting patterns, and needs to be fully understood and addressed before moving on
- The agent seems to move to decrease the reward rather than increase the reward as expected

### 08/01 Thu

- Continued developing the analysis code
- Merged the pull request for lifelong learning
- Discussed the federated learning idea with centralized and decentralized ideas.
- Attended the Learning on the Lawn poster session

### 07/31 Wed

- Started to develop the analysis code for the lifelong learning results
- Formalized the lifelong learning code and discussed some training results and directory structure with Dario

### 07/30 Tue

- Add function to track all images, positions, commands, embeddings from the training
- Finished checking some preliminary training results from the lifelong learning

### 07/29 Mon

- Fixed a bug on waggle plugin issue with the publishing the message
- Fixed another bug on missing image when agent starts to capture images causing the program to halt

## Week 07/22 -- 07/28

### 07/26 Fri

- Kayak day!

### 07/25 Thu

- Finally finished coding lifelong learning diagnostics and all information gathering procedure
- Images, positions, commands and embeddings should be gathered while training the model when user provides `--track_all` argument

### 07/24 Wed

- Modified many parts of the code for clarification of the input
- Update tracking functionalities
- Added many auxiliary diagnostics, such as timestamps, to help understand the gathered data

### 07/23 Tue

- Tested the tracking all output results and fixed some path issues
- Discussed some other diagnostics to gather during inference and training phase

### 07/22 Mon

- Add functions to generate diagnostics output such as embeddings, positions, commands, etc
- Change saving the output embeddings from numpy to hdf5 to ensure performance and large data volume holding is possible.
- Did SAGE project presentation!

## Week 07/15 -- 07/21

### 07/19 Fri

- Continued to work on the tracking function and diagnostics gathering capabilities

### 07/18 Thu

- Changed the logger input and fixed a bug with input to the vision transformer
- Started to develop the tracking function to track the lifelong learning model progress

### 07/17 Wed

- Fixed many issues with the code
  - Program halts when the first image is not available or failed to acquire
  - Some images with space in the file name can created a file error during saving
  - File permission issue
  - dtypes for inference to the model
- Standardize the timestamp and filename for consistency and following analysis

### 07/16 Tue

- Finished coding the analysis function
- I found the lifelong learning is too complex with many components. However, to explain some effects, we have to have some reproducility and explainability for the model. Those two aspects all reply on the traceability of the models. We need to add the traceability to the model
- Conveyed this idea to Dario and he also agreed that we need some traceability for the models to analyze and explain later behaviors

### 07/15 Mon

- Reduced the redundant code
- Started to code the analysis function to process the embeddings
- Fixed some bugs for inference and permission issue
- Added more logging information

## Week 07/08 -- 07/14

### 07/12 Fri

- Work from home, thanks to CrowdStrike :-)
- Fixed a bug in JEPA only training (not world model training)
- Added some tests for larger images

### 07/11 Thu

- Presented the update at the group meeting
- Finally regained access to the node in the afternoon, started to run lifelong learning
- Fixed some file paths issue with lifelong learning

### 07/10 Wed

- Toured ALCF
- Node is still offline, so discussed some future collaboration possibility with Dario

### 07/09 Tue

- The DBSCAN result for the embeddings shows that the model learns some clear pattern of the image
  but after looking into the images, I didn't find a clear meaning of the clusters. Will try to look into the images more.
- Discussed this result with Dario and he suggested that there might be some potential bugs in the code
  causing the model to learn the wrong information.
- The nodes are down, so I cannot check the life-long learning workflow on the Dell blade.

### 07/08 Mon

- Trying to understand the meanings of the clusters from the world model
- Trying to run the whole workflow for life-long learning on the Dell blade

## Week 07/01 -- 07/07

### 07/05 Fri

- Finished the evaluation of the fourth channel
- Generated some tSNE plots for the embeddings to show the clusterization
- There are some distinct clusters and start to look into the meaning of each cluster

### 07/04 Thu

- Independence day

### 07/03 Wed

- Attended the team meeting
- Finished the training and started the evaluation of the fourth channel

### 07/02 Tue

- Fixed issues with image directories
- Finished adding the depth as a fourth channel
- Started the fourth channel training on the Dell blade

### 07/01 Mon

- Start to add the depth as the fourth channel
- Improved the logging messages inside the training

## Week 06/24 -- 06/30

Main focus: evaluate the world model training performance and the dreamer training

### 06/28 Fri

- Modified the code to use position directly rather parsing the distance from the image name
- Had more discussions on interpreting the embeddings and the clusters
  - The model seems to **not** learn the depth or zoom information very well
  - Adding the depth or zoom as the fourth channel
  - Transform (such as normalization or projection) the reward into wider space for model to learn it better

### 06/27 Thu

- Merged the code from my repository to the main waggle repository
- Tested the code to run on Dell blade controlling both the Axis and Hanwha cameras
- Attended the team meeting and discussed the next steps
- Got feedback from the team on the evaluation results
  - Check input from the world model and add more diagnostics for the dataset
  - Calculate the distance between each image and visualize the distribution. Potentially adding distance as a weight for the reward
  - If possible, test the framework with a dynamic environment?

### 06/26 Wed

- Finished the evaluation and found several issues:
  - Rewards from the world model span in a very narrow range
  - The self prediction reward is unexpectedly high
  - The n step prediction does not have a clear path
  - However, there are some patterns on the clusterization for each step case

### 06/25 Tue

- Started to evaluate the inference results
- Tested the sorting and found some issues with the order
- Presented some initial clusterization results


### 06/24 Mon

- Updated the code to generate reward function from the predictor in world model
  - Each image in a minibatch is used to compare with all other images to generate the embeddings (target, context), and the predictor. (Bijection-like)
  - Sort the input data in the order of image capturing time to ensure temporal coherence between images. We want the model to understand the movement of the images are continuous.
- Generated the embeddings for the images and the predictor
- Performed clusterization and loss analysis for normal IJEPA and world model 

## Week 06/17 -- 06/23

Main focus: start the world model and dreamer training on nodes

### 06/21 Fri

- Started inference on the world model on Dell blade
- Fixed some bugs with the inference code
- Haven't touched the dreamer training yet, will start it next week

### 06/20 Thu

- Discussed more framework details
  - How to solve the communication issue between the nodes
  - How to implement the federated learning
  - Potential collapse due to low resolution and limited diversity of images
- Fixed some bugs on reading bad images

### 06/19 Wed

- Discussed the gradient issue with Dario, and clarified the ML procedure
  - The two losses are 1. embedding matching loss, and 2. prediction of the gradients
  - Therefore, the `target_encoder.zero_grad()` is fine to use
- Started the training of the world model on Dell blade. The training is using realtime images from the PTZ camera inside ANL.

### 06/18 Tue

- Fixed the compatibility issue with the PyTorch version
  - CUDA==10.2 on sage node, CUDA==11.6 on most dell blades
  - CUDA 11.6 supports up to pytorch 1.13, but the code requires 2.0
  - Updated the dockerfile and rebuilt the docker image to use pytorch 1.13 with cuda 11.6 to run all training on Dell blades
- Fixed a bug with acquiring images with Axis cameras
- Start to change the code to adapt to pytorch 1.13
  - Found some potential issues with `encoder.zero_grad()`, which could remove all gradients accumulated and made the training pointless.
- Helped others to fix the compatibility issue with the PyTorch version
- Toured the Argonne campus.

### 06/17 Mon

- Tested the world model training on the SAGE node but had several issues:
  - PyTorch version causes compatibility issues with the code (needs 2.0 but has 1.9 instead)
  - Trainings are all interrupted by the node restart
  - The training is very slow
- Moved to the Dell blade to train the models, but has to adapt the code to the new environment
  - Communication between node and blade can be difficult
  - Transferring control commands and images has to be implemented
- The docker image has to be modified with the new environment

## Week 06/10 -- 06/16

Main focus: training on a sage node with acquiring images on-the-fly with PTZ camera

### 06/14 Fri

- Found the "@" causing the empty images, fixed the issue. This issue causes a nominal file to exist but with no content.
- Fix another corrupted JPG issue by verifying the image, and open and save the image again.
- Started training the model on the SAGE node with the PTZ cameras acquiring images on-the-fly!
- Went through the code with Dario to discuss the next steps

### 06/13 Thu

- Changed many parts of the code on file structure, changed code's usage of relative path to absolute path inside docker container
- Tested the parts of the code on the SAGE node
- Fixed a URL bug causing the images to not successfully download
- Found another issue with empty images, plan to fix it tomorrow

### 06/12 Wed

- Wrote documentation for ptz-sampler and tested the code
- Found another issue that the node will automatically restart, potentially due to training taking too much memory
- Fixed the issue with file mounting
- Observing the training loss plateau on W084!
- Will have to fix the issue with the node restart

### 06/11 Tue

- Used the waggle plugin base as the base image for the docker container
  - Fixed some CUDA incompatible issues with the changes
- Still cannot get images from the PTZ camera using container
- There were also some file issue due to the volume mounting with docker

### 06/10 Mon

- Successfully accessed the SAGE node with the PTZ cameras using UI and checked the code can move the camera
- Modified the code to acquire images on-the-fly with PTZ camera
- Got several errors caused by both the docker container and the code
- Worked on fixing the errors and testing the code

## Week 06/03 -- 06/09

Main focus: Interpretation of the embeddings and training on the SAGE node

### 06/07 Fri

- Finished the training on the SAGE node with the PTZ cameras
- The training is very slow but the model is able to learn from the images.
  - the training is in fact 10 times slower than a dell blade with a T4 GPU
- Verified the model learns the same information as the model trained on the dell blade

### 06/06 Thu

- Presented the clusterization results at the team meeting
- Team agreed to give me more nodes with the PTZ cameras to collect more data
- Docker container works fine on the SAGE node with just the training part

### 06/05 Wed

- Finished the interpretation of the clusters
  - the two clusters represent the day and night images
  - there are some smaller clusters inside the big "day" cluster but didn't find a meaningful interpretation
  - Lack of enough image is a problem for the model to learn
- Started to work on training the model on a SAGE node with limited resources
- Has to modify the dockerfile to accommodate the different versions of GPU drivers on the SAGE node

### 06/04 Tue

- Finished the clusterization of the embeddings
- tSNE plot shows that the embeddings are well separated with two clusters
- Started to work on the interpreting the clusters
- Worked on the refactoring and adding embeddings generation functions

### 06/03 Mon

- Generated the embeddings for the saved image dataset for both target and context encoder
- Started to analyze the embeddings with clusterization
- Refactored the code for modularity and readability

## Week 05/27 -- 06/02

### 05/31 Fri

The dockerfile for the job has some issue when running on dell blade and saving data.
I rewrote the dockerfile and tested it on the local machine.
The dockerfile will now work more like an environment rather than a standalone job.
Started the job on a dell blade and it's running fine.

### 05/30 Thu

Got access to the Dell blade and some nodes.
I transferred data from local machine to the remote nodes.
Started to run the code on a remote node but had some errors.
I will try to fix it tomorrow. Had the group meeting.

### 05/29 Wed

Attended the second orientation. Had more discussion with Dario about the project.
Regained access to ANL computing resources.
Setting up the environment and checking data.

### 05/28 Tue

Official first day. I attended orientation, and catch up with the team about many projects.
Started to talk more about the project with Dario.

- Project detail: I-JEPA + DayDreamer + Federated Learning
- Data collection equipment: Axis and Hanwha cameras running on a wild SAGE node.
- Computing hardware: Jetson Xavier NX on a sage node and T4 GPU on a dell blade.

### 05/27 Mon

Memorial day.
