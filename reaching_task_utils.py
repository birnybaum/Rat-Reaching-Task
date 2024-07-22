import os
import shutil
import subprocess
import glob
import re
import pandas as pd
import numpy as np
import cv2
from scipy import signal
import matplotlib.pyplot as plt

def list_available_rats(User_Dir):
    path_list = glob.glob(os.path.join(User_Dir, 'Rat_*'))
    rat_list = []
    for path in path_list:
        rat_match = re.search(r'Rat_(.*)', path)
        if rat_match:
            rat_list.append(rat_match.group(1))
    #print("Available rats: ",rat_list)
    return rat_list

def process_sessions(User_Dir, sessions, rat_name, rat_hand, config_path):
    for session in sessions:
        input_dir = os.path.join(User_Dir, f'Rat_{rat_name}', f'S{session}/')
        backup_dir = os.path.join(User_Dir, f'Rat_{rat_name}', f'backup_S{session}/')
        
        # Ensure backup directory exists
        os.makedirs(backup_dir, exist_ok=True)
        
        # Process videos for downsampling
        video_files = [f for f in os.listdir(input_dir) if f.endswith('.avi')]
        for video_file in video_files:
            process_video(input_dir, backup_dir, video_file, rat_hand)
        
        # Analyze videos with DeepLabCut
        analyze_videos(input_dir, config_path)

def process_video(input_dir, backup_dir, video_file, rat_hand):
    input_file = os.path.join(input_dir, video_file)
    backup_file = os.path.join(backup_dir, video_file)
    shutil.move(input_file, backup_file)
    
    ffmpeg_command = ['ffmpeg', '-i', backup_file, '-vf', 'scale=2032:1086', '-qscale', '0', input_file]
    if rat_hand == 'left':
        ffmpeg_command[4] += ',hflip'
    subprocess.run(ffmpeg_command)
    
    
def analyze_videos(input_dir, config_path):
    import deeplabcut
    avi_files = glob.glob(os.path.join(input_dir, '*.avi'))
    for avi_file in avi_files:
        deeplabcut.analyze_videos(config_path, [avi_file], save_as_csv=True)
        deeplabcut.filterpredictions(config_path, [avi_file])

def process_files(User_Dir, rat_name, session_number):
    myList = []
    file_path = os.path.join(User_Dir, f'Rat_{rat_name}/S{session_number}/*filtered.csv')
    myFiles = glob.glob(file_path)
    for file in myFiles:
        df = pd.read_csv(file)
        df.rename(columns=df.iloc[0] + '_' + df.iloc[1], inplace=True)
        df = df.iloc[2:].reset_index(drop=True)
        df.drop(['bodyparts_coords'], axis=1, inplace=True)
        df = df.astype(float)
        df = df.iloc[:, ~((np.arange(df.shape[1]) % 3 == 2) | (np.arange(df.shape[1]) >= df.shape[1]-3))]
        myList.append(df)
    return myList

#Creates excel sheet for selected rat and makes a sheet for each session
def make_template_spread_sheet(User_Dir,rat_name,sessions):
    #Create template folder if it doesnt exist
    if os.path.isdir(os.path.join(User_Dir,'Templates'))==False:
        os.makedirs(os.path.join(User_Dir,'Templates'))
    if os.path.isfile(os.path.join(User_Dir,'Templates',f'Rat_{rat_name}_Templates.xlsx'))==False:
        num = []
        for i in range(1, sessions+1):
            num.append(f'Rat_{rat_name} S{i} Template')
        with pd.ExcelWriter(os.path.join(User_Dir,'Templates',f'Rat_{rat_name}_Templates.xlsx')) as writer:
            for i in range(sessions):
                data = {"Template": num[i]}  
                df = pd.DataFrame(data,index=[0])
                df.to_excel(writer, sheet_name=f'Rat {rat_name} S{i+1} Template', index=False)   
    return

def templates_required(User_Dir, rat_name, sessions=10):
    sessions = 7 if rat_name in ['Fariborz', 'Iraj', 'Tur'] else 10
    myTemp=[]
    for i in range(1,sessions+1):
        file_path = os.path.join(User_Dir,'Templates', f'Rat_{rat_name}_Templates.xlsx')
        df = pd.read_excel(file_path, sheet_name=f'Rat {rat_name} S{i} Template')
        df.drop(columns=df.columns[0], axis=1, inplace=True)
        myTemp.append(df)
        sub=[]
    for i in range(sessions):
        if len(myTemp[i].columns)!=10:
            sub.append(i+1)
    return sub


def completed_rats(User_Dir,rat_list):
    completed_rat_list = [] 
    for rat in rat_list:
        if rat not in ['Fariborz','Iraj','Tahmasb', 'Tur']:
            sessions=10
        else: sessions=7
        try:
            if templates_required(User_Dir,rat,sessions)==[]:
                completed_rat_list.append(rat)
        except:
            print(f"Template for {rat} does not exist yet!")
    print('Rats with completed template lists are :',completed_rat_list)
    return completed_rat_list
    
    
def play_video(video_path, window_width, window_height):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Could not open video file '{video_path}'.")
        exit()

    cv2.namedWindow('Video Player', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Video Player', window_width, window_height)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        resized_frame = cv2.resize(frame, (window_width, window_height))
        cv2.imshow('Video Player', resized_frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def rat_corr(User_Dir,rat_name):
    if templates_required(User_Dir, rat_name) == []:
        sessions = 7 if rat_name in ['Fariborz', 'Iraj', 'Tur'] else 10
        print(f"Processing data for Rat {rat_name}...")
        
        myList = []
        myTemp = []
        for i in range(1, sessions+1):
            List = process_files(User_Dir, rat_name, i)
            df = pd.read_excel(os.path.join(User_Dir, 'Templates', f'Rat_{rat_name}_Templates.xlsx'),
                               sheet_name=f'Rat {rat_name} S{i} Template')
            df.drop(columns=df.columns[0], axis=1, inplace=True)
            myTemp.append(df)
            myList.append(List)
        data = myList
        Corr = []
        session = len(data)
    
        for i in range(session):
            sub2 = []
            for j in range(len(data[i])):
                sub = []
                for k in range(10):
                    x = data[i][j].iloc[:, k]
                    y = pd.DataFrame(myTemp[i]).iloc[:, k]
                    x = x - np.nanmean(x)
                    y = y - np.nanmean(y)
                    x /= np.linalg.norm(x)
                    y /= np.linalg.norm(y)
                    corr = signal.correlate(x, y, mode='valid', method='fft')
                    sub.append(corr)
                sub2.append(sub)
            Corr.append(sub2)
    
        avg_corr = []
        for i in range(len(Corr)):
            sub = []
            for j in range(len(Corr[i])):
                sub.append(np.nanmean(Corr[i][j], 0))
            avg_corr.append(sub)
    
        peak_idx = []
        peak = []
        for i in range(len(avg_corr)):
            sub_idx = []
            sub_peak = []
            for j in range(len(avg_corr[i])):
                index, _ = signal.find_peaks(avg_corr[i][j], height=0.15)
                if index.size != 0:
                    last_idx = index[0] #first is 0
                    sub_idx.append(last_idx)
                    sub_peak.append(avg_corr[i][j][last_idx])
                else:
                    last_idx = np.argmax(avg_corr[i][j])
                    sub_idx.append(last_idx)
                    sub_peak.append(avg_corr[i][j][last_idx])
            peak_idx.append(sub_idx)
            peak.append(sub_peak)
    
        avg_peak = []
        for i in range(len(peak)):
            avg_peak.append(np.nanmean(peak[i]))
    else:
        print(f"Template for Rat {rat_name} is incomplete!")
    return avg_peak

def plot_single_trial(User_Dir,rat_name,session_number,trial):
    df = pd.read_excel(os.path.join(User_Dir,'Templates', f'Rat_{rat_name}_Templates.xlsx'),
                sheet_name=f'Rat {rat_name} S{session_number} Template')
    df.drop(columns=df.columns[0], axis=1, inplace=True)
    myTemp = df    
    
    Corr=[]
    # Creating grid for subplots
    fig = plt.figure()
    fig.set_figheight(10)
    fig.set_figwidth(8)
    ax1 = plt.subplot2grid(shape=(4, 4), loc=(0, 0), colspan=4)
    ax2 = plt.subplot2grid(shape=(4, 4), loc=(1, 0), colspan=4)
    ax3 = plt.subplot2grid(shape=(4, 4), loc=(2, 0), colspan=4)
    ax4 = plt.subplot2grid(shape=(4, 4), loc=(3, 0), colspan=4)
    
    # Labels for each plot
    labels_original = ['Wrist_x', 'Wrist_y', 'Thumb_x', 'Thumb_y', 'Index_x', 'Index_y',
                       'Middle_x', 'Middle_y', 'Last_x', 'Last_y']
    
    labels_correlation = labels_original + ['Avg']
    labels_combined = labels_original + ['Grab Location']
    
    # Loop through each body part
    for i in range(10):
        x = trial.iloc[:, i]
        y = pd.DataFrame(myTemp).iloc[:, i]
        
        # Plotting subplots
        ax1.plot(x, label=labels_original[i])
        ax1.set_title('Original Trial')
        ax1.set_ylabel('Amplitude')
        ax1.set_xlabel('Sample')
        
        ax2.plot(y, label=labels_original[i])
        ax2.set_title('Template')
        ax2.set_ylabel('Amplitude')
        ax2.set_xlabel('Sample')
        
        x = x - np.nanmean(x)
        y = y - np.nanmean(y)
        x /= np.linalg.norm(x)
        y /= np.linalg.norm(y)
        
        corr = signal.correlate(x, y, mode='valid', method='fft')
        Corr.append(corr)
        
        ax3.plot(corr, label=labels_correlation[i], linestyle=':', linewidth=1.25)
    
    # Find the peak and index of the average correlation
    avg_corr = np.nanmean(Corr, 0)
    
    peak_idx, _ = signal.find_peaks(avg_corr,height= .1)
    peak = avg_corr[peak_idx[-1]]
    
    print('The Peak of the Correlation is', peak, 'and the index is', peak_idx[-1] + 25)
    
    ax3.plot(avg_corr, color='black', label='Avg Correlation')
    ax3.set_title('Norm Corr')
    ax3.set_xlabel('Lag')
    ax3.set_ylabel('Correlation')
    
    ax4.plot(trial)
    ax4.axvline(x=peak_idx[-1] + 25, color='r', linestyle='-')
    ax4.set_title('Norm Corr w/ Sample Point')
    ax4.set_ylabel('Amplitude')
    ax4.set_xlabel('Sample')
    
    # Adding legends
    ax1.legend(bbox_to_anchor=(1.1, 1.05))
    ax2.legend(bbox_to_anchor=(1.1, 1.05))
    ax3.legend(bbox_to_anchor=(1.1, 1.05))
    ax4.legend(labels=labels_combined, bbox_to_anchor=(1.1, 1.05))
    
    plt.tight_layout()
    plt.show()

# Function to plot data for a specified rat
def plot_single_rat_data(User_Dir, rat_name):
    avg_peak = rat_corr(User_Dir,rat_name)
    if rat_name in ['Fariborz', 'Iraj', 'Tur']:
        S = [1, 2, 3, 4, 5, 6, 7]
    else:
        S = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    plt.figure(figsize=(16, 8))

    plt.plot(S, avg_peak, marker='o', markerfacecolor='r', linestyle='--')
    plt.title(f'Rat {rat_name}: Average Peak Corr')
    plt.xlabel('Session')
    plt.xticks(S)
    plt.ylabel('Corr Value')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    

def plot_all_rats(User_Dir,completed_rat_list):
    # Calculate the number of rows for subplots
    num_rows = len(completed_rat_list)
    max_sessions = max(7, 10)
    # Create a figure with subplots for each rat
    plt.figure(figsize=(num_rows, num_rows/2))
    Rat_Avg_Peak = []
    # legends = []
    lines_avg_peak = []
    std_devs = []
    for idx, rat_name in enumerate(completed_rat_list):
        sessions = 7 if rat_name in ['Fariborz', 'Iraj', 'Tur'] else 10
        avg_peak = rat_corr(User_Dir,rat_name)
        Rat_Avg_Peak.append(avg_peak)
        S = list(range(1, sessions + 1))
        line, = plt.plot(S, avg_peak, marker='o', markerfacecolor='r', linestyle='--')
        lines_avg_peak.append(np.pad(avg_peak, (0, max_sessions - sessions), mode='constant', constant_values=np.nan))
        # legends.append(rat_name)
        std_devs.append(np.pad(np.nanstd(lines_avg_peak[idx], axis=0), (0, max_sessions - sessions),
                               mode='constant', constant_values=np.nan))
    avg_peak_avg = np.nanmean(lines_avg_peak, axis=0)
    std_dev_avg = np.nanmean(np.vstack(std_devs), axis=0)
    plt.plot(S, avg_peak_avg, linewidth=3, label='Average', color='black')
    plt.errorbar(S, avg_peak_avg, yerr=std_dev_avg, linewidth=3, label='Average', color='black', fmt='o',
                 markerfacecolor='r', linestyle='--')
    plt.title('Evolution of Stereotypic Behaviors Across Training Sessions', fontsize=30)
    plt.xlabel('Training Session', fontsize=30)
    plt.ylabel('Peak Correlation Coeficient', fontsize=30)
    plt.xticks(range(1, 11))
    plt.tick_params(axis='both', labelsize=20)  # Set the font size for both x and y-axis ticks
    #labels=np.append(rat_list,'Average')
    #plt.legend(labels=labels,loc='upper left')
    #plt.savefig('All_Rats.png', dpi=300)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    return Rat_Avg_Peak, avg_peak, S

def save_all_rats(User_Dir, completed_rat_list, Rat_Avg_Peak,avg_peak,S):
    # Save the data to an Excel file
    data = {}
    max_sessions = 0
    for i, rat_name in enumerate(completed_rat_list):
        data[rat_name] = Rat_Avg_Peak[i]
        if len(Rat_Avg_Peak[i]) > max_sessions:
            max_sessions = len(Rat_Avg_Peak[i])

    df_data = pd.DataFrame({rat_name: pd.Series(rat_data) for rat_name, rat_data in data.items()})
    df_data = df_data.T
    df_data.columns = ['S' + str(i+1) for i in range(max_sessions)]

    save_data = input("Do you want to save the data to an Excel file? (yes/no): ").strip().lower()
    if save_data == 'yes':
        output_path = os.path.join(User_Dir, 'rat_behavior_analysis.xlsx')
        df_data.to_excel(output_path, index=True, index_label='Rat Name')
        print(f"Data has been saved to {output_path}")