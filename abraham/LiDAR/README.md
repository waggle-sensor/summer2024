# General Information
This folder contains two scripts, one to plot the mpl file itself in color and another to plot 5 minute intervals of the mpl file. These scripts will work on the mini_mpl files found in /lcrc/project/waggle/public_html/datasets after you have downloaded them to your local machine. 


## mplplotter.py
The mplplotter.py script creates an output that looks like this

<p align="center"> <img src="/abraham/Images/lidar_sky-solar1.png" width="700"> </p> 

## mplavg.py
The mplavg.py script creates an output that looks like this

<p align="center"> <img src="/abraham/Images/pc0-5.png" width="700"> </p> 

## How To Get Files
To download files from lcrc to a local path on your computer
 ```sh
scp your_username@lcrc.anl.gov:/lcrc/project/waggle/public_html/datasets/minimpl_202203.mpl /your/local/path/on/computer
```

There is also a zip file I created that has 24 hours of clear sky and 12 hours of hazy sky conditions. I organized this, from the main mini_mpl files. We wanted to use the clear sky files as a baseline or standard and see how it differed from the hazy sky files. We thought this would help us potentially define a threshold between clear and hazy for a model.

To download this
```sh
scp your_username@lcrc.anl.gov:/lcrc/project/waggle/public_html/datasets/LiDAR_clearhazy.zip /your/local/path/on/computer

```
## How To Run The Scripts
To run the scripts you would need to update the filename_path variable to the path of the mpl file in your machine that you are using. Just for idea, if the plots don't work for you, you can update the "mplavg.py" script or both scripts to save the data to a csv file instead of a plot. It may make it easier for you to manipulate the data. 
