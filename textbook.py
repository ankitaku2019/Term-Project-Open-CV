import string
import copy
import tkinter as tk
###Helper Functions###
#This function is from the 112 website to read filename. 
#Link: https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO 
def readFile(path):
    with open(path, "rt") as f:
        return f.read()
#The next function is justifyText, taken from a past homework assignment. 
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

#helper function to format the text    
def formatText(data): 
    text=readFile(data.pathname)
    formattedText=justifyText(text, 40)
    return formattedText

class ManipulateText(object):
    #text would be formatted already when placed in here 
    def __init__(self, text): 
        self.text=text
        self.txtLst=[]
        # self.numLines=(len(self.text)/50)
        #33 is the number of lines the current height can fit
    #makes a list of all the words in the text
    def getLineNum(self): 
        txtLst=[]
        for i in range(0, len(self.text),41): 
            self.txtLst.append([self.text[i:i+40]])
        return self.txtLst
    #highlights the appropriate text
    def highlight(self, x, y, fill, textHeight):
        #19 includes a little space above letters
        wordHeight=19
        textStart=120
        lineNumShift=abs(textHeight)//wordHeight
        x=x-textStart
        # y=y+textHeight
        #has the correct line
        lineNum=(y//wordHeight)
        lineNum+=lineNumShift
        txtStr=str(self.txtLst[lineNum])
        txtStr=txtStr[2:-1]
        currLineLst=txtStr.split(" ")
        print(currLineLst, lineNum)
        lengthLine=0
        letterLen=9
        spaceLen=9
        wordInd=-1
        word=None
        while lengthLine<x:
            wordInd+=1
            word=currLineLst[wordInd]
            if len(word)>0: 
                lengthLine+=((len(word)*letterLen)+letterLen)
            if len(word)==0: 
                lengthLine+=spaceLen
        rectStart=120
        for index in range(wordInd): 
            if len(currLineLst[index])>0:
                rectStart+=((len(currLineLst[index])*letterLen)+letterLen)
            if len(currLineLst[index])==0: 
                rectStart+=spaceLen
        # print(currLineLst[wordInd])
        # print(len(currLineLst[wordInd]))
        return [[rectStart, wordHeight*(lineNum-lineNumShift)], 
        [(rectStart+((len(currLineLst[wordInd]))*letterLen)), 
        wordHeight*((lineNum-lineNumShift)+1)], fill, [lineNum, wordInd]]
    
        
    
    #finds word user is looking for
    def findWord(self, phrase):
        searchRes=[] 
        for i in range(len(self.txtLst)):
            line=self.txtLst[i]
            txtStr=str(line)
            txtStr=txtStr[2:-1] 
            txtStr=txtStr.lower()
            if phrase in txtStr: 
                searchRes.append([txtStr, i])
        return searchRes

#creates the yellow rectangle beneath the text to emulate a highlight        
def mousePressedHighlight(newTxt, x, y, data):
        highlightInfo=newTxt.highlight(x, y, data.fill, data.textHeight)
        data.clickedLst.append(highlightInfo)
        if data.creatingNote==True: 
            #excludes the fill color
            #due to list aliasing, must do a deepcopy
            coordsForSticky=copy.deepcopy(highlightInfo)
            #only need the first two indices
            coordsForSticky=coordsForSticky[0:2]
            #this is for note writing
            coordsForSticky.append("")
            if coordsForSticky[0][1]>=data.height//2:
                coordsForSticky[0][1]-=20
                coordsForSticky[1][1]-=120
            else: 
                coordsForSticky[0][1]+=20
                coordsForSticky[1][1]+=120
            #makes a uniform post it sticky note
            shift=150-(coordsForSticky[1][0]-coordsForSticky[0][0])
            coordsForSticky[1][0]+=shift
            data.notesForTxt.append(coordsForSticky)
#allows users to delete notes after creation            
def findNoteIndex(notesForTxt, box): 
    xCoord=box[0]
    for i in range(len(notesForTxt)): 
        #this is the only value that will match the data.clickedLst portion
        if notesForTxt[i][0][0]==xCoord[0]:
            return i 

#moves highlight and notes after people scroll
def moveBoxes(data, moveBy):
    #3rd index indicates the fill and doesn't have to be changed
    coordRange=2 
    for rectangle in data.clickedLst:
        for coord in range(coordRange):
            rectangle[coord][1]+=moveBy
    for noteBox in data.notesForTxt: 
        for coord in range(coordRange):
            noteBox[coord][1]+=moveBy
#helper function to draw notes
def drawNotes(canvas, notesForTxt, index): 
    note=notesForTxt[index]
    canvas.create_rectangle(note[0], note[1], fill="yellow", outline="green", width=5)
    noteTxt=justifyText(notesForTxt[index][2], 20)
    canvas.create_text(note[0], anchor="nw", font="Arial 14", 
    text=noteTxt)

#Configured this to contain the text you need
#for the option you choose 
#top level windows
#Top Level Code is from 
#https://stackoverflow.com/questions/42211865/how-to-add-text-to-a-toplevel-window       
def create_window(option):
    instructions={"Highlight": "Click highlight button and then select the \n"+
    "word you wish to highlight. To delete, select the word and then click \n" +
    "delete on your keyboard.", "Note" : "To take a note on specific word \n" +
    "please select the word you wish to take a note on. The word will \n" +
    "be highlighted in green and a sticky note will show up. Begin typing \n" +
    "and the words will show up on the sticky note. To make the sticky note \n"+
    "go away (but automatically save your text), click below the \n" +
    "note. To see a sticky note again, click on the green highlighted box \n" +
    "of your choice. To delete, click on the box of your choice and press \n" +
    "delete on your keyboard", "Find Word": "Begin typing for results \n" +
    "to show up in the white textbox at top of screen. Results will show \n" +
    "up in the middle of screen. If you click on a result, the text will \n" +
    "scroll to that point and the sentence with the word you are looking \n"+ 
    "for will be at the top" }
    window=tk.Toplevel(height=500, width=100)
    tk.Label(window, text=instructions[option]).pack(padx=20, pady=10)
    
###Main tkInter for Textbook Page###
def mousePressed(event, data): 
    print(event.x, event.y)
    #setting up the formatted text to 
    fixedText=formatText(data)
    newTxt=ManipulateText(fixedText)
    txtLst=newTxt.getLineNum()
    if 0<event.x<0.125*data.width:
        #start the fraction at 0.125
        options=["Highlight", "Note", "Find Word", "See Notes", "Go Back"]
        fraction=0.125
        counter=0
        while fraction<=0.625: 
            if (fraction*data.height)<event.y<((fraction+0.125)*data.height): 
                #print(txtLst)
                if options[counter]=="Highlight":
                    data.highlight=True
                    create_window("Highlight")
                    data.fill="yellow"
                elif options[counter]=="Note": 
                    data.highlight=True
                    data.fill="green"
                    data.creatingNote=True
                    create_window("Note")
                else:
                    #stops highlighting at that point
                    data.highlight=False
                    data.creatingNote=False
                    if options[counter]=="Find Word": 
                        data.wordLook=True
                        create_window("Find Word")
                    elif options[counter]=="See Notes":
                        data.seeAll=True
                #goes back to the previous screen
                    elif options[counter]=="Go Back": 
                        data.mode=data.previousMode
                        data.previousMode="TextbookScreen"
            counter+=1
            fraction+=0.125

    elif 0.875*data.width<event.x<data.width and 0<event.y<0.125*data.height: 
        #implements scrollX and scrollY, up
        data.textHeight+=20
        moveBoxes(data, 20)
    elif 0.875*data.width<event.x<data.width and data.height-(0.125*data.height)<event.y<data.height: 
        #implements scrollX and scrollY, down
        data.textHeight-=20
        moveBoxes(data, -20)
    else:
        data.seeAll=False
        #will render highlight multiple unusable for now
        if data.highlight==True: 
            mousePressedHighlight(newTxt, event.x, event.y, data)
            data.highlight=False
        #checks if anything in data.clickedLst has been clicked on 
        for i in range(len(data.clickedLst)):
            box=data.clickedLst[i]
            print("This is the box coordinates")
            print(box)
            if box[0][0]<event.x<box[1][0] and box[0][1]<event.y<box[1][1]: 
                #note and not a highlight
                #there are notes if it enters next loop
                if box[2]=="green":
                    print("This is the list of notesForTxt") 
                    print(data.notesForTxt)
                    data.noteIndex=findNoteIndex(data.notesForTxt, box)
                    data.creatingNote=True
                    data.delete=[i, data.noteIndex]
                if box[2]=="yellow": 
                    data.delete=[i]
        if data.creatingNote==True:
            #have made the post-it coordinates
            #does not automatically go out of bounds for next click now
            if data.notesForTxt!=[] and data.noteIndex!=-1: 
                coords=data.notesForTxt[data.noteIndex]
                #clicked outside note
                if coords[0][0]>event.x or event.x>coords[1][0] and\
                coords[0][1]>event.y or event.y>coords[1][1]: 
                    data.creatingNote=False
        if data.wordLook==True: 
            if 0.15*data.width<event.x<0.875*data.width:
                counter=0 
                #goes through all the search results on the pages
                for startBox in range(60,data.startRes,30):
                    if startBox<event.y<(startBox+30):
                        #make the text start from this line instead
                        lineNum=data.searchRes[counter][1]
                        print(lineNum)
                        data.wordLook=False
                        #starts displaying from the search result line
                        data.textHeight-=((lineNum)*19)
                        moveBoxes(data, (-1*(lineNum)*19))
                    counter+=1
def keyPressed(event, data): 
    #the rectangle moves, but the text does not move
    fixedText=formatText(data)
    newTxt=ManipulateText(fixedText)
    txtLst=newTxt.getLineNum()
    if event.keysym=="Up": 
        data.textHeight+=20
        moveBoxes(data, 20)
    elif event.keysym=="Down" and data.textHeight<data.textBottom:
        data.textHeight-=20
        moveBoxes(data, -20)
    #implements section for typing into note
    if data.creatingNote==True: 
        if event.char in string.ascii_letters or event.char in string.digits \
        or event.char in string.punctuation==True:
            print(True) 
            data.notesForTxt[data.noteIndex][2]+=event.char
        elif event.keysym=="BackSpace":
            noteTxt=data.notesForTxt[data.noteIndex][2]
            noteTxt=noteTxt[:-1]
            data.notesForTxt[data.noteIndex][2]=noteTxt
        elif event.keysym=="space": 
            data.notesForTxt[data.noteIndex][2]+=" "
        elif event.keysym=="Return": 
            data.notesForTxt[data.noteIndex][2]+="\n"
    #key pressed for searching for things
    if data.wordLook==True: 
        searchText=""
        if event.char in string.ascii_letters or event.char in string.digits \
        or event.char in string.punctuation==True: 
            data.searchText+=event.char
        elif event.keysym=="BackSpace":
            data.searchText=data.searchText[:-1]
        elif event.keysym=="space": 
            data.searchText+=" "
        elif event.keysym=="Return":
            searchRes=newTxt.findWord(data.searchText)
            data.searchRes=searchRes
            print(data.searchRes)
    if data.delete!=[]: 
        if event.keysym=="Delete": 
            data.clickedLst.pop(data.delete[0])
            #if there are more values in the list still
            if data.delete!=[]: 
                data.notesForTxt.pop(data.delete[0])
            data.delete=[]
    if data.highlight==True: 
        if event.keysym=="Right": 
            newLastHighlight=newTxt.highlightMultiple(data.clickedLst[-1])
            data.clickedLst[-1]=newLastHighlight
            
            
        
        
def redrawAll(canvas, data): 
    #draws the left side buttons
    canvas.create_rectangle(0, 0, 0.125*data.width, data.height, fill="magenta")
    canvas.create_text(10, 10, text="Menu", 
    font="Arial 14 underline", fill="blue", anchor="nw")
    #creates all buttons on left side undernath this code
    canvas.create_rectangle(0, 0.125*data.height, 
    0.125*data.width, 0.25*data.height, width=3)
    canvas.create_text(10, 0.13*data.height,font="Arial 12", anchor="nw", text="Highlight")
    canvas.create_rectangle(0, 0.25*data.height,0.125*data.width, 
    0.375*data.height, width=3)
    canvas.create_text(10, 0.30*data.height,font="Arial 12", anchor="nw", text="Note")
    canvas.create_rectangle(0, 0.375*data.height,0.125*data.width, 
    0.5*data.height, width=3)
    canvas.create_text(10, 0.40*data.height, font="Arial 12",
    anchor="nw", text="Find")
    canvas.create_text(10, 0.43*data.height, font="Arial 12", anchor="nw", text="Word")
    canvas.create_rectangle(0, 0.5*data.height, 0.125*data.width, 0.625*data.height, width=3)
    canvas.create_text(10,0.53*data.height, font="Arial 12",
    anchor="nw", text="See")
    canvas.create_text(10,0.57*data.height, font="Arial 12",
    anchor="nw", text="Notes")
    canvas.create_rectangle(0, 0.625*data.height, 0.125*data.width, 0.75*data.height, width=3)
    canvas.create_text(10, 0.7*data.height, font="Arial 12", anchor="nw", text="Go Back")
    #creates the right scrollbar, up arrow, and down arrow
    canvas.create_rectangle(0.875*data.width, 0, data.width, data.height, fill='magenta')
    #creates the up arrow box
    canvas.create_rectangle(0.875*data.width, 0, data.width, 0.125*data.height, width=3)
    canvas.create_line(0.9375*data.width, 10, 0.9375*data.width, 0.1*data.height, width=3)
    canvas.create_line(0.9375*data.width, 10, 0.90625*data.width, 40, 
    width=3)
    canvas.create_line(0.9375*data.width, 10,0.96875*data.width, 40, 
    width=3)
    #creates the down arrow box
    canvas.create_rectangle(0.875*data.width, (data.height-(0.125*data.height)), data.width, data.height, width=3)
    canvas.create_line(0.9375*data.width, (data.height-(0.10*data.height)), 0.9375*data.width, data.height-20, width=3)
    canvas.create_line(0.9375*data.width, data.height-20, 0.90625*data.width, data.height-40, 
    width=3)
    canvas.create_line(0.9375*data.width, data.height-20,0.96875*data.width, data.height-40, 
    width=3)
    #create the textbook in the middle
    if data.wordLook==False: 
        if data.clickedLst!=[]: 
            for box in data.clickedLst:
                canvas.create_rectangle(box[0], box[1], fill=box[2])
        #creates the text for the screen/loads the textbook
        formattedText=formatText(data)
        canvas.create_rectangle(0.13*data.width, 0, 0.85*data.width, 
        data.height, width=5)
        #Consolas is a monospace font (idea given by my mentor Sanjna)
        #font was found on the Tkinter font documentation
        canvas.create_text(0.20*data.width, data.textHeight, text=formattedText, 
        anchor="nw", font="Consolas 12") 
    #draws search box instead
    if data.wordLook==True: 
        canvas.create_rectangle(0, 30, 0.125*data.width, 70, fill="AntiqueWhite1")
        canvas.create_text(0, 30, anchor="nw", font="Arial 12", text=data.searchText)
        if data.searchRes!=[]: 
            data.startRes=60
            for i in range(len(data.searchRes)):
                #first index is the result 
                res=data.searchRes[i][0]
                endRes=data.startRes+30 
                canvas.create_rectangle(0.15*data.width, data.startRes, 0.875*data.width, endRes, fill="AntiqueWhite1")
                canvas.create_text(0.15*data.width, data.startRes, font="Arial 12", anchor="nw", text=res)
                data.startRes=endRes
        #if there are no search results after the user has typed something
        elif data.searchRes==[] and data.searchText!="":
            canvas.create_text(data.width//2, data.height//2, text="No Results", font="Arial 12")
    #draws the the note boxes after the text
    #covers up the text/not transparent anymore
    if data.notesForTxt!=[]: 
        if data.creatingNote==True: 
            drawNotes(canvas, data.notesForTxt, data.noteIndex)
        elif data.seeAll==True: 
            for j in range(len(data.notesForTxt)): 
                drawNotes(canvas, data.notesForTxt, j)
    

    
    