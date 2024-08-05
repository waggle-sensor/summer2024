# May 28th, 2024
I worked on finishing all my training, and Seongha gave me a rundown on what my project would look like. I also brushed up on some PyTorch.

# May 29th, 2024
I was away at the University of Illinois Urbana-Champaign for a registration day.

# May 30th, 2024
I finished all of my training and worked on running a few simple models that I found online that would help me have a better understanding of what I would be dealing with. These models identified what images were, so if I gave it a picture of a dog, it would return that it was a dog.

# May 31st, 2024
I worked on running a simple pretrained Unet model on cloud cover estimation. It was a bit confusing, and I had lots of trouble trying to use the pretrained model Seongha gave to me. I worked on that for the entire day with still no good result.

# June 3rd, 2024
I finished using the Unet model Seongha gave to me on cloud cover estimation. I was able to use it on a couple of my images, and I believe it gave back accurate results. Next, I am going to work on doing the same thing but with ResNet models. I will start with ResNet50.

# June 4th, 2024
I didn't complete much today as, towards the end, I realized that I could not find a dataset that had cloud cover images and their corresponding estimation values. I spent most of the day updating my code so that it could train a model with a dataset that would be downloaded to my computer.

# June 10th, 2024
I spent most of the day refreshing myself with PyTorch fundamentals and videos. I felt as if I did not have a strong foundation and there were some parts I was forgetting when I was writing code. I continued working on training my ResNet50 model on the CIFAR10 dataset.

# June 11th, 2024
I continued studying and researching machine learning topics. I relearned a lot about how the structure of training and testing a model should go. I also relearned how I should load in a pretrained model. I also worked on training the pretrained ResNet50 model on the CIFAR10 dataset. It was going well, and I made a ton of progress. I picked a lot of my hyperparameters based on what I learned, using the CrossEntropyLoss function and the Adam optimizer. I made my batch size 64 so that my model can train faster, but I believe this may have made it a bit less accurate.

# June 12th, 2024
I ran my model, the ResNet50 pretrained model, on the CIFAR10 dataset. I am basically fine-tuning it to images in that dataset. I received an 89% accuracy on the test data, meaning the model was pretty good. I noticed, though, that there was a bit of difference between the training loss and the validation loss by an average of about 0.3500, which could mean that there is slight overfitting. I believe I can fix it by augmenting the data, meaning adding random crops, utilizing a learning rate scheduler, and/or adding some dropout layers.

# June 13th, 2024
I spent more time researching how to get images and corresponding data from the Waggle node W01B. I converted the data that I got into their respective CSV files, one for images and another that held the irradiance values. Now I will try and figure out how to take the wanted values from each CSV file and merge them together, all while finding the irradiance values that closely match the timestamps of the images taken.

# June 14th, 2024
I spent some time reading up on documentation and tutorials on how to merge these files. I ended up succeeding, and I got a file with some images having their corresponding irradiance values. I don't know why the other images don't have their respective values, but I will figure that out later. I am also trying to figure out how to get these URLs into actual images that I can download to my computer.

# June 17th, 2024
Today I had a meeting with Seongha discussing the goals of this project and how soon I should finish them. I then worked on downloading the images using a script that I created, but it always said "failed to download." I asked Seongha, and she said to use wget and the terminal. I hope by the end of the day, I will have my images downloaded. I want to then train a ResNet50 model on these images. I will have to think about the hyperparameters and parameters I want in order for my model to be accurate.

# June 18th, 2024
I spent today training and testing my model on about 300 images that had their corresponding irradiance values. This small dataset was because I only gathered data for 30 days. Training and testing looked good, showing no signs of overfitting. MAE was also pretty good, but there was a slight divergence towards the end of the epochs. I discussed this with Seongha and discovered I had been using the wrong data. I am supposed to be using the solar charge controller app instead of the solar irradiance one. Specifically, I am using the env.solar.voltage.array data. Now I am downloading a year's worth of data, which is taking a while, and then cleaning it. Once I complete this, I will train and test the ResNet50 model immediately.

# June 19th, 2024
I spent today training and testing the model. I updated some of the metrics and included accuracy. Accuracy is not the best suited for regression analysis, but with a good threshold, it can help. I decided to set this threshold to 5 because I felt that I could accept an error of about 5 between predicted and actual values. I think this is good for a start, but I will probably update it to a smaller number. I trained and tested the model twice today, receiving similar results. These results showed that the model was learning and generalizing well, but they did not meet the standards we wanted. The only thing that would help or help the most would be way more data, but right now that data is unavailable. Now I'll be working on the clear sky classifier.

