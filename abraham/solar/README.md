# General Information
This folder contains the csv file used for training and the model training script. The dataset is comprised of image paths and their corresponding wattage value. The model I trained was a regression model that estimated the solar wattage based on a given sky-face image. 

The model performed alright scoring a r2 score of 0.75. This meant that 75% of the variance in the dependent variable(wattage) was predictable from the independent variables(images). Besides model performance, we noticed unusual behavior with the wattage data as it did not follow the same trend as irradiance throughout the day. It peaked very early in the morning, not at around noon, which is were irradiance peaked and where wattage should've peaked. Due to this, we decided to focus more on the sky classification aspect of LiDAR data. 

## How To Get Data
The dataset images can be found in /lcrc/project/waggle/summer_projects/summer2024/ruben_abraham. In this folder, you will see a zip file called "watt_model_dataset."

You can download it like this
```sh
scp your_username@lcrc.anl.gov:/lcrc/project/waggle/summer_projects/summer2024/ruben_abraham/watt_model_dataset.zip /your/local/path/on/computer
```
Once extracted, it contains the "storage.sagecontinuum.org" folder which contains all of the images I used.

The model itself is also found in the "ruben_abraham" folder called "resnet50Watt.pth." 
You can download the model like this
```sh
scp your_username@lcrc.anl.gov:/lcrc/project/waggle/summer_projects/summer2024/ruben_abraham/resnet50Watt.pth /your/local/path/on/computer
```

## How To Run The Model Training Script
In order to run the script, you must have updated the "img+power||(1).csv" file with the correct image paths on your local machine.  

The end of the file paths will look similar to this.

..../storage.sagecontinuum.org/api/v1/data/imagesampler-top-1738/sage-imagesampler-top-0.3.0/000048b02d15bc6d/1706878815998505681-sample.jpg

Once you update the csv file, you just need to update the filepath for the df variable in the "model.py" script so that you are able to train or run the model. 

