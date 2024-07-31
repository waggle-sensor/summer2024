# General Information
This folder contains the model training file and the dataset it was trained on. The model itself is too big to put on here, but the model basically is able to decide whether an image is clear sky, 0, or other, 1. The dataset it was trained on contains image file paths and their corresponding label. 

The model performed really well scoring 98% test accuracy with precision and recall both above 97% for both classes. There is currently no inferencing function for the model, because it was not fully complete to our liking. We wanted to use LiDAR data to seperate the other class or 0 class into more descriptive classes, but were unable to do so. 

## How To Get Data
The images are located in /lcrc/project/waggle/summer_projects/summer2024/ruben_abraham. In this folder, there is a file called "clear_model_dataset.zip."

You can download it like this.
```sh
scp your_username@lcrc.anl.gov:/lcrc/project/waggle/summer_projects/summer2024/ruben_abraham/clear_model_dataset.zip /your/local/path/on/computer
```

Once you extract the file, you can find the "0" class folder containing clear images, the "1" class folder containing other images, and the "allday" folder containing all of the images. The model I trained on this dataset is also located in the "ruben_abraham" folder and named "resnet50_clearsky.pth."

You can download the model like this.
```sh
scp your_username@lcrc.anl.gov:/lcrc/project/waggle/summer_projects/summer2024/ruben_abraham/resnet50_clearsky.pth /your/local/path/on/computer
```
## How To Run The Model Training Script
In order to run the script, you must have updated the "labeled_paths.csv" file with the correct image paths on your local machine. 

In the "labeled_paths.csv" the file paths are for my local machine, but the paths will look similar on other machines. The file paths in the file are currently like this

/teamspace/studios/this_studio/0/1712692813650778909-sample.jpg

Once you download the images, you would have to update these paths using a script. The end would look similar to this

..../0/1712692813650778909-sample.jpg

Once the csv file is corrected, then you must update the file path in "clearsky.py" itself to the corrected csv file. Then, you can run the model training script.




