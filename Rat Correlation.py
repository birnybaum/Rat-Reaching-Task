# This script will allow you to select one of three correlation types: session, rat, or all rats
# If you select session, you will be prompted to enter a rat and session number and then select a trial from that session
# It will then plot the original trial, the template, the correlation between the two, and the correlation with the sample point marked
# The script will also print the last peak of the correlation and the index of the last peak
# The last peak is the successful grab in multigrab trials so it was selected to represent the data
# If you select rat, you will be prompted to enter a rat name and the script will plot the correlation for all sessions of that rat
# If you select all rats, the script will plot the correlation for all rats and save the data to a csv file
# The script will also print the average peak correlation for all rats and the standard deviation


# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 12:16:23 2024

@author: Andrew
"""


from reaching_task_utils import (
    list_available_rats,
    completed_rats,
    process_files,
    plot_single_trial,
    plot_single_rat_data,
    plot_all_rats,
    save_all_rats,
)

User_Dir = # Enter the path to the directory containing the videos start with a r' and end with a trailing slash
# Example: User_Dir = r'C:\Users\username\Documents\Reach_Task\\'

rat_list = list_available_rats(User_Dir)
completed_rat_list = completed_rats(User_Dir, rat_list)

print('\nAvailable correlation types: session, rat, all rats')
Correlation = input('What do you want to correlate? Choose one of the options: ')
if Correlation == 'session':
    rat_name = input('Choose your rat: ')
    session_number = int(input('Enter the session number: '))
    myList = process_files(User_Dir, rat_name, session_number)
    trial = myList[int(input(f'Select your trial, 1-{len(myList)-1}: '))]
    plot_single_trial(User_Dir,rat_name,session_number,trial)
elif Correlation == 'rat':
    rat_name = input("Enter the rat name: ")
    plot_single_rat_data(User_Dir, rat_name)
elif Correlation == 'all rats':
    Rat_Avg_Peak, avg_peak, S = plot_all_rats(User_Dir, completed_rat_list)
    save_all_rats(User_Dir, completed_rat_list, Rat_Avg_Peak,avg_peak,S)
    
    
