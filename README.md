# Reaching-Task

<div align="center">
  <img src="README%20images/Labeled_Reach.png" alt="Arash" width="400"/>
</div>


## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Using DeepLabCut](#using-deeplabcut)
4. [Novel Video Analysis](#novel-video-analysis)
5. [Custom Scripts Using DeepLabCut](#custom-scripts-using-deeplabcut)  
    I. [New Reaching Task.ipynb](#new-reaching-task)  
    II. [Process Videos.py](#process-videos)  
    III. [Template and Correlation.ipynb](#template-and-correlation-script)  
    IV. [Rat Correlation.py](#all-rats-average-peak)  
    V. [Session Viewer.py](#session-viewer)  
    VI. [Watch Session.py](#watch-session)  
6. [Acknowledgments](#acknowledgments)


## Introduction
Welcome to the Reaching Task repository, which outlines the process of handling our experimental rat behavioral data. This includes preprocessing the videos and analyzing the trajectories of the reaching tasks. Our goal was to measure the stereotypical nature of rats during a reaching task. In this task, a rat triggers a pedestal to rise with a sugar pellet, and then reaches out to grab it. We hypothesized that as the rat improves over 10 sessions, its grab would become more stereotypical and uniform.

Using [DeepLabCut trajectory software](https://github.com/DeepLabCut/DeepLabCut), I developed a model to make motion tracking predictions using machine learning in TensorFlow. This model allows us to analyze thousands of videos efficiently, without manual labeling or the need to watch each video individually. 

In this repository, you can follow my journey through the analysis of the experiment, learn about the challenges I faced, and use my model to make your own predictions for your experiments.


## Installation       

### [DeepLabCut Installation Guide](https://deeplabcut.github.io/DeepLabCut/docs/installation.html)
### Important: Use DeepLabCut Tensorflow 
- My model will only work in a Tensoflow enviornment
- Double click on the batch file `setupDeeplabcutTF.bat`
  - This will create the `DEEPLABCUT_TF` environment in the `REACHING-TASK` directory
  - It will use the `DEEPLABCUT_TF.yaml` to create it
  - This will give you Deeplabcut version 2.3.10 using Tensorflow Engine

- Follow steps carefully, versions have to be compatible:
  - GPU needs to have CUDA installed.
  - If you don’t see activity during training, then your GPU is likely not installed correctly for DeepLabCut. Return to the installation instructions, and be sure you installed CUDA 11+, and ran `conda install cudnn -c conda-forge` after installing DeepLabCut.
  - To check if GPU is running with DeepLabCut:
    - Open Task Manager > More > Performance > GPU (yours) > Switch tab to CUDA.
    - This will show % of GPU used, which will be high during training.
    - [How to confirm that your GPU is being used by DeepLabCut](https://deeplabcut.github.io/DeepLabCut/docs/recipes/installTips.html)



### Issues I had with Version 2.3.5 (2023)
- The version was very buggy:
  - No Saving
  - No Cropping
  - Kernel kept dying

### Troubleshooting Installation to Older Version
- Trouble installing newest DeepLabCut environment
- Created a new environment for the old version:
  - Copied dependencies and except for `pip install deeplabcut`.
  - Installed `deeplabcut==2.2.3` using pip.
  - Installed Version 2.2.3 and it ended up in “Light Mode"
    - Installed `wxpython` using pip to use the GUI.
  - Cropping did not work right away:
    - Installed `matplotlib==3.5.2` using pip.
  - Problem Saving Points in Excel and in GUI:
    - In the Labeling Toolbox, syntax needed to be changed:
     - Labeling toolbox is in `anaconda3\envs\deeplabcut\Lib\site-packages\deeplabcut\gui`.
     - Lines to be changed:
       ```python
       self.dataFrame.loc[self.relativeimagenames[self.iter]][self.scorer, bp[0][-2], "x"] = bp[-1][0]
       self.dataFrame.loc[self.relativeimagenames[self.iter]][self.scorer, bp[0][-2], "y"] = bp[-1][1]
       ```
     - Changed to:
       ```python
       self.dataFrame.loc[self.relativeimagenames[self.iter], (self.scorer, bp[0][-2], "x")] = bp[-1][0]
       self.dataFrame.loc[self.relativeimagenames[self.iter], (self.scorer, bp[0][-2], "y")] = bp[-1][1]
       ```
### Deeplabcut Pytorch
- The newest deeplabcut release version 3.0.1 (June 2024) Uses Pytorch Engine
- There is a lot of changes, read documentation if you want to use this version
- My model will not work since it was made using Tensorflow
  - You may be able to transform the model form TF to Pytorch
  - This will include changing all of the config file in deeplabcut 
  - I have not tried this approach
# Using DeepLabCut
### Create Task
- Import `deeplabcut`.
- Create the task using `deeplabcut.create_new_project`.

### Export Videos
- Select Manually
- It will allow for cropping which will speed up the process as less data is being analyzed.
- Take crop coordinates and apply them (copy-paste coordinates) to the config file for each video.
- Export automatically with `crop=True`.
- All videos will now have the same crop effects.
- Once the config file is changed for each video, the newest version can be implemented:
  - The export automatically will work to extract frames.
  - Alternatively, use the [NAPARI crop extension](https://www.napari-hub.org/plugins/napari-crop).
      - Download the Crop Plug-in.
      - Create a Shape Layer (of crop).
      - Extract Coordinates.
      - Go to `config.yaml` (change video coordinates to these).
      - Extract frames again (the edited config will properly crop).

    ### Crop Coordinates
    These coordinates were specific to the model being used, it included the whole task (rat hand reaching for pellet). 
    - Front Coordinates Crop: `819, 1290, 510, 1084`
    - Left Mirror Coordinates Crop: `192, 572, 575, 1004`
    - Lefty Coordinates Crop: `700, 1175, 510, 1084`

    ### Labeling
    - Labeling is done manually for recommended 100-150 frames. (10 videos for the project)
    - In the `config.yaml`, add labels and body parts:
    - Each task will need different body parts/objects.
    - A hand will have fingers/wrist and a pellet to grab.
    - Many points can be added but will be more tedious.
    - Only label one session per window (close it and re-run the cell).
    - Open Folder works, open file does not.
    - While marking, make sure the labels are correct:
    - Toggle show label.
    - It will sometimes change color but not label.
    - It will sometimes skip labels.
    - You can move and erase points.
    - Make sure to save the selected layer, not all layers, it will cause you to lose work and kill the kernel.(bug)

    ### Training
    - Training will take a very long time:
    - It took an hour to run 50,000 iterations; with a newer GPU, it took half an hour to run 50,000 iterations.
    - Total training time: ~20 hours (1,030,000 iterations).
    - Leave the computer on overnight to run training.
    - Make sure the GPU is being used:
    - It will not work properly and will take even longer to train, before breaking.
    - To check if GPU is running with DeepLabCut:
        - Task Manager > More > Performance > GPU (yours) > Switch tab to CUDA.
        - This will show % of GPU used, will be high during training.
        - It should be at almost 100% while training, 55-65% with a new GPU.
        - If it goes to zero, make sure the training didn’t fail.
    - If training fails:
    - Make sure “snapshots” of your training are saved.
    - You can start from a snapshot instead of the beginning.
    - Snapshots are large, so don’t save too often; default every 50,000 starting at 200,000.
    - If no snapshots are saved, you must start over.
    - To use a snapshot, load the `pose_cfg.yaml` (in the training folder with the snapshots).
    - Change `init_weights` from default to the specific snapshot path.
    - Example:
        ```yaml
        init_weights: C:\\Users\\Andrew\\Documents\\Parra_Lab\\New-Reaching_Task_Left_Mirror-Andrew-2023-05-31\\dlc-models\\iteration-0\\New-Reaching_Task_Left_MirrorMay31-trainset95shuffle1\\train\\snapshot-400000
        ```
    - You don’t need to specify the snapshot file, only the number because a few files are being utilized.
    - If you want to label more videos and retrain, you can:
    - It will train under a new iteration.
    - To switch iterations, go to `config.yaml` and change the iteration to the desired one.

    ## Novel Video Analysis
    - After training, the model performance must be evaluated:
    - If the model performance is good, you can move on.
    - Use the `analyze_video` function to test the model on new data:
    - An Excel file with the x and y trajectory for each body part will be made.
    - Use the `filter` function to smooth out trajectory data:
        - Median – default (worked best for me)
        - Spline
        - Arimax
    - After video analysis:
    - Plot trajectories for each video:
        - Coordinate vs time (x and y separately).
        - Likelihood vs time.
        - X vs y direction.
    - Create labeled videos:
        - Will plot skeleton and labeled data onto videos.
        - This will show the predicted trajectory over the actual video.  
## Custom Scripts Using DeepLabCut
- Naming convention is important for all the code.
- Rats' files will be named (Rat_{Rat name}) i.e. Rat_Arash.
- Rat sessions will be S1-S10 (relies heavily on having sessions).
- Specific videos do not need to be named.

### New Reaching Task
- This script will go through all of steps needed to make a new model
- This is mostly from the deeplabcut user guide
- A model was already made for this reaching task, a new one is not needed
- Refer to user guide and usage steps above for guidance 
- User Inputs:
  - video_path = path to the video file as a list or array of paths
  - working_dir = path to the directory where you want to store the project
  - USER = users name
  - Project = project name

### Problems Faced with Videos
- There are a lot of videos:
  - 20 Rats, 10 Sessions per rat, 20-70 trials per session, 1 video per trial.
  - Over 10,000 videos.
- Storage:
  - Each video is about 1-2 GB and 1 second long.
  - Takes up too much storage room on computer.
  - Takes a long time to analyze.
  - Video players would crash.
- FFMPEG was used to downsample in high quality to keep the integrity of videos:
  - Videos are now 10-30 MB with the same frame rate and pixel density.
  - Videos were originally raw footage with no compression.
  - The model was tested with original videos vs downsampled videos and results were almost identical.
- Lefty Rats:
  - The model was made using a right-handed rat (Arash, 1st video of each session).
  - Left-handed rats performed terribly using the model.
  - Used FFMPEG to horizontally flip the videos to make left-handed look like right-handed.
  - The model performed just as well with flipped videos.
- Videos are being downloaded from DropBox and downsampled (and flipped for lefty):
  - Can only be done one rat at a time because each rat's footage is a TB (not enough storage on computer).
  - This takes hours to download and then process (one rat takes 1-3 days).
  - Videos will be uploaded back to DropBox for ease of use in the future.

### Use Script to Downsample and Analyze Videos
Input the following:  
- Path of video files
- Config path (model)
- Rat name
- Right or Left handed
- Rat sessions (pick 1 specific session or many sessions starting from 1)
- Decide if you want to analyze and filter videos or not

### Expected Time
- Should take 20 minutes for downsampling each rat.
- Should take about 1 hour for analyzing and filtering each rat.
- Make sure the GPU is running, or this step will take hours.

### Files Created
- **Downsample**:
  - Original videos will be moved to file `backup_S1-S10`.
  - New downsampled (flipped) videos will be in files `S1-S10`.
- **Analyze**:
  - H5 file.
  - PICKLE file.
  - Excel Spreadsheet.
- **Filter**:
  - H5 file.filtered.
  - Excel Spreadsheet.filtered.
  - The filtered.csv Excel file is the one used for the rest of the codes.

### Process Videos 
- This script processes videos for the reaching task experiment  
- The script:
  - Moves the original videos to a backup directory
    - Saved in the following format: Rat_Name/backup_S{Session_Number}/video.avi
  - Downsamples the videos
    - Saved in the following format: Rat_Name/S{Session_Number}/video.avi
  - Analyzes them using DeepLabCut
    - Saved as predcitions in an excel sheet
- Prompts:
  - Enter the number of sessions to process, the rat name, and which hand the rat uses.
  - Specify whether they want to analyze the videos using DeepLabCut
  - The script assumes the videos are in .avi format and the output videos are in .avi format

### Problems Faced with Predictions
- Every video is unique, even the same rat in the same session:
  - Length of video (number of samples).
  - Time of grab.
  - A standardized way of identifying when the rat is grabbing is needed.
  - To find similarities in videos, plots of all the body parts (x and y direction) were generated.
  - There is a point in the curve where the y-direction dips and the x-direction peaks.
  - After watching many videos, this point is when the grab takes place (many of these points when multiple grab trials occur).
  - There is a need to identify the grab without having to watch all the videos or analyze the plots individually.

### Cross-Correlation
- To compare videos in each session, a template generator was created, and the cross-correlation between each trial was used to observe lags (sample time) of high similarity; this point will be the start of each grab.
- The template was a combination of 3 or more trials carefully selected at the point of grab (25 samples before and after the point of interest).

![Normalized Cross-Correlation](README%20images/Normalized_Cross_Corr.png) 

- The normalized cross correlation is taken for each lag 
- This was taken separately for each body part and then averaged 
- The lag with the highest similarity (max corr) is the time point where the grab is most likely to begin 
- Each trial was indexed from the peak for 50 samples (roughly the start to finish of a grab)
- This gave a list of grabs 50 samples long which is now useful for comparison (having the same length is needed for comparison across trials)
- This was done for all trials in the session

### Template and Correlation Script
- Inputs:
  - Rat name
  - Session number
-	Once videos are downsampled and analyzed they can be loaded into a list
    -	All of the code uses list comprehension due to the nature of the data
    -	Each file is a different length 
    - Most operations would not work without nesting lists 
    - The error would be “array + inhomogeneous part”
-	GUI will open with a checklist of all of the trials & a plot of each trial 
    -	Click on the next button to see the next trial and previous to see previous trial
    -	Once desired trials are located, check them off on the checklist 
    -	Close window for the next steps

![alt text](README%20images/Template_GUI.png)

#### Selecting Trial
- There will be a point that looks like a “grab” in every trial 

![alt text](README%20images/Grab_Trial.png)

- This is where the x-coordinates and y-coordinates movements synchronize at a peak and trough
-	The point is usually where the x-coordinates are at a max and the y-coordinates are at a minimum 
-	This motion signifies a grab, some videos will have multiple


![alt text](README%20images/Multigrab_Trial.png)

-	Mult-Grab videos aren’t good for templates because the 2nd grab usually starts in the same window as the 1st grab
-	Trials without too much noise should be selected for the template 
 
![alt text](README%20images/Noisy_Grab_Trial.png)

-	Noise can come from inconsistencies in the grab video
    -	Irregular grab motion
    - The 2nd hand being visible on the glass or pedestal
    - Having the nose stick through
    -	Unidentified object in the video

#### Selecting Point of Interest 
- After selecting desired trials
  -	Choose the same number of trials each time
  - The analysis was done choosing 3 trials as the templates 
  - Templates did not look as good with more trials 
-	The selected plots will reopen
-	Choose the point of interest by clicking the mouse on x-coordinate which signifies the time or sample of interest 
    -	Y-coordinate will have no effect on the template
-	25 points before and after the point of interest will be taken to signify a “grab” 
- The segmented trials will be averaged to complete the template and look like a “grab”

![alt text](README%20images/Template_Grab.png)

-	The template will be stored in an excel sheet
    -	Each Rat will have an Excel file “Rat_Name_Templates”
    -	Each Session will have an Excel sheet “Rat Name S{i} Template”
-	The templates are now easily accessible
-	For proper calculations templates for each session must be made

#### Cross-Correlation 
- Each trial will be compared for against the template to find the point of interest 
- The peaks of the cross-correlation will be the time or sample of the grab



![alt text](README%20images/Cross_Corr.png)

#### Peak Cross-Correlation Coefficient 
- The max cross-correlation coefficient value was taken for each trial
-	The average of each trial for each session was taken using session specific template

### Rat Correlation
This Script has a prompt to select one of 3 correlation types:
- Session
  - Calculate the average last peak stereotypical value for a session for a single rat
  - Plot the correlation compared to the template for a sample trial
  - Inputs: 
    - Rat Name
    - Session Number 
    - Trial Number
- Single Rat
  - Calculate the average last peak stereotypical value for a single rat, all sessions
  - Plot the peak correlation for each session
  - Inputs:
    - Rat Name
- All Rats
  - Calculate the average last peak stereotypical value for all sessions for every rat
  - Plot all sterotypical values for all the rats over time and plot the average with standard deviation bars
  - Save the values into an excel sheet if desired
  - Inputs:
    - Yes/No (save to excel)



![alt text](README%20images/All_Stereotypie.png)

![alt text](README%20images/Stereotypic_Behavior.svg)


### Session Viewer
- This script allows the user to view all of the deeplabcut predictions for one session
- The user will be asked to select a rat and session to view as input
- The predictions will be availble to be scrolled through by clicking next trial or previous trial
- This is useful if you are trying to locate outlier trials 

### Watch Session 
- This script allows the user to watch all of the videos in one session
- The user will be asked to select a rat and session to view as input
- The videos will play without stopping until there are not more video files in the session
- This is useful if you are trying to locate outlier videos
## Acknowledgments
### Parra Lab 
- Lucas C Parra - Head of Parra Lab
- Forouzan V Farahani - Conducted Experiments for Analysis

### Deeplabcut Paper & Software

- Mathis, A., Mamidanna, P., Cury, K. M., Abe, T., Murthy, V. N., Mathis, M. W., & Bethge, M. (2018). DeepLabCut: markerless pose estimation of user-defined body parts with deep learning. Nature Neuroscience, 21(9), 1281–1289. https://doi.org/10.1038/s41593-018-0209-y

- Nath, T., Mathis, A., Chen, A.C. et al. Using DeepLabCut for 3D markerless pose estimation across species and behaviors. Nat Protoc 14, 2152–2176 (2019). https://doi.org/10.1038/s41596-019-0176-0
