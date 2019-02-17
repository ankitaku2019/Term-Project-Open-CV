#File for logging in for tkinter
import string
import UserAuthentication as userA
###Helper Functions###
#shows password as asterisks rather than the actual password
def hidePassword(data): 
    showforPass=""
    for i in range(len(data.password)): 
        showforPass+="*"
    return showforPass
    
        
###Tkinter Log In Functions###
#specifies where to go based in what you click
def mousePressed(event, data): 
    if data.width//4<event.x<0.75*data.width and 0.25*data.height<event.y<0.375*data.height:
        data.clickedPass=False
        data.clickedUser=True
    elif data.width//4<event.x<0.75*data.width and 0.5*data.height<event.y<0.625*data.height:
        data.clickedUser=False 
        data.clickedPass=True
    elif data.width//4<event.x<0.75*data.width and 0.80*data.height<event.y<0.90*data.height: 
        if data.database.checkPassword(data.user, data.password)==False: 
            data.wrongPass=True
        else: 
            data.wrongPass=False
            #resets the username and password in case users switch later
            data.password, data.user="", ""
            data.mode="LoadScreen" 

#The idea of event.char came from this Stack Overflow post: 
#https://stackoverflow.com/questions/19264066/tracing-keypresses-in-python    
def keyPressed(event, data): 
    print(event.char)
    if event.char in string.ascii_letters or event.char in string.digits \
    or event.char in string.punctuation==True: 
        if data.clickedUser==True: 
            data.user+=event.char
        if data.clickedPass==True:
            data.password+=event.char
    elif event.keysym=="BackSpace":
        if data.clickedUser==True: 
            data.user=data.user[:-1]
        elif data.clickedPass==True: 
            data.password=data.password[:-1]
    print(data.password)

#draws in the log in functions    
def redrawAll(canvas, data):
    #create this first, otherwise gets hidden by background
    #not quite working
    if data.wrongPass==True: 
        canvas.create_rectangle(data.width//4, 0.75*data.width, data.height//4, 0.75*data.height, fill="pink")
        canvas.create_text(data.width//2, data.height//2, text="WRONG PASSWORD! Try again!", fill="AntiqueWhite1")
    #creates the background
    canvas.create_rectangle(0, 0, data.width, data.height,fill="blue")
    #username and its coressponding rectangle
    canvas.create_text(10, data.height//4, anchor="nw", text="Username:", font="Arial 16 bold", fill="orange")
    canvas.create_rectangle(data.width//4, data.height//4, 0.75*data.width, 0.375*data.height, outline="orange", width=7)
    #types username for the letters you type in 
    canvas.create_text(data.width//2, 0.30*data.height, font="Arial 16 bold", text=data.user)
    #password and its corresponding rectangle
    canvas.create_text(10, 0.5*data.height, anchor="nw", text="Password:", font="Arial 16 bold", fill="orange")
    canvas.create_rectangle(data.width//4, 0.5*data.height, 0.75*data.width, 0.625*data.height, outline="orange", width=7)
    #types asterisks for the password that someone types in 
    canvas.create_text(data.width//2, 0.55*data.height, text=hidePassword(data), font="Arial 16 bold")
    #GO and its corresponding rectangle
    canvas.create_rectangle(data.width//4, 0.80*data.height, 0.75*data.width, 0.90*data.height, fill="AntiqueWhite1")
    canvas.create_text((data.width//2)-20, 0.83*data.height, anchor="nw", text="GO!", font="Arial 16 bold", fill="orange")