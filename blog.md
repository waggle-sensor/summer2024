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
I spent more time researching how to get images and corresponding data from the waggle node W01B. I converted the data that I got into their respective csv files, one for images, and another that held the irridance values. Now I will try and figure out how to take the wanted values from each csv file and merge them together, all while finding the irridance values that closely match to the timestamps of the image taken. 

# June 14th, 2024
I spent some reading up documentation and tutorials on how to merge these files. I ended up succeeding and I got a file with some images having their corresponding irridance values. I don't know why the other images don't have their respective values, but I will figure that out later. I am also trying to figure out how to get these urls into actual images that I can download to my computer. 

# June 17th, 2024
Today I had a meeting with Seongha discussing over the goals of this project and how soon I should finish them. I then worked on downloading the images using a script that I created, but it always said failed to download. I asked Seongha and she said to use wget and use the terminal. I hope by the end of the day, I will have my images downloaded. I want to then train a resnet50 model on these images. I will have to think about the hyperparameters and parameters I want in order for my model to be accurate. 

# June 18th, 2024
I spent today training and testing my model on about 300 images that had their corresponding irradiance values. This small dataset was because I only gathered data for 30 days. Training and testing looked good, showing no signs of overfitting. MAE was also pretty good, but their was a slight divergence towards the end of the epochs. I discussed with Seongha, and I discovered I had been using the wrong data. I am supposed to be using the solarcharge-controller app instead of the solar-irridance one. Specifically I am using the env.solar.voltage.array data. Now I am downloading a year's worth of data which is taking a while, and then cleaning it. Once I complete this, I will train and test the resnet50 model immediately.

#June 19th, 2024
I spent today training and testing the model. I updated some of the metrics and included accuracy. Accuracy is not the best suited for regression analysis but with a good threshold it can help. I decided to make 5 this threshold because I felt that I could accept an error of about 5 between predicted and actual values. I think this is good for start but I will probably update it to a smaller number. I trained and tested the model 2 times today receiving similar results. These results showed that the model was learning and generalizing good, but they did not meet the standards we wanted. The only thing that would help or help the most would be way more data, but right now that data is unavailable. Now I'll be working on the clear sky classifier. 

#June 20th, 2024
I hope to learn more about how I can categorize images in their respective classes prior to training a model on that. I also hope to find some similar models that have already done this type of stuff so that I can possible fine tune them on the data that I have present. 
