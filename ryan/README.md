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

![Ryan's Board June 26th, 2024 Afternoon](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3668.jpg)