# June 20th, 2024
I hope to learn more about how I can categorize images in their respective classes prior to training a model on them. I also hope to find some similar models that have already done this type of work so that I can possibly fine-tune them on the data that I have present. I found one model, but it did not train on fisheye images. I don't know whether to use that specific pretrained model or use a pretrained model from PyTorch and start from there. I was notified by Seongha that images from nodes at the Argonne campus were able to be retrieved. So now my goal is back to the solar portion of this project. I have to first find out the conversion rate from irradiance to power.

# June 21st, 2024
I used a simple linear regression model to try and figure out the relationship between the two variables. Nothing proved to be useful, as I received very low R2 scores and MSE, meaning that there was really no correlation between the two variables. I also looked at the graphs for irradiance and power compared to each other and noticed that the wattage was always or generally higher, which is very inaccurate. I thought it was a location problem, so I compared the irradiance and power at the Emiquon node, W01B, and the conclusion was the same. This was very weird.

# June 24th, 2024
Today, I explained to Seongha the problems and information I found from my work on Friday and over the weekend. The conclusion was that there was no correlation or relationship between the two variables. No conversion rate means there is no way I can expand my dataset. I can't convert irradiance to wattage from the tower data.

# June 25th, 2024
Even with the lack of correlation, I continued to work on a model with solar wattage to at least say I did that. This would be much more useful than the solar voltage model I created previously. Wattage is a much better representation of solar irradiance than voltage. I also added some better metrics such as MAE, RMSE, and R2 score to explain the performance of my regression model. Previously, I had used accuracy and a threshold for that, which was very subjective and didn't really make sense.

# June 28th, 2024
I started working on the clear sky classification model. I worked on sorting through all of the daylight sky images into their respective folders. I also designated all of the images that contained blockers into their respective folders. After sorting, I was left with around 500 clear sky images and 2000 other images. I duplicated the clear sky images until I reached a folder size of 2000 images. This made the dataset more balanced and prevented overfitting.

# July 1st, 2024
I worked on the clear sky classification model and tested it. It came out to an impressive accuracy of 98% and recall and precision both above 97%. This showed that my model was predicting and generalizing well. I then started working on trying to plot the MPL data that was downloaded through LCRC.

# July 2nd, 2024
I spent looking through the LiDAR or MPL data and trying to make a script that could read and plot them. There was not much documentation.

# July 5th, 2024
I created a script to read each MPL and create a corresponding LiDAR plot. I noticed that many of the images had errors, not due to the script but because of changes or adjustments to the equipment they used to gather data. It was interesting seeing the different LiDAR plots and the corresponding weather during those hours.

# July 11th, 2024
I spent the last couple of workdays on vacation in Oregon, so not much work was done. I was constantly moving places, and these places didn't have the best service. I spent today just observing different LiDAR plots and matching them to their images. After speaking with Seongha, I want to create a bunch of classes, like cloudy, clear, hazy, and other, and fill them with LiDAR and image data.

# July 12th, 2024
Today we had a meeting with atmospheric scientist Paytsar, where we discussed how we could incorporate LiDAR data into our dataset to train a model. She did not know whether we could take the data and be able to turn it into a set of numbers that would state the sky condition. She suggested, though, that we find the signal strength averages every 5 minutes for each height. I spent the rest of the day trying to do this with the data we had.

# July 15th, 2024
I continued today working on plotting the 5-minute averages of the signal strength. I was able to plot one of the 5 minutes, and after reviewing it with Seongha, it looked correct. These 5-minute averages can tell us easily the sky condition by looking for certain oscillations and the presence of cuts. Cuts, to me, look like the average peaks and then after go straight to 0 or noise. I also started working on the poster and presentation.

# July 16th, 2024
Since I would not be able to create a model using the LiDAR data, Seongha suggested that I focus on getting one example of each sky condition I could find. The goal for the poster and presentation would now be to explain the benefit or importance of LiDAR data in predicting sky conditions. I was able to create one example for clear, cloudy, hazy, and thick overcast conditions. I continued to add and clean my poster and presentation for peer review. I was able to complete them before the end of the day.

# July 17th, 2024
Today I spent all my time cleaning up my poster after listening to all the feedback. I made the writing more concise and clear, deleting any informal words. I also added more details to my images and made them bigger. I also became very sick.

# July 18th, 2024
While I was sick, I submitted my poster and started working on cleaning up my presentation. I didn't want the presentation slides to be just writing, so I cut down a lot of the words, which I could say on my own. I also started working on updating the summer2024 repo and organizing my work.

# July 22nd, 2024
I presented my project today. After this I worked on cleaning up my github and adding to my research report paper!

