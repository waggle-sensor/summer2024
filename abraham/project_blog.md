# Using LIDAR to Aid Models in Solar Estimation and Sky Classification

LIDAR technology, with its ability to create detailed maps of atmospheric environments, can potentially solve the issue of blockers by providing precise information about the location and height of obstructions. It proposes many benefits that can’t be offered by a regular camera, especially the fact that it provides accurate data in all different types of weather conditions including fog, rain, and low light. This information can be used to adjust solar irradiance estimates and sky predictions, making them more accurate in any setting. Current models experience difficulties in the presense of blockers and unfamiliar sky conditions. We believe LiDAR to potentially solve this issue and allow us to deploy these nodes in urban areas. 

![Image](/abraham/Images/202203022300.png)

## Problems & Results
A major problem occurred when we were trying to gather solar wattage data. We naturally assumed wattage and irradiance to follow similar 
trends, but we found they shared little correlation with each other. 


<img src="/abraham/Images/solar.png" alt="Solar Image" width="700">


Due to this we looked more into the cloud classification aspect of this research. A sky classification model was built that predicted whether the image was clear sky, 0, or other, 1. Some hyperparameters chosen include ResNet50 pretrained, Cross-Entropy Loss Function, and Adam Optimizer. The ResNet50 model received 98% test accuracy with recall and precision above 98% for both classes.  This is where we encountered our next big problem. We were unable to represent the sky condition in numbers with the LiDAR data, so we chose to just find the correlation or relationship between irradiance data, images, and corresponding LiDAR data. This would help to prove the benefit of LiDAR in predicting sky conditions, and consequently solar data. LiDAR data would help specifically to divide the ”other” class in the sky classification model into more descriptive classes like cloudy, thick overcast, hazy, etc. 




## Conclusions & Future Work
Although a ML model was not created in these 10 weeks, based on the correlation between LiDAR data, image, and solar irradiance data, we can say that LiDAR data is very beneficial in the prediction of sky conditions and the estimation of solar irradiance. It should be used in pair to the images. In the future, we aim to convert LiDAR data into numerical values that represent sky conditions. Solving this issue will allow us to create a dataset and, subsequently, develop a model that incorporates both image and LiDAR data. This model would be able to classify sky conditions and eventually estimate solar irradiance, very accurately.

