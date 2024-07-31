# General Information
This folder contains the model training file and the dataset it was trained on. The model itself is too big to put on here, but the model basically is able to decide whether an image is clear sky, 0, or other, 1. The dataset it was trained on contains image file paths and their corresponding label. 

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
In order to run the script, you must have updated the "labeled_paths.csv" file with the correct image paths on your local machine. Once the csv file is corrected, then you must update the file path in "clearsky.py" itself to the corrected csv file. 



