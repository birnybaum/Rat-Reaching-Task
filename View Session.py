# This script will let you view all the trials for a given rat and session number.
# This will allow you do visualize the data for each trial and compare them. 

import re
import glob
import pandas as pd
import numpy as np
import os.path
from reaching_task_utils import list_available_rats, process_files, completed_rats


User_Dir =  # Enter the path to the directory containing the videos start with a r' and end with a trailing slash
# Example: User_Dir = r'C:\Users\username\Documents\Reach_Task\\'
rat_list = list_available_rats(User_Dir)
  
# Call the function
while True:
    rat_name = input(f"Acceptable names are {rat_list}\n\nEnter rat name: ")
    if rat_name in rat_list: 
        sessions = 7 if rat_name in ['Fariborz', 'Iraj', 'Tur'] else 10
        session_number = input("\nEnter the session number: ")
        myList = process_files(User_Dir, rat_name, session_number)   
        break    
    else: 
        print(f'{rat_name} Is not an acceptable rat name')
   


import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

LARGEFONT = ("Verdana", 35)

class tkinterApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)  # Second column should expand

        self.frames = {}
        self.selected_trials = []  # List to store the selected trial indices

        # Scrollbar for trial selection
        trials = [f'Trial {i + 1}' for i in range(len(myList))]
        self.trial_vars = []  # List to store the variables for each checkbox

        # Create the frame for the checklist
        checklist_frame = tk.Frame(container, bd=2, relief="ridge", width=200)  # Set width to make it smaller
        checklist_frame.grid(row=0, column=0, sticky="nsew")

        canvas = tk.Canvas(checklist_frame)
        frame = tk.Frame(canvas)

        scroll_y = tk.Scrollbar(checklist_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scroll_y.set)

        scroll_y.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0, 0), window=frame, anchor="nw")

        for i, trial in enumerate(trials):
            var = tk.StringVar(value="off")  # Initialize checkbox state as "off"
            self.trial_vars.append(var)
            trial_style = ttk.Style()
            trial_style.configure("Trial.TCheckbutton", font=("Verdana", 10))  # Set the font size for the style
            trial_checkbox = ttk.Checkbutton(frame, text=trial, variable=var,
                                             onvalue="on", offvalue="off", command=self.on_trial_checked, style="Trial.TCheckbutton")
            trial_checkbox.pack(anchor="w")  # Align checkboxes to the left

        # Bind the event to update scroll region after the frame size changes
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Create the plot frame
        plot_frame = tk.Frame(container)
        plot_frame.grid(row=0, column=1, sticky="nsew")

        self.container = plot_frame  # Store the plot frame in an instance variable

        # Create a plot for each trial and add it as a page
        for i in range(len(myList)):
            frame = PlotPage(plot_frame, self, myList[i], i)
            self.frames[i] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(0)  # Show the first plot page initially

        # Bind the close event of the application to a custom method
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def on_trial_checked(self):
        # Update the selected_trials list based on the checkboxes' states
        self.selected_trials = [i for i, var in enumerate(self.trial_vars) if var.get() == "on"]

    def on_close(self):
        # Custom method to handle application closing
        # Add any cleanup code here if needed
        self.destroy()


class PlotPage(tk.Frame):

    def __init__(self, parent, controller, data, trial_number):
        tk.Frame.__init__(self, parent)

        self.data = data
        self.trial_number = trial_number

        label = ttk.Label(self, text=f'Rat {rat_name}: Session {session_number}, Trial {trial_number + 1}', font=LARGEFONT)
        label.pack(pady=10, padx=10)

        # Create the plot for this page
        x = np.arange(len(data))
        plt.figure()
        plt.plot(x, data)
        plt.xlabel('Samples')
        plt.ylabel('Coordinate')
        plt.grid(True)
        plt.legend(labels=myList[0], bbox_to_anchor=(1.1, 1.05))
        plt.tight_layout()

        # Create a canvas for the plot
        canvas = FigureCanvasTkAgg(plt.gcf(), master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Close the figure to prevent accumulating too many open figures
        plt.close()

        # Button to navigate to the previous plot page
        if trial_number > 0:
            prev_button = ttk.Button(self, text="Previous Trial",
                                     command=lambda: controller.show_frame(trial_number - 1))
            prev_button.pack(side=tk.LEFT, pady=10, padx=10)

        # Button to navigate to the next plot page
        if trial_number < len(myList) - 1:
            next_button = ttk.Button(self, text="Next Trial",
                                     command=lambda: controller.show_frame(trial_number + 1))
            next_button.pack(side=tk.RIGHT, pady=10, padx=10)


if __name__ == "__main__":


    app = tkinterApp()
    app.mainloop()
    
   
    

