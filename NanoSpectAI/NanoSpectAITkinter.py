import tkinter as tk
# from tkinter import ttk
import ttkbootstrap as ttk
import subprocess
import sys

# window
window = ttk.Window(themename = 'superhero')
window.title('NanoSpectAI')
window.geometry('600x400')

# variables
seconds = 0
timer_running = True
timer_id = None

# functions
def update_timer():
    global seconds, timer_id
    seconds += 1
    if seconds == 15:
        timeLabel.configure(text = 'Mobile Launched')
        subprocess.Popen([sys.executable, 'NanoSpectMobile.py'])
    else:
        timeLabel.configure(text = str(seconds))
        timer_id = window.after(1000, update_timer)

def stop_timer_and_launch(app_name, script):
    global timer_running, timer_id
    if timer_id is not None:
        window.after_cancel(timer_id)
        timer_id = None
    timer_running = False
    timeLabel.configure(text = f'{app_name} Launched')
    subprocess.Popen([sys.executable, script])
    

# labels
timeLabel = ttk.Label(window,
                    text = '0', 
                    font = ('Helvetica', 24))
timeLabel.pack(pady = 20)

# buttons
nanoSpectAICamera = ttk.Button(window, 
                               text = 'Camera',
                               width = 30,
                               command =  lambda: stop_timer_and_launch('Camera', 'NanoSpectCamera.py'))
nanoSpectAICamera.pack(pady = 50)

nanoSpectAIMobile = ttk.Button(window, 
                               text = 'Mobile',
                               width = 30,
                               command = lambda:stop_timer_and_launch('Mobile', 'NanoSpectMobile.py'))
nanoSpectAIMobile.pack()

# run
timer_id = window.after(1000, update_timer)
window.mainloop()
