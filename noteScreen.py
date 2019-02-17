#Note Screen tkinter File
import string
import tkinter as tk
###Helper Functions
#Top Level Code is from 
#https://stackoverflow.com/questions/42211865/how-to-add-text-to-a-toplevel-window 
def create_window():
    warning="That is not a possible location"
    window=tk.Toplevel(height=500, width=100)
    tk.Label(window, text=warning).pack(padx=20, pady=10)
def create_window_save(): 
    message="Saved!"
    window=tk.Toplevel(height=500, width=100)
    tk.Label(window, text=message).pack(padx=20, pady=10)
#The next functions are part of justifyText, taken from a past homework 
#assignment. 
#aligns text to the same width for each line
def formattedText(text,width):
    result=""
    newWordIndex = 0
    count = 0
    for i in range(len(text)):
        if(text[i]== " " and count<=width):
            result+=text[newWordIndex:i+1]
            newWordIndex = i+1
            count+=1
        elif(text[i]== " " and count>width):
            result+= "\n" + text[newWordIndex:i+1]
            count=len(text[newWordIndex:i+1])
            newWordIndex = i+1
        else:
            count+=1
    return result

#takes a string (which may contain various kinds of whitespace)
#and a width (which you may assume is a positive integer),
#and returns that same text as a multi-line string that is left- and right-
#justified to the given line width
def justifyText(text, width):
    text = " ".join(text.split()) + " "
    text = formattedText(text,width)
    text+='`'
    result = ""
    for line in text.split("\n"):
        if(line[-1]=='`'):
            result+=line[:-1]
            break
        if(len(line.strip())==width):
            result+=line.strip()+"\n"
        else:
            line=line.strip()
            extraSpacesToAdd = width - len(line)            
            numOfSpaces = line.count(" ")
            if numOfSpaces>0:
                spacesToAdd = extraSpacesToAdd//numOfSpaces
                remainderOfSpaces = extraSpacesToAdd%numOfSpaces
            for word in line.split(" "):
                if(remainderOfSpaces>0):
                    result+= word + " " * (spacesToAdd + 2)
                    remainderOfSpaces-=1
                else:
                    result+= word + " " * (spacesToAdd+1)
            result=result.strip()+"\n"
    return result[:-1]
###Main TKinter Code for Note Screen
def redrawAll(canvas, data): 
    canvas.create_rectangle(0, 0, data.width, data.height, fill="orange")
    #makes the add button in upper left, makes the save button in upper right
    #makes a select button in lower left
    canvas.create_rectangle(0, 0, data.width//8, data.height//8, outline="blue", 
    width=7, fill="white")
    canvas.create_text(10, 0.06*data.height, text="Add", font="Arial 16 bold", 
    fill="blue", anchor="nw")
    canvas.create_rectangle(0.85*data.width, 0, data.width, data.height//8, 
    outline="blue", width=7, fill="white")
    canvas.create_text(0.90*data.width, 0.06*data.height, text="Save", 
    font="Arial 16 bold", fill="blue", anchor="nw")
    canvas.create_rectangle(0, 0.90*data.height, 0.25*data.width,data.height, 
    fill="white", width=7, outline="blue")
    canvas.create_text(5, 0.92*data.height, font="Arial 16 bold", text="Select", 
    anchor="nw", fill="blue")
    canvas.create_rectangle(0.85*data.width, 0.90*data.height, data.width, 
    data.height, fill="white", width=7, outline="blue")
    canvas.create_text(0.85*data.width, 0.92*data.height, font="Arial 16 bold", 
    text="Go Back", anchor="nw", fill="blue")
    for note in data.notes:
        if note[2]==True: 
            if note[4]=="Rectangle": 
                canvas.create_rectangle(note[0], note[1], fill="AntiqueWhite1", 
                outline="green", width=7)
                newTxt=justifyText(note[3], 200)
                canvas.create_text(note[0], anchor="nw", font="Arial 14 bold", 
                text=newTxt)
            else: 
                canvas.create_oval(note[0], note[1], fill="AntiqueWhite1", 
                outline="green", width=7)
                canvas.create_text(note[0], anchor="nw", font="Arial 14 bold", 
                text=note[3])
        else: 
            if note[4]=="Rectangle": 
                canvas.create_rectangle(note[0], note[1], fill="AntiqueWhite1")
            else: 
                canvas.create_oval(note[0], note[1], fill="AntiqueWhite1")
    #creates a popupwindow if the createNote is True
    if data.createNote==True: 
        canvas.create_rectangle(0.125*data.width,data.height//8, 0.90*data.width,0.90*data.height, fill="pink")
        canvas.create_text(0.25*data.width, 0.15*data.height, text="Choose a note style:", 
        font="Arial 16 bold", fill="AntiqueWhite1", anchor="nw")
        canvas.create_rectangle(0.25*data.width, 0.20*data.height, 0.40*data.width, 0.35*data.height, fill="AntiqueWhite1")
        canvas.create_oval(((0.60*data.width)-30), ((0.30*data.height)-30), ((0.60*data.width)+30), ((0.30*data.height)+30), 
        fill="AntiqueWhite1")

#Adds the text to the specified note
def keyPressed(event, data):
    print(event.keysym)
    for note in data.notes: 
        if note[2]==True: 
            if event.keysym in string.ascii_letters: 
                note[3]+=event.keysym
            elif event.keysym=="space": 
                note[3]+=" "
            elif event.keysym=="BackSpace": 
                note[3]=note[3][:-1]
            elif event.keysym=="Return": 
                note[3]+="\n"
            elif event.char in string.punctuation: 
                note[3]+=event.char
        
#Specifies what functions to go to based on what was clicked     
def mousePressed(event, data):
    if data.creatingNoteRectangle==True: 
        data.notes.append([(event.x-100, event.y-100), (event.x+100, 
        event.y+100), False, "", "Rectangle"])
        data.creatingNoteRectangle=False
    elif data.creatingNoteCircle==True: 
        data.notes.append([(event.x-100, event.y-100), (event.x+100, 
        event.y+100), False, "", "Circle"])
        data.creatingNoteCircle=False
    if data.selected==True: 
        for note in data.notes: 
            if note[0][0]<event.x<note[1][0] and note[0][1]<event.y<note[1][1]: 
                note[2]=True
            #Turn all others previously selected off
            else: 
                note[2]=False
    if data.createNote==True: 
        #clicked on the rectangle inside the add screen
        if 0.25*data.width<event.x<0.40*data.width and\
         0.20*data.height<event.y<0.35*data.height: 
            data.createNote=False
            data.creatingNoteRectangle=True
        #Clicked on the circle inside the add screen
        elif ((0.60*data.width)-30)<event.x<((0.60*data.width)+30) and \
        ((0.30*data.height)-30)<event.y<((0.30*data.height)+30): 
            data.createNote=False
            data.creatingNoteCircle=True
    #Select a note to write in it
    if 0<event.x<0.25*data.width and 0.90*data.height<event.y<data.height: 
        data.selected=True
    #Clicked the Add button
    if 0<event.x<data.width//8 and 0<event.y<data.height//8: 
        data.createNote=True
    #save Note
    if 0.85*data.width<event.x<data.width and 0<event.y<data.height//8: 
        #save note
        create_window_save()
    #Go back to previous screen
    if 0.85*data.width<event.x<data.width and \
    0.90*data.height<event.y<data.height: 
        data.mode=data.previousMode
        data.previousMode="NoteScreen"
        