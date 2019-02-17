#Creates a user authentication class to create and save users 
import string
class UserAuthentication(object):
    def __init__(self): 
        self.userDict={}
    #creates a new User
    def createNewUser(self, username, password): 
        self.userDict[username]=password
        countSpecialChar, countUpper, countLower, countDig=0, 0, 0, 0
        for letter in password: 
            if letter in string.ascii_letters: 
                if letter in string.ascii_lowercase: 
                    countLower+=1
                elif letter in string.ascii_uppercase: 
                    countUpper+=1
            elif letter in string.digits: 
                countDig+=1
            elif letter in string.punctuation: 
                countSpecialChar+=1
        #passes the strong password test
        #ignore the special Char, because it's having problems
        # if countSpecialChar!=0 and 
        if countUpper!=0 and countLower!=0 and countDig!=0: 
            self.writeFile(r"C:\Users\ankit\Box\Carnegie Mellon University\First Semester Freshman Year\15-112 Fundamentals of Programming\Term Project\files\userDictionary.txt")
        #forces the person to try again with their password
        else: 
            return False
    #makes sure the passwords match
    def checkPassword(self, username, password):
        #read text file that contains the user dictionaries
        userDict=UserAuthentication.readFile(r"C:\Users\ankit\Box\Carnegie Mellon University\First Semester Freshman Year\15-112 Fundamentals of Programming\Term Project\files\userDictionary.txt")
        index, pastIndex=0, -1
        tmpKey=""
        tmpPassword=""
        while index<len(userDict):
            if userDict[index]==":":
                tmpKey=userDict[pastIndex+1:index]
                pastIndex=index
            elif userDict[index]=="\n":
                tmpPassword=userDict[pastIndex+1:index]
                self.userDict[tmpKey]=tmpPassword
                pastIndex=index
            index+=1
        #goes through the user dictionary and checks the password
        for key in self.userDict: 
            if username==key: 
                if self.userDict[username]==password: 
                    return True
                return False
        return False
    #The two functions below are taken from the CMU course website: 
    #Link: https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
    def writeFile(self, path):
        userString=""
        with open(path, "wt") as f:
            for key in self.userDict: 
                userString+=key+":"
                userString+=self.userDict[key]+"\n"
            f.write(userString)
    @staticmethod
    def readFile(path):
        with open(path, "rt") as f:
            return f.read()

        
        
        
    