from tkinter import filedialog
# from filedialog import LoadFileDialog
from tkinter import *
from tkinter.filedialog import askopenfilename
###Main tKinter Functions###
def keyPressed(event, data): 
    pass

#opens various screens based on what you click
def mousePressed(event, data): 
    if 0.125*data.width<event.x<0.625*data.width and 0.25*data.height<event.y<0.45*data.height:
        #The next three lines of code are modified from: 
        #https://stackoverflow.com/questions/7994461/choosing-a-file-in-python3
        #and https://stackoverflow.com/questions/10993089/opening-and-reading-a-file-with-askopenfilename
        #must be patient and wait a second to open the file loading screen 
        root=Tk()
        root.withdraw()
        data.pathname = askopenfilename(initialdir="/",
                                  title='Please select a file')
        data.mode="TextbookScreen"
        data.previousMode="LoadScreen"
    elif 0.125*data.width<event.x<0.625*data.width and 0.60*data.height<event.y<0.80*data.height: 
        data.mode="NoteScreen"
        data.previousMode="LoadScreen"
    elif 0.125*data.width<event.x<0.625*data.width and 0.90*data.height<event.y<data.height: 
        data.mode=data.previousMode
        data.previousMode="LoadScreen"

#draws the buttons
def redrawAll(canvas, data): 
    canvas.create_rectangle(0, 0, data.width, data.height, fill="green")
    canvas.create_rectangle(0.125*data.width, 0.25*data.height, 0.625*data.width, 
    0.45*data.height, fill="blue")
    canvas.create_text(0.15*data.width, 0.30*data.height, text="Upload Textbook", 
    anchor="nw", font="Arial 16 bold")
    canvas.create_text(0.15*data.width, 0.50*data.height,
     text="Please upload a .txt file", font="Arial 16 bold", anchor="nw")
    #creates a rectangle and some text to make a rectangle and text for note screen
    canvas.create_rectangle(0.125*data.width, 0.60*data.height, 0.625*data.width,
    0.80*data.height, fill="blue")
    canvas.create_text(0.15*data.width, 0.70*data.height, anchor="nw", 
    text="Make Notes for Self", font="Arial 16 bold")
    canvas.create_rectangle(0.125*data.width, 0.90*data.height, 0.625*data.width, data.height, fill="blue")
    canvas.create_text(0.15*data.width, 0.95*data.height, anchor="nw", 
    text="Go Back", font="Arial 16 bold")