#Specifically taken from Animation Time Based Animations
#on the 15-112 Course Website
# Basic AnEimation Framework and Run Function (without modification)
#Was taken from this link: 
#https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html

from tkinter import *
from tkinter import filedialog
import tkinter as tk
from PIL import Image
from PIL import ImageTk
import random
import startScreen
import logIn
import signUp
import noteScreen
import loadFile
import textbook
import UserAuthentication
import cv2
import threading
import pupil



####Helper Functions Called Within Main tKinter Code###
def makeCircles(speed, radius, width):
    numCircles=10
    circlesList=[]
    colorsLst=["yellow", "orange", "pink", "green"]
    for i in range(numCircles): 
        bounds=(radius, width-radius)
        circlesList.append([random.randint(bounds[0], bounds[1]),
                            random.randint(bounds[0], bounds[1]), speed, 
                            random.choice(colorsLst)])
    return circlesList


def determineChange(data): 
    #order of variables is newX, oldX, newY, oldY
    print(data.pupilLocation)   
    newX, oldX=data.pupilLocation[0], data.pupilLocation[1]
    newY, oldY=data.pupilLocation[2], data.pupilLocation[3]
    changeX=(newX-oldX)
    changeY=(newY-oldY)
    sigChange=5
    if 0<data.pointerCX+(changeX)<data.width: 
        data.pointerCX+=(3*changeX)
    if 0<data.pointerCY+(changeY)<data.height: 
            data.pointerCY+=(5*changeY)
####################################
# customize these funcEtions
####################################

def init(data):
    data.mode="StartScreen"
    data.previousMode=""
    data.time=0
    data.pupilLocation=[]
    data.pointerCX, data.pointerCY=data.width//2, data.height//2
    data.clickedUser=False
    data.clickedPass=False
    data.creatingNote=False
    data.pointerR=30
    data.radius=25
    data.speed=4
    data.seeAll=False
    data.user=""
    data.password=""
    data.fill=""
    data.createNote=False
    data.pathname=""
    # data.pathname=r"C:\Users\ankit\Box\Carnegie Mellon University\First Semester Freshman Year\15-112 Fundamentals of Programming\Term Project\files\SampleTextFile_10kb.txt"
    data.selected=False
    data.wordLook=False
    #start with the rectangle extended this much and then change it later
    #can fit 33 lines inside the current screen height of 600
    #each line is about 20 pixels
    data.textBottom=data.height+100
    data.textTop=0
    data.textHeight=0
    data.loaded=False
    data.wrongPass=False
    data.textLst=[]
    data.database=UserAuthentication.UserAuthentication()
    data.clickedLst=[]
    data.highlight=False
    data.notes=[]
    data.note=""
    data.delete=[]
    data.notesForTxt=[]
    data.searchText=""
    data.search=False
    data.searchRes=[]
    data.startRes=0
    data.displaySearch=True
    data.creatingNoteRectangle=False
    data.creatingNoteCircle=False
    #default is last index
    data.noteIndex=-1
    data.border=False
    data.noteText=""
    #I got this from Stack Overflow: https://stackoverflow.com/questions/10133856/how-to-add-an-image-in-tkinter
    data.stickyNoteImage= ImageTk.PhotoImage(Image.open(r"C:\Users\ankit\Box\Carnegie Mellon University\First Semester Freshman Year\15-112 Fundamentals of Programming\Term Project\image\stickyNote.png"))
    data.circles=makeCircles(data.speed, data.radius, data.width)
def mousePressed(event, data):
    # use event.x and event.y
    if data.mode=="StartScreen": startScreen.mousePressed(event, data)
    elif data.mode=="LogIn": logIn.mousePressed(event, data)
    elif data.mode=="SignUp":signUp.mousePressed(event, data)
    elif data.mode=="NoteScreen": noteScreen.mousePressed(event, data)
    elif data.mode=="LoadScreen": loadFile.mousePressed(event, data)
    elif data.mode=="TextbookScreen": textbook.mousePressed(event, data)
    elif data.mode=="WordLook":wordLook.mousePressed(event, data)
def keyPressed(event, data):
    if data.mode=="LogIn": logIn.keyPressed(event, data)
    elif data.mode=="SignUp":signUp.keyPressed(event, data)
    elif data.mode=="NoteScreen": noteScreen.keyPressed(event, data)
    elif data.mode=="LoadScreen":loadFile.keyPressed(event, data)
    elif data.mode=="TextbookScreen": textbook.keyPressed(event, data)
    elif data.mode=="WordLook": wordLook.keyPressed(event, data)
def timerFired(data):
    if data.mode=="StartScreen" or data.mode=="LogIn" or data.mode=="SignUp": startScreen.timerFired(data)
    data.pupilLocation=[pupil.newXAvg, pupil.oldXAvg, pupil.newYAvg, pupil.oldYAvg]
    # print(data.pupilLocation) 
    determineChange(data)
def redrawAll(canvas, data):
    # draw in canvas
    if data.mode=="StartScreen": startScreen.redrawAll(canvas, data)
    elif data.mode=="LogIn": logIn.redrawAll(canvas, data)
    elif data.mode=="waiting": redrawAllWaiting(canvas, data)
    elif data.mode=="SignUp": signUp.redrawAll(canvas, data)
    elif data.mode=="NoteScreen": noteScreen.redrawAll(canvas, data)
    elif data.mode=="LoadScreen": loadFile.redrawAll(canvas, data)
    elif data.mode=="TextbookScreen": textbook.redrawAll(canvas, data)
    elif data.mode=="WordLook": wordLook.redrawAll(canvas, data)

    
    
####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)
        
    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay=100
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    #I got this to from:https://stackoverflow.com/questions/14910858/how-to-specify-where-a-tkinter-window-opens
    #moves the tKinter window so that it doesn't open at exact same spot as the webcam window
    root.geometry("600x600+600+100")
    root.mainloop() # blocks until window is closed
    print("bye!")
    
#Threading Module Code from: 
#https://stackoverflow.com/questions/49816348/running-webcam-and-tkinter-at-the-same-time
th=threading.Thread(target=pupil.main)
th.setDaemon(True)
th.start()
run(600, 600)
