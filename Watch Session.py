# This script will allow you to watch the videos of a specific rat in a specific session. 
# The script will list all the available rats and sessions, and then prompt you to enter the rat name and session number.
# It will then play the videos for that rat in that session. 

import cv2
import glob
import re
import os
from reaching_task_utils import list_available_rats, play_video


User_Dir =  # Enter the path to the directory containing the videos start with a r' and end with a trailing slash
# Example: User_Dir = r'C:\Users\username\Documents\Reach_Task\\'
rat_list = list_available_rats(User_Dir)

if not rat_list:
    print("No acceptable rat names found. Exiting.")
    exit()

print(f"\nAcceptable names are {rat_list}")

rat_name = input("\nEnter rat name: ")

if rat_name not in rat_list:
    print("Invalid rat name. Exiting.")
    exit()

session = input("\nEnter the session number: ")

myFiles = glob.glob(os.path.join(User_Dir, f'Rat_{rat_name}', f'S{session}/*.avi'))

window_width = 1600
window_height = 800

if not myFiles:
    print(f"No video files found for rat '{rat_name}' in session {session}. Exiting.")
    exit()

for video in myFiles:
    video_path = video.replace("\\", "/")  # Replace backslashes with forward slashes
    play_video(video_path, window_width, window_height)
