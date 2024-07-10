# Summer 2024 Blog

## 05/28/2024
It's my first day! My day started with orientation from 9-12. After that, I met my team for the first time! Following lunch, I met with my mentor Yongho to learn about my project--working on resource management in the DAWN project. I spent the rest of the afternoon getting through onboarding documents and starting to dig into the project.

## 05/29/2024
My second day was just an onboarding day. I started the day with orientation from 9-12. Then I set up my Google Drive and Github folders for storing my work this summer. I finished the day with more required trainings.

## 05/30/2024
Today I finished up the required trainings! After that, I was able to talk through my design with Yongho. We made sure to resolve any confusion and align on the project. As of now, our current plan of action is to create an ansible playbook that setups an individual Jetson Nano for local performance metrics. This is currently missing from the current Waggle stack. Several of the pieces are there, but they are scattered throughout the code base. With a uniform setup, we have a playground where we can test various things like analysis tools for an eventual deployment to the Waggle stack. I finished off the day by provisioning a Jetson Nano to start working on my project.

## 05/31/2024
Today I began working on my project! The first part of the project is to write an ansible script that sets up a Jetson Nano for logging. Most of this script has already been written, but it is scattered in various places within several codebases. My job is stitching all of these pieces together into one uniform script. I began today in the Charon project. It is a project that is being developed to watch performance metrics on HPC systems. This means that there is a lot of overlap with my project! The ansible script I wrote today sets up Kubernetes and local storage for Grafana! As I work through writing this script, I need to deploy the Grafana dashboard and metrics scraping tools. I also updated my design document that contains my current thoughts on the project to align with the conversation that Yongho and I had yesterday. So far, I think I'm off to a good start! This is the end of my first week, and I've enjoyed working at Argonne a lot!

## 06/03/2024
Today I continued to work on my Ansible script. I added the rest of the code needed to set up the Grafana operator and agent. I then attempted to run it on the Jetson Nano. I say attempted because the Nano had a much older version of Ansible installed. I spent my day back porting the script to an older version of Ansible. After resolving all of these errors, we found out the the memory capacity of the Nano isn't enough to run the entire Grafana stack with Mimir included. So, I spent the rest of the day cleaning up code while Yongho attempted to get a Jetson NX.

## 06/04/2024 
Today I attempted to run my script on the Jetson NX. The way we had initially planned to do this was to run it locally as a localhost. However, I was stuck with an even older version of Ansible on the NX. Instead of porting the script once again, Yongho and I decided to set up a local network to run my script. This involved a little bit more porting. We had to figure out how to remotely connect to a host through an inventory and then resolved several minor errors that had gone unnoticed until now. I ended the day with Pete's retirement event where I got to spend some more time getting to know the others on the team!

## 06/05/2024
I finally got the ansible script running today! This meant that I was able to take a clean Jetson NX and run the script to set up the grafana agent and scraper. The final issue that I ran into was the exporting of tegra stats. This is a built in command provided by NVIDIA to monitor various performance statistics on the device. There is an existing waggle pod that exports this to the mimir storage. However, this has configuration for a waggle node that isn't necessary for a blank box like this one. In fact, having this extra configuration hinders the deployment of the tegra stats pod. So, by porting this over, we were finally able to have a working pod.

## 06/06/2024
Since, we are done with the ansible script, it is time to start thinking about the next part of the project: modeling the system. We want our model to accurately represent a possibly complex system that takes the certain state of the device--cpu performance, gpu performance, etc--and returns the estimated power usage by these devices. One way to go about this would be to try to design a mathematical model of the system. However, we don't truly know what kind of system to expect without any data. Another approach is to design a machine learning model that represents this. Under the hood, these two ideas are fairly similar. One just has a much simpler closed form solution while the latter is an approximation of this. Regardless, we need data to start approaching either one of these problems.

Now, to gather this data we want to run programs and measure all of these pieces of data (performance and power usage). However, we don't have enough existing programs in the sage/waggle ecosystem to do this. So, we need to simulate what a program might look like. We can treat a program like a black box that uses some set of resources R at a time t. So a program is simply the collection of the pairs {(R, t)}. Since we don't actually care what the program does, we just need a way to vary R over various times. We can do this with a generic stress program that randomly stresses the resources R. 

## 06/07/2024
Today I began looking at the existing infrastructure in the waggle ecosystem for testing nodes. Currently, there are existing docker images that stress all sorts of resources (cpu, gpu, ram, storage, etc). Each one of these is spun up in a separate pod and stresses the resource to either a specified amount or a maximum amount. Since we want to vary the level of stress, we need some finer control over these stress tests. Furthermore, we want to be able to combine them into one pod. Since cadvisor scrapes metrics per pod, we need to launch all of these in the same pod to properly simulate a program that is running. So, with the rest of my day I started working on that.

## 06/10/2024
I spent my morning working on combining the cpu and gpu stress tests into a single pod that could be launched. For the cpu, we are using stress-ng, a well known stress test with lots of fine control over cpu utilization. However, for the gpu, there is no such equivalent. I started by evaluating a program called gpu_burn. However, with this, we get no fine control over the utilization of the gpu. Instead, it pushes the gpu to 100%. To work around this, I'm planning to try adapting the simple waggle gpu stress test to vary the gpu stress randomly. To do this, I plan on adding small amounts of sleep in between the matrix multiplications in the test.

I ended the day in a meeting for the Charon project. First, was an internal meeting in which Akhilesh talked about his work and the previous research he'd done. He pointed us towards a paper that he had written about reducing power consumption in HPC nodes. He talked about the process he used to do that which was all very similar to the project that I am currently working on. The second meeting was with the APS scientists which was really interesting to hear about their research!

## 06/11/2024
I spent most of today reading the research papers the Akhilesh pointed us towards. They were about offline reinforcement learning and reducing power consumption (the paper he wrote). His paper used the technique of offline reinforcement learning to train a control program to reduce power consumption. This was based on a mathematical model that he defined. Now, this seems like a similar approach to what we might ultimately want to do with my project. However, we can improve upon a mathematical model by collecting the data that defines said model. This is the current step that we are working on.

## 06/12/2024
I spent today continuing to look into related research and papers that Yongho had sent me. There is a large body of research focused on energy efficiency and a large body of research focused on the problems that arise in edge computing. However, there is very little research at the intersection of these two ideas. Our work seems to be a start in this area, but performance modeling an entire edge system sounds significantly more difficult. I'm going to start thinking on this.

## 06/13/2024
Today I refactored and cleaned up the code for a generic stress test. I was also able to test it using the gpu-stress-test docker container. Since this already has torch installed, I was able to work around my previous issue of not having torch. This seems to work as intended, so the next step is working on how to pull this out into a tool. This will involve constructing a docker image and writing a kubernetes job for it!

## 06/14/2024
Today I wrote a dockerfile and began testing it. It was fairly simple to write, considering it is based mostly on the gpu stress test dockerfile. I also reused the github action of building and pushing a docker image to docker hub. However, it turns out that this image only works when the dockerfile is at the top level of a repository (mine was not). This means I will have to refactor the project slightly.

## 06/17/2024
Today I worked on a few different things. For starters, I migrated the stress code to a new repo called stressme. With this, the Dockerfile sits at the top level of the container, and we can use the waggle build and push github action for docker containers. This saved me a lot of work reinventing the wheel. Now, in this process, I discovered a few bugs, but ultimately, I was able to build and push my docker image. In this, I ran into another problem. This image doesn't allow me to import pytorch. I'm not sure why that is yet, but I will have to look into it more tomorrow.

The other thing I began working on was the data pipeline from Grafana to what will eventually be a model. Grafana displays data nicely, but I can't manipulate it with something like a machine learning model. So, we can query the Grafana api for data to manipulate locally. I began playing with the api to get a feel for it.

## 06/18/2024
Today I worked on debugging the pytorch issue within the image. The solution to this issue is running a container with the nvidia container runtime. We can do this in Docker using the --runtime flag, but there is not an easy equivalent in Kubernetes. Today, I worked on installing the nvidia runtime container and setting it to the versions that are in the waggle production. We were able to specify the nvidia runtime, but it had no cuda libraries within it.

