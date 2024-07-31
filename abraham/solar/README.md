# General Information
This folder contains the csv file used for training and the model training script. The dataset is comprised of image paths and their corresponding wattage value. The model I trained was a regression model that estimating the solar wattage based on a given sky face image. 

## How To Get Data
The dataset images can be found in /lcrc/project/waggle/summer_projects/summer2024/ruben_abraham. In this folder, you will see a zip file called "watt_model_dataset."

You can download it like this
```sh
scp your_username@lcrc.anl.gov:/lcrc/project/waggle/summer_projects/summer2024/ruben_abraham/watt_model_dataset.zip /your/local/path/on/computer
```

Once extracted, it contains the "storage.sagecontinuum.org" folder which contains all of the images I used.


The model is also found in the "ruben_abraham" folder called "resnet50Watt.pth." 
You can download the model like this
```sh
scp your_username@lcrc.anl.gov:/lcrc/project/waggle/summer_projects/summer2024/ruben_abraham /your/local/path/on/computer
```
