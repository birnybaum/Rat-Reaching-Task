#This script processes videos for a reaching task experiment. It downsamples the videos and analyzes them using DeepLabCut.
#The user is prompted to enter the number of sessions to process, the rat name, and which hand the rat uses.
#The user is also prompted to specify whether they want to process the videos using DeepLabCut.
#The script moves the original videos to a backup directory, downsamples the videos, and analyzes them using DeepLabCut.
#The processed videos are saved in the original directory.
#The script requires the user to have DeepLabCut installed and a config.yaml file for the experiment.
#The script assumes the videos are in the following format: Rat_Name/S{Session_Number}/video.avi located in the User_Dir directory.
#The processed videos are saved in the following format: Rat_Name/S{Session_Number}/video.avi
#The backup videos are saved in the following format: Rat_Name/backup_S{Session_Number}/video.avi
#The script assumes the videos are in .avi format and the output videos are in .avi format.
#The script assumes the user has ffmpeg installed and added to the PATH.

import os
import shutil
import subprocess
import glob
import deeplabcut
import re
from reaching_task_utils import list_available_rats, process_sessions


# Initialize global variables
User_Dir = # Enter the path to the directory containing the videos start with a r' and end with a trailing slash
# Example: User_Dir = r'C:\Users\username\Documents\Reach_Task\'
config_path = os.path.join(User_Dir, 'New-Reaching_Task-Andrew-2023-05-29\\config.yaml')


def main():
    
    available_rats = list_available_rats(User_Dir)  # Show available rats at the start
    #print("Available rats:", ', '.join(available_rats))
    rat_name = input("Enter rat name: ")
    if rat_name not in available_rats:
        print("Rat name not found. Please enter a valid rat name from the list.")
        return
    rat_hand = input("Which hand does the rat use, right or left? ").lower()
    
    session_input = input("Enter the number of sessions to process or '1' to specify a session: ")
       
    try:
        session_count = int(session_input)
        if session_count == 1:
            specific_session = input("Enter the specific session number: ")
            sessions = [specific_session]
        else:
            sessions = [str(i) for i in range(1, session_count + 1)]
    except ValueError:
        print("Invalid session input. Please enter a valid number.")
        return
    
    
    process = input("Do you want to downsample and analyze the videos using DeepLabCut? (yes/no): ").lower()
    
    if process == 'yes':
        process_sessions(User_Dir, sessions, rat_name, rat_hand, config_path)
        print('Processing complete.')

if __name__ == "__main__":
    main()