#specifies where to go based on where you have clicked
def mousePressed(event, data): 
    if 0.125*data.width<event.x<0.375*data.width and 0.75*data.height<event.y<0.875*data.height: 
        data.mode="LogIn"
        data.previousMode="StartScreen"
    elif 0.625*data.width<event.x<0.875*data.width and 0.75*data.height<event.y<0.875*data.height: 
        data.mode="SignUp"
        data.previousMode="StartScreen"
#makes the dynamic moving backgrounds
def timerFired(data): 
    newCircles=[]    
    for i in range(len(data.circles)):
        circle=data.circles[i] 
        x, y, speed, color=circle[0], circle[1], circle[2], circle[3]
        x+=speed
        if x+data.radius>=data.width or x-data.radius<=0: 
            speed=-speed
        newCircles.append([x, y, speed, color])
    data.circles=newCircles
        
 #draws all items    
def redrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill="blue")
    for circle in data.circles: 
        x, y, speed, color=circle[0], circle[1], circle[2], circle[3]
        canvas.create_oval(x-data.radius, y-data.radius, x+data.radius, y+data.radius, fill=color)
    canvas.create_text(data.width//2, data.height//4,font="Arial 24 bold", fill="orange", 
    text="Welcome to")
    canvas.create_text(data.width//2, data.height//2, font="Arial 24 italic", fill="orange", text="~Beyond Productivity~")
    #the login and signup buttons are created below
    canvas.create_rectangle(data.width//8, 0.75*data.height, 0.375*data.width, 0.875*data.height, fill="old lace")
    canvas.create_text(0.25*data.width,0.80*data.height, text="Log In", font="Arial 16")
    canvas.create_rectangle(0.625*data.width, 0.75*data.height, 0.875*data.width, 0.875*data.height, fill="old lace")
    canvas.create_text(0.75*data.width, 0.80*data.height, text="Sign Up", font="Arial 16")
    #Creates the pointer circle that fluctuates with openCV
    canvas.create_oval(data.pointerCX-data.pointerR, data.pointerCY-data.pointerR,
    data.pointerCX+data.pointerR, data.pointerCY+data.pointerR, fill="red")