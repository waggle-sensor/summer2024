# Intro 
Hello! My name is Ryan. I am a rising junior studying computer science at the University of Dallas. This summer I am working on an image searchability feature inside of the SAGE/WAGGLE portal. This would be useful so that, when a user looks up a feature such as: "groundhog", they can see all of the images with that feature.
# June 3rd, 2024
Began learning PyTorch and AI fundamentals
# June 4th, 2024
Started on Microsoft PyTorch training courses and started reading papers regarding image sparsification
# June 5th, 2024
Finished Microsoft training course and made notes on image sparsification papers. Began reading about OpenClip
# June 6th, 2024
Played around with OpenClip and wrote most of a paper in LaTeX about it. Tried to do image -> text and text -> image
# June 7th, 2024
Finished paper, had a meeting, and looked at ImageBind. Realized I need computing power and will begin to use the ANL computing resources available. 
# June 10th, 2024
Was onboarded with the HPC systems. Still need to learn how to work them. Also tried to work out how to get OpenCLIP to figure out what is inside an image
# June 11th, 2024
CLIP does not pay attention to specific details within an image, only the image as a whole. This means there has to be a way to classify little components. First, I tried to split all of the images into 16 block segments. Sadly, this means it cuts some of the critical peices and confuses OpenCLIP. I decided that I need to do feature segmentation. That first led me to "GroupViT" but after a lot of trying, their code is just broken and big. I am now trying to use MS COCO with PyTorch--maybe OpenCLIP would help too. What would be great is to use OpenCLIP but force it to do feature segmentation by looking really hard. OC is really lazy and thinks clouds are trucks with 90% certianty so I'm not sure what to do with that. Also when I put in "there is a small little unicorn in this picture" it returned 3 SAGE images. I didn't see any unicorns.  
# June 12th, 2024
Tried to use DeepLabV3. It only segments by objects as a group rather than individually. This made it really hard to see what was actually happening at the specific level that is needed. I took those segments and gave it to openClip to see if it could gather useful information. It worked better than just OpenClip alone but was very slow
# June 13th, 2024
Today, I discovered YOLOV9. It is very fast and, with some finetuning, could be exactly what we need. 
# June 14th, 2024

Playing around with YOLO. Trying to make it detect smoke, animals, and emergencies better

![Ryan's Board June 14th 2024](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3621.jpg)

update: I was able to use YOLO with OpenClip. Found a dataset with smoke and tested it. I need to find more datasets or just start training my own. Might do it this weekend. Probably not though. 

# June 17th, 2024

Goals for today: 

Prepare for a metting with Sean and Dr. Park about what to do with deploying MM at the edge. I will try to use the Oregon SSH portal and see if that works. Hopefully it does. Then, I will look into Image Bind again and test it out on my laptop since it has a GPU. 

Depending on what is said during the meeting will determine the rest of the day--and proably the week. I know I will still need to learn Docker and most likely find or make models for the edge. Both also seem like useful things to know. 
![Ryan's Board June 15th 2024](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3626.jpg) 


AFTERNOON UPDATE:

I had the meeting. It seems like the goal right now is to make a simple version of what will be created later after the proposal Sean is putting together. I tested out what OpenClip captions when I input a picture that might come from a Sage node with what we are looking for (fires, crashes, etc). The results are not always the best... I think I might need to train it? The good news is that the predictor works pretty well--at least with minor testing. So that may be the best option right now. 

![Wrong Caption...](https://github.com/waggle-sensor/summer2024/blob/main/ryan/images/generated_captions/CAPTIONED1718653118.jpg) 

I tried to put Image Bind on my laptop but something keeps going wrong. It works on my desktop though so I will maybe just transfer everything manually. Or make it work. 

The Blade node still does not have internet. Hoping that that comes soon. I will play around with Docker when that works. 

![Ryan's Board June 17th 2024 AFTERNOON](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3627.jpg) 

# June 18th, 2024

Today I am going to make two programs: One with automatic captioning done by OpenClip and one with automatic matching,  also done by OpenClip. Hopefully this will give a good showcase of the best options. I may put together a PPT slide but I can work out the logistics later. I also want to try out ImageBind to see if it is any better. It would help with MM. If I have time I may invesitgate audio to text/image generation. If the network is still down on the Blades, Docker may have to wait again. 

![Ryan's Board June 18th, 2024 MORNING](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3631.jpg)


Afternoon update: I figured out my ImageBind problems are just a bunch of dependency issues. I made a PDF/PPT of what OpenClip says and does. It doesn't do things too well when it comes to complicated images. I did a lot of code cleaning and making things work more properly. I also checked out how to fine tune OpenClip--I don't understand it but I will learn if the time comes. 


![Wrong Caption 2...](https://github.com/waggle-sensor/summer2024/blob/main/ryan/images/generated_captions/CAPTIONED1718744313.jpg) 


I have a feeling that time will come.... 

![Ryan's Board June 18th, 2024 AFTERNOON](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3634.jpg)

# June 19th, 2024 

Today I will be working with new models to see if they can detect important things from the SAGE nodes. I am also hoping to finally get imageBind to run. By the end of the day (ideally) I want to have tested all 3 different models with SAGE data and determine which one is the best, or, which one is the best for individual cases. We will see how that goes. Hopefully only a few things break along the way. 

![Ryan's Board June 19th, 2024 Morning](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3642.jpg)


Afternoon update:
I tested the models. LLaVA works great with a few minor modifications. It is actuallly so good right out of the box I wish I saw it sooner. I will present about it tomorrow. It took about 6 hours today to get to the point where it works on my machine. It was worth it. 

![Ryan's Board June 19th, 2024 AFTERNOON](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3647.jpg)


# June 20th, 2024

Today I am going to make a small demo of LLaVA and see if I should put it in my presentation for the meeting. I may just showcase how well it works. It classifies an ambulance as a firetruck; I am hoping that is one of the very few problems it faces. Overall it should still be good enough.     The one thing that worries me about LLaVA is the size. It runs well but its about 12 gigs. We may have to do some random cutting or soemthing. Not really sure how that will work yet. 

![Ryan's Board June 19th, 2024 AFTERNOON](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3649.jpg)

Afternoon update:

Had the meeting. Thinking about using Aristotle's 10 categories to make an image searcher. Waleed found TroL which seems better than LLaVA. Will update about that tomorrow

![Ryan's Board June 20th, 2024 AFTERNOON](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3653.jpg)

# June 21st, 2024

Today I am going to work with the TroL model and see if it fits on the node. It was released 3 days ago and is incedible at captioning. My laptop can almost not handle it so I may try to use it on the blade. That will get me familiar with Docker as well which is probably something I need to work on anyway. I am still thinking about prompt engineering in a way to get TroL (or LLaVA) to output an explanation with Aristotle's 10 categories. I think this would help as a search capability. I'll try to have a decision by the end of the day for that. 

![Ryan's Board June 21th, 2024 Morning](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3656.jpg)

I *almost* made a dockerfile work today. Technically it does work but it just doesn't run right. I'd say that is a win. Orin is blocking me from using docker right now and that is being resolved. I just tried to make the docker image on my computer so that, when the time comes, I can just load it up. It almost worked. But on Monday it will work! (I hope). After that is done I can move into the more fun logistics of making a basic search thing and a basic find thing. What "thing" is in this case I am still not sure. Hoping to present both demos on Thursday though. It depends on how much effort I drill into this. If things work right at a rate of 85% I think it will be okay.


![Ryan's Board June 21th, 2024 AFTERNOON](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3657.jpg)



# June 24th, 2024

Today is the day docker finally works. It will work. After that I will try to load it on Orin if they allow me to use docker. If that still does not work I will just keep using and modifying the code locally until I think it will be suitable. Then, at some point before Wednesday, I will load it onto the node and just let it run. It would be nice to somehow add gradio to it so I can get some GUI to show it off. If not CLI works fine too.


![Ryan's Board June 24th, 2024 Morning](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3660.jpg)

UPDATE: Docker works! It is now just a problem with the old CUDA version on the blade. However, I did make some major adjustments to the code so I will have to redo the dockerfile. That's ok because I know what I am doing now. I made a script that takes in SAGE images (with a user login) and makes a JSON file with it. My plan tomorrow is to take all that info and make a search function for it. Maybe with elastic search? I am not too sure yet. Will post the code tmwr--it is in another directory right now.

![Ryan's Board June 24th, 2024 Afternoon](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3661.jpg)

# Jun 25th, 2024

Today I have Orin access. This means I can play around with docker again. I hope that they have a compatible CUDA version. I will make searchability work and maybe try out a real time search just to see. I think first I will start off with CLI but then switch to do a really simple GUI version of what I am working on if that is needed. I'll see how the day goes and the problems I run into. 

![Ryan's Board June 25th, 2024 Morning](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3664.jpg)

Today I worked with ORIN but, due to the low CUDA version, was unable to build the docker image. I tried for a few hours in the morning to get it to run but to no avail. In the afternoon I finished building my search code (at least the early prototype) my code is now in the github. It can search based on "fuzzy search" (which isn't that good) or it can search with an LLM. That is better but not super prompt-engineered yet. Some good things to show for the meeting on Thursday. I will keep working on it. Also, I learned a little bit about gradio. I think it may be nice to have for the demo so I will keep plugging along with that in the morning. I do not know how I will build a dockerfile for all of this. It is going to be massive. Very massive. That is ok thought. I think image searching will turn out at leat 85% well in the end. It will not catch everything -- I already know that (and have false positives) but it is much better than nothing! 

![Ryan's Board June 25th, 2024 Afternoon](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3665.jpg)

# Jun 26th, 2024

I am making a GUI for my search prgoram today. This will give some nice abstraction to the code--making it easier to import to other places--and create a nice demo along the way. I need to do better prompt-engineering today as well in order to get the best results possible. Then, I will check out the Blade to see if it has an updated version of CUDA on it--or ask about it if it doesn't. Then, if I have time at the end of the day, I will start to remove the unecessary stuff from my dockerfile to make it smaller and faster to build. That may become a Friday thing though. 

![Ryan's Board June 26th, 2024 Morning](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3668.jpg)

AFTERNOON:
Got sidetracked with Florence-2. Not really side tracked but used all day because it is much better than TroL. And much much smaller. I made a search program for it. It is very much a prototype but it is good enough as a protoype. I think it may work on the node as well? I wish there was more time today to figure that out. Working on the GUI demo now that I have everything that I need. Should take only about an hour I hope. If there is still time before the meeting I may try a tiny version on the node? We will see. 

![Ryan's Board June 26th, 2024 Afternoon](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3669.jpg)


# Jun 27th, 2024

The goal for the morning is to finish up the presentation. The goal for the afternoon is to deploy some kind of prototype onto the node. Should be good. I will have a much better description in the afternoon. 

![Ryan's Board June 27th, 2024 Morning](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3672.jpg)

I spent most of the mornning working with gradio and making a demo and presentation for the meeting. All of it was good. I spent some of the afternoon writing my abstract and will review it tomorrow. I am still trying to think of the best way to make all of the info searchable. Chris reccomended that I try out making the user select things I want them to select rather than letting them roam free with a blank "type anything" box. I think that will be the fastest way to do things. There may be a way to do a little bit of both but it is probably the best start I have. Tomorrow I am going to make a dockerfile and try it out on ORIN or a node -- just to see. I will also reformat my JSON file to fit what I want it to do just a little more (with caption to phrase grounding). I would like to get as much of this done before July as possible. 

![Ryan's Board June 27th, 2024 Afternoon](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3677.jpg)


# Jun 28th, 2024


Today I am going to make a dockerfile and run some tests with Florence on the node and/or Orin. Before that I will make some slight changes to the JSON file and try to also find a way to redirect the localhost gradio so that I can see it on my computer. I don't know how that works but I heard it is possible. 

![Ryan's Board June 28th, 2024 Morning](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3678.jpg)

Good day -- will update blog about it Monday

Friday went well. I was able to put Florence-2 onto the blade and get it running the demo I made. It is slower than my computer which is interesting. Not slow enough to cause concern though. Everything is progressing. 

![Ryan's Board June 28th, 2024 Afternoon](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3679.jpg)

# July 1, 2024

Since docker and Florence-2 seem to be working together, I am going to write a script in order to deploy it on a node--just to see what happens. Hopefully nothing gets destroyed in the process. To make this script I will put together a gui interface. This should help Neal as well so that he can test the model out. Once that is done I will keep imporving the search and make it easier. If we have a meeting on Wednesday I may have a demo. Sean mentioned that there is a way to link VS code with Docker and SSH all in one. That would be awesome. I am going to try that out.

![Ryan's Board July 1st, 2024 Morining](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3692.jpg)

Docker on the node is brutal. I think it itself is an AI machine who has the goal of destroying all moral and like for Docker. Every move I make it knows exactly how to break it. But it will be defeated. If not I'll just find another way to do what I need to do. More on that tomorrow I hope. 

![Ryan's Board July 1st, 2024 Morining](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3693.jpg)

# July 2, 2024

Today is a continuation of yesterday. I will hopefully have Florence up and running on the node. I am thinking, if it doesn't work the way I have it right now, to instead deploy a little tiny CLI version. That would be a lightweight and effieicnt for a prototype. I will try to get everything working though. I think I am sure I can get Ollama working pretty easlily so that shouldn't take too long

![Ryan's Board July 2nd, 2024 Morining](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3695.jpg)

Endded up getting the node to run Florence-2 on the CPU. That was good. It seems that the CUDA version is too old for the pytorch version that I need. If I have time, I will try to deploy the NVIDIA GPU version on V001 tomorrow if I have time. I was also able to get Ollama up and running. It was very slow. It took about 13 minutes for it to determine what was going on in an image. I think Florence is going to win the race for what we need to do. I will check out all of the CPU and memory usages. In terms of CPU time on Florence it runs under a minute. Stil very slow but faster. Will try to run Dario's LLava version on it too. If I had more time today I would have done all of these things but I kept running into strange container issues with everything. Should be still on track

![Ryan's Board July 2nd, 2024 Afternoon](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3696.jpg)

# July 3rd, 2024

Benchmarking on the nodes is the number one priority today. Especially before the presentation. If something goes wrong, even having a rough estimate of what to expect would help. I will try Ollama's LLaVa and Florence. If there is time I will try LLaVA by itself. 

![Ryan's Board July 2nd, 2024 Morining](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3702.jpg)


I was able to deploy everything and it seemed to work well. I ended the day by reformatting my files in my github to make it easier for useability. I hope to add documentation to everything as well so it's not a complete mess. 

![Ryan's Board July 2nd, 2024 Afternoon](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3703.jpg)

# July 5th, 2024

I will continue to improve my codebase so that it can be read and understood by people. The goal within the next few days is to have READMEs and comments on my code so they can be forked and modified with ease. 

Next week I will get back to imporving the code/dockerfile, making a better search feature, and adding important features for blade and node search functionality. 

# July 8th, 2024

As I am going along, I may contunue to make adjustments to my code. I think it is better to imporve as I move so that I don't have to go back and fix things every other week. The main goal is to turn the code into a more usable prototype so that it can be implimented without many issues. I will also benchmark the power/memory usage. I did this on Wednesday but only briefly. I would like to create a more consitent showcase so that it can be proven that one LLM is better than the other. 

![Ryan's Board July 8th, 2024 Morning](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3726.jpg)


Today I loaded Gemma-2 onto my laptop and tried a prototype of search. Seems to be going ok. The Blade stopped working so I can't make too much real progress until that gets fixed. I can still do some stuff locally. All going well. Still trying to think of what should go on the blade and what should go on the node.

![Ryan's Board July 8th, 2024 Afternoon](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3728.jpg)


# July 9th, 2024

While the Blade is still down I am going to try to completly containerize the huggingFace model on the node to see if that speeds up deployment. It would be nice if it does. I will also make a diagram or two to show what the eventual end goal is. I think that will help in the Thursday meeting. 

![Ryan's Board July 9th, 2024 Morning](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3729.jpg)

The nodes are now all down. I continued to test Ollama with Gemma and Florence-2. I also fixed some docker problems and got the hugging face model to run locally. I also made a chart to show a possible plan for Sage Search. My hope is that by the afternoon the nodes will be back up.

![Ryan's Board July 9th, 2024 Afternoon](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3732.jpg)

# July 10th, 2024 

Nodes are still down :( I could work on my poster and presentation but will probably do that early next week when I have some nice graphs and information to present about the nodes/blades. For now I will figure out the things I can do on my laptop that I know will work with the system. If I knew about what was going to happen I would have made sure to do everything with the nodes and blades earlier in the week. That is ok though. There are still things to do. 

![Ryan's Board July 10th, 2024 Morning](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3733.jpg)

Just made a slack bot after a long time of not knowing what was going on. It runs Gemma via Ollama. Whohooo

![Ryan's Board July 10th, 2024 Afternoon](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3735.jpg)

# July 11th, 2024

I am going to make the presentation for the meeting and show where all of the information is coming from (and is going to). I will also keep checking the node status and possibly put the slack bot into a dockerized container. 

![Ryan's Board July 11th, 2024 Morning](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3737.jpg)

Nodes are kind of back up. I deployed ollama on a docker container and shipped it onto the blade. I also shipped it to W0B5 but running into some small problems. A lot fo things are happening now

![Ryan's Board July 11th, 2024 Afternoon](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3739.jpg)

# July 12th, 2024 

Today I will try to get the Gemma2 Ollama working on the node, and see if a full demo can be set up. I will also try to just ship a full ready-to-go container and see what happens. In addition, if I have time, I will stress test the node deployment and figure out the output tokens/second.  

![Ryan's Board July 12th, 2024 Morning](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3743.jpg)

A lot of good things happened today. I think I am eventually going to move on from Gemma as a search LLM and stick to a normal algorithm. It is 11.4 gigs total and doesn't seem to run on the nodes. It is way too much. Here is what I need to work in total: slack-bot--blade--node--Florence-2--isFit--blade--slack. right now I have bits and peices of all of these but have yet to combine it. I should probably run actual tests at somepoint since I am doing a lot more building than testing. That may be an issue in the future. I hope everything will come together next week in larger components

![Ryan's Board July 12th, 2024 Afternoon](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3744.jpg)

# July 15th, 2024

I am going to stay on the hunt for a better search algorithm rather than relying on Gemma-2. I think I saw a few things floating around but have yet to check them out. The primary goal of the day is to chart all of the power usage on W0B5 and W0B4 (Florence-2 and LLaVA) as well as make an output comparison. It would be great to get that done so that I can throw it on my poster as well. Tomorrow, the goal will be to make the poster and presentation.

![Ryan's Board July 12th, 2024 Morning](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3753.jpg)

Solid progress on generating output tokens per second. Will try to make graphs tomorrow morning 

![Ryan's Board July 12th, 2024 Afternoon](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3759.jpg)

# July 16th, 2024

I am *actually* going to do testing today. Then I will put all of it in my poster/presentation this afternoon and tomorrow. Today's goal is trying to get all of the good pictures and screenshots to show what I have been doing. 


![Ryan's Board July 12th, 2024 Morning](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3762.jpg)


Testing in progress. Poster also in progress. Will be done by 10:00 am tomorrow!

![Ryan's Board July 12th, 2024 Afternoon](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3763.jpg)

# July 17th, 2024

Final crunch time for poster and presentation. The data is coming in which is good! I'll just parse it out and put it in. Then, if I have time, I'll keep working on the slackbot. 

![Ryan's Board July 12th, 2024 Morning](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3766.jpg)

AFTERNOON: No need to show board still working on the presentation and fixing up the poster a little bit. Should be back on track with integration after it is finished. Still crunch time :) 

# July 22nd, 2024

Just need to present and work on the slack bot. Will start updating board this afternoon

# July 25th, 2024

Having to delete all of the API tokens to git push is really annoying. I think that is why I haven't been updating the blog because I don't want to delete it every time . The problem is that if I accidentally push an API token, VS Code gets really angry and I have to git revert and do a lot of stuff that takes up time. There is probably a better way than having to delete and push. Maybe if I use a .txt file and read from there. But then when it comes time to push on the node I don't know what a good "secret" solution is. Unless, maybe, we had the tokens hidden on the sage site and it would be allowed to ping. I don't know. Anyways, today I have to make a presentation for the meeting and put a few things together. I would really really like to get Florence working finally as a plugin. That better work by the end of the day. If not, I will just keep working on it over the weekend because it's annoying that it hasn't worked right out of the box. Hopefully good things to come. 

AFTERNOON:
The node is still really slow but I was able to get slack to get images from the server so that is a plus. Almost there

# August 5th, 2024

Last week best week. 