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