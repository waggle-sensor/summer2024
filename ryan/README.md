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

![Wrong Caption...](https://github.com/waggle-sensor/summer2024/blob/main/ryan/images/generated_captions/example%20_images/CAPTIONED1718653150.jpg) 

I tried to put Image Bind on my laptop but something keeps going wrong. It works on my desktop though so I will maybe just transfer everything manually. Or make it work. 

The Blade node still does not have internet. Hoping that that comes soon. I will play around with Docker when that works. 

![Ryan's Board June 17th 2024 AFTERNOON](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3627.jpg) 

# June 18th, 2024

Today I am going to make two programs: One with automatic captioning done by OpenClip and one with automatic matching,  also done by OpenClip. Hopefully this will give a good showcase of the best options. I may put together a PPT slide but I can work out the logistics later. I also want to try out ImageBind to see if it is any better. It would help with MM. If I have time I may invesitgate audio to text/image generation. If the network is still down on the Blades, Docker may have to wait again. 

![Ryan's Board June 18th, 2024 MORNING](https://github.com/waggle-sensor/summer2024/blob/main/ryan/RyanBoard/IMG_3631.jpg)