## 06/19/2024
Since we are blocked on the kubernetes runtime issue, I spent the day looking into various machine learning techniques that we might want to apply to our data. Remember that our ultimate goal is to predict the power consumption of a program from other metrics such as cpu and gpu utilization. I started by looking at the pytorch solution to the mnist problem. This involves a CNN to classify images. I also spent the day reading up on various pieces of theory such as convolutions, transformers, etc. Seongha recommended that we use a timeseries transformer predictor. 

## 06/20/2024
I spent most of today reading and editing Yongho's paper. It explains some of the foundational work he has done in building a performance metrics system for waggle. This includes the jetson-exporter and his sidecar container. We also made progress on the cuda container issue. As we expected the issue is with the runtime choice. To specify this in kubernetes, you need to define a RuntimeClass object (which updates the config.toml to use a new runtime) and tag the container with it. I added these various steps to the ansible script for future provisioning.

## 06/21/2024
Today, I tried to run the container after creating the nvidia RuntimeClass object. First, I ran into some issues with pulling the image. Kubernetes fails to pull it due to its size. To resolve this issue, we have to pull with k3s ctr. After, this I tried running the image and still didn't have any cuda libraries installed. 

## 06/24/2024
To get past the roadblock of the nvidia container issue, we decided to run the stressme app I developed on a sage node. We decided to run it on W023 (at the main gate) to start gathering some data. This meant that I needed to start looking at the sage data client to pull my data. 

## 06/25/2024
I continued working with the sage data client to pull data and eventually formatted it in a way that was usable to me. I'm not super familiar with pandas so it was a fun opportunity to try it out! We ran into a weird issue with my app that caused it to not terminate on the sage node. The cpu stress of my app is provided by stress-ng. If you run it with less than a second passed as an argument, it won't terminate.

## 06/26/2024
I continued to work with the sage data client and added more filtering options to supplement the fairly simple sage data client. Yongho also resolved the issue with nvidia container issue. To solve it, we upgraded the nx to use jetpack 5.1.2 and had to use a new base container image.

## 06/27/2024
Today I started trying to define a model that could predict my data. I started with the mnist example that I received from Yongho. I simplified the model structure to a simple feedforward network and customized it to use a pandas dataset. I then tried classifying data, but the model didn't converge. Despite this, I had a relatively high accuracy. This doesn't seem right, so I'll need to dig further into this.

## 06/28/2024
Yongho and I are planning to move the mimir and grafana instances off of the NX in order to save resources on the NX. We are getting a laptop to have a metrics instance on.

## 07/01/2024
Taking a look at the data I had gathered, there was not a strong correlation between any measurements except the tegra measurement of cpu utilization and power. Taking a step back, we decided to simplify our data gathering process at least initially. Instead of randomization, we decided to linearly interpolate the data and to add an option to use cpu only.

## 07/02/2024
I spent today splitting up the ansible playbook into a modular design. With this, we can enable or disable various aspects of the system when flashing a new device. This both makes the process more modular and more reproducible. I also continued to look at my data. 

## 07/03/2024
I spent today flashing the laptop and looking at the deterministic cpu data. Once again, the only plots that are correlated are the tegra measurements of cpu and power. This means we need to take a step back and look at our variables once again. We decided to recreate this experiement on the NX instead of on W023. We will try this next week.

## 07/08/2024
I reflashed the NX in order to remvoe the extra bloat that was added to the device. I also tested that the laptop's mimir and grafana instaces were working. 

## 07/09/2024
Today I spent figuring out why we weren't seeing any metrics published to the database. It turns out that we needed to specify the http protocol in the address for the laptop. That is, we needed to turn 10.31.81.129:8080... into http://10.31.81.129:8080. Now, we are getting metrics published! Unfortunately, we aren't getting any tegra metrics published because nvidia changed the format for jetpack 5.1.2. Yongho is working on rewriting the jetson-exporter and then we will have data to look at.

## 07/10/2024
Today I caught up on documentation. I started by catching up on my blog. Then, I started working on starting final documentation to recreate my project from the summer. This includes perf-mon, stressme, and results.