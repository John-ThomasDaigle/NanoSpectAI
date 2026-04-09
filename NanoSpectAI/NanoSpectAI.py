import tkinter as tk
#from tkinter import ttk
import ttkbootstrap as ttk
import subprocess
import sys

# window
window = ttk.Window(themename = 'superhero')
window.title('NanoSpectAI')
window.geometry('600x400')

# variables
seconds = 0

# functions
def update_timer():
    global seconds
    seconds += 1
    if seconds >= 15:
        timeLabel.configure(text = 'Mobile Launched')
        subprocess.Popen([sys.executable, "Mobile.py"])
    else:
        timeLabel.configure(text = str(seconds))
        window.after(1000, update_timer)

# labels
timeLabel = ttk.Label(window,
                    text = '0', 
                    font=('Helvetica', 24))
timeLabel.pack(pady = 20)

# buttons
nanoSpectAICamera = ttk.Button(window, 
                               text = 'Camera',
                               width = 30,
                               command =  lambda:  subprocess.Popen([sys.executable, "Camera.py"]))
nanoSpectAICamera.pack(pady = 50)

nanoSpectAIMobile = ttk.Button(window, 
                               text = 'Mobile',
                               width = 30,
                               command = lambda: subprocess.Popen([sys.executable, "Mobile.py"]))
nanoSpectAIMobile.pack()

# run
update_timer()
window.mainloop()