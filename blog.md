# May 28th, 2024

I worked on finishing all my trainings and Seongha gave me a rundown on what my project would look like. I also brushed up on some Pytorch. 

# May 29th, 2024

I was away at University of Illinois Urbana-Champaign for a registration day.

# May 30th, 2024

I finished all of my trainings and worked on running a few simple models that found online that would help me have a better understanding of what I would be dealing with.
These models identified what images were so if I gave it a picture of a dog, it would return that it was a dog.

# May 31th, 2024

I worked on running a simple pretrained Unet model on cloud cover estimation. It was a bit confusing and I had lots of trouble trying to 
use the pretrained model Seongha gave to me. I worked on that for the entire day with still no good result. 

# June 3rd, 2024

I finished using the Unet model Seongha gave to me on cloud cover estimation. I was able to use it on a couple of my images and I believe it gave back accurate results. Next,
I am going to work on doing the same thing but with resnet models. I will start with resnet50.

# June 4th, 2024

I didn't complete much today as towards the end I realized that I could not find a dataset that had cloud cover images and their corresponding estimation values. I spent most of
the day updating my code so that it could train a model with a dataset that would be downloaded to my computer. 


# June 10th, 2024

I spent most of the day refreshing myself with Pytorch fundamentals and videos. I felt as if I did not have a strong foundation and there were some parts I was forgetting when I was writing code. I continued working on training my resnet50 model on the CIFAR10 dataset. 

# June 11th, 2024

I continued studying and researching machine learning topics. I relearned a lot about how the structure of training and testing a model should go. I also relearned how I shoould load in a pretrained model. I also worked on training the pretrained resnet50 model on the CIFAR10 dataset. It was going well, and I made a ton of progress. I picked a lot of my hyperparameters, based on what I learned, using the CrossEntropyLoss funtion and the Adam optimizer. I made my batch size 64, so that my model can train faster, but I believe this may have made it a bit less accurate. 

# June 12th, 2024

I ran my model, the resnet50 pretrained model on the CIFAR10 dataset. I am basically fine tuning it to images in that dataset. I recieved an 89% accuracy on the test data, meaning the model was pretty good. I noticed though that there was a bit of difference between the training loss and the validation loss by an average of about 0.3500, which could mean that there is slight overfitting. I believe I can fix by augmenting the data meaning adding like random crops, utilizing a learning rate sceduler, and or add some dropout layers. 

# June 13th, 2024



