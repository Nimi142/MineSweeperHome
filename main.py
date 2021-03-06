isDebug = False
vBuild = 3
'''
Note:
f = Frame()
width=f.winfo_width()
height=f.winfo_height()
'''
'''
Ways to solve problems:
High scores: Create a dictionary from a csv file with the code learned in Hemda. If dictionary is None create a new one
Screen resizing: Measure in paint.net the correct ratio between them and also detect changes in width, change over what 
was changed the most. For when, make it a key, like "R" for example.
And make a custom board setting!!! its Easyy!!!!
'''
patch = \
'''
Version = 1.0B
'''
'''
Naming System:
(X = Variable name)
!Name starts in caps (i.e vNum = 0)
Function = X
List = aX
Number = vX
String = sX
Label = lX
Button = bX
Frame = fX
TopLevel (Window) = wX
Boolean = isX
Photo = pX
Dictionary = dX
constants = cX
Time(Number) = tX
Entry = eX
'''
from tkinter import *
from PIL import Image, ImageTk
import random, time, linecache, csv
from os import stat
from _thread import start_new_thread
from math import ceil
# Create HighScores File:
try:
    open("HighScores.txt","x")
except:
    print("File exists")
if stat("HighScores.txt").st_size == 0:
    w = open("HighScores.txt", "w")
    w.write("00000,100 \n1000000,100 \n10000000,100")
    w.close()
'''
The file will look like this:
[time,clicks]
100000,100
1000000,100
10000000,100
'''

vSide = 50

# Initializing Tk instances:
main = Tk()
main.title("MineSweeper Home")
main.iconbitmap(r'c:images/logo.ico')

# main.attributes("-fullscreen", True)

wSetPlayer = Toplevel(main)
wConfigure = Toplevel(main)
wLost = Toplevel(main)
wWin = Toplevel(main)
fGame = Frame(main)
fInfo = Frame(main)
wSetPlayer.withdraw()
wLost.withdraw()
wWin.withdraw()
main.withdraw()
'''
Difficulty will be measured in numbers:
Beginner = 0 (9x9, 10 mines)
Intermediate = 1 (16x16, 40 mines)
Expert = 2 (24x24, 99 mines)
'''
# Initializing classes:
class Tile:
    Button = Button(fGame)
    isBomb = False
    isFlag = False
    xPos = 0
    yPos = 0
    bombsNear = 0
    isClicked = False
    image = None
# Initializing variables:
dBombs = {}
sName = "Set_Name"
vDifficulty = 0
vStartBombs = 10
vBoardSize = 9
vClicks = 0
tStartTime = 0
tFullTime = 0
vFlagsLeft = 0
vHighClicks = 0
vHightime = 0
vWindowSize = 0
aBoard = []
aBombs = []
aData = []
aNames = []
aHighScores = []
isStart = False
isRetry = False
isStop = False

# Configuring the photos:
pOne = ImageTk.PhotoImage(Image.open("images/one.png").resize((vSide,vSide), Image.ANTIALIAS))
pTwo = ImageTk.PhotoImage(Image.open("images/two.png").resize((vSide,vSide), Image.ANTIALIAS))
pThree = ImageTk.PhotoImage(Image.open("images/three.png").resize((vSide,vSide), Image.ANTIALIAS))
pFour = ImageTk.PhotoImage(Image.open("images/Four.png").resize((vSide,vSide), Image.ANTIALIAS))
pFive = ImageTk.PhotoImage(Image.open("images/Five.png").resize((vSide, vSide), Image.ANTIALIAS))
pSix = ImageTk.PhotoImage(Image.open("images/Six.png").resize((vSide, vSide), Image.ANTIALIAS))
pSeven = ImageTk.PhotoImage(Image.open("images/Seven.png").resize((vSide, vSide), Image.ANTIALIAS))
pEight = ImageTk.PhotoImage(Image.open("images/Eight.png").resize((vSide,vSide), Image.ANTIALIAS))
pBomb = ImageTk.PhotoImage(Image.open("images/Bomb.png").resize((vSide,vSide), Image.ANTIALIAS))
pFlag = ImageTk.PhotoImage(Image.open("images/Flag.png").resize((vSide,vSide), Image.ANTIALIAS))
pEmpty = ImageTk.PhotoImage(Image.open("images/empty.png").resize((vSide,vSide), Image.ANTIALIAS))
pUnpressed = ImageTk.PhotoImage(Image.open("images/Unpressed.png").resize((vSide,vSide), Image.ANTIALIAS))
pFlagBomb = ImageTk.PhotoImage(Image.open("images/FlaggedBomb.png").resize((vSide,vSide), Image.ANTIALIAS))

#Functions:
def setplayer():
    global eSetPlayer
    global wSetPlayer
    global sName
    global lPlayer
    sName = eSetPlayer.get()
    wSetPlayer.withdraw()
    lPlayer.configure(text=sName)


def openplayer():
    global wSetPlayer
    wSetPlayer.deiconify()
def exitfullscreen(event = None):
    global main
    main.attributes("-fullscreen",False)


def resize():
    global main
    global aBoard
    global isStop
    global vWindowSize
    global fInfo
    global pOne
    global pTwo
    global pThree
    global pFour
    global pFive
    global pSix
    global pSeven
    global pEight
    global pFlag
    global pBomb
    global pUnpressed
    global pEmpty
    global pFlagBomb
    height = main.winfo_height()
    width = main.winfo_width()
    if height != vWindowSize:
        vWindowSize = height
        vWindowSize = height
        vButtonSize = aBoard[0][0].Button.winfo_height()
        pOne = ImageTk.PhotoImage(Image.open("images/one.png").resize((vButtonSize, vButtonSize), Image.ANTIALIAS))
        pTwo = ImageTk.PhotoImage(Image.open("images/two.png").resize((vButtonSize, vButtonSize), Image.ANTIALIAS))
        pThree = ImageTk.PhotoImage(Image.open("images/three.png").resize((vButtonSize, vButtonSize), Image.ANTIALIAS))
        pFour = ImageTk.PhotoImage(Image.open("images/Four.png").resize((vButtonSize, vButtonSize), Image.ANTIALIAS))
        pFive = ImageTk.PhotoImage(Image.open("images/Five.png").resize((vButtonSize, vButtonSize), Image.ANTIALIAS))
        pSix = ImageTk.PhotoImage(Image.open("images/Six.png").resize((vButtonSize, vButtonSize), Image.ANTIALIAS))
        pSeven = ImageTk.PhotoImage(Image.open("images/Seven.png").resize((vButtonSize, vButtonSize), Image.ANTIALIAS))
        pEight = ImageTk.PhotoImage(Image.open("images/Eight.png").resize((vButtonSize, vButtonSize), Image.ANTIALIAS))
        pBomb = ImageTk.PhotoImage(Image.open("images/Bomb.png").resize((vButtonSize, vButtonSize), Image.ANTIALIAS))
        pFlag = ImageTk.PhotoImage(Image.open("images/Flag.png").resize((vButtonSize, vButtonSize), Image.ANTIALIAS))
        pEmpty = ImageTk.PhotoImage(Image.open("images/empty.png").resize((vButtonSize, vButtonSize), Image.ANTIALIAS))
        pUnpressed = ImageTk.PhotoImage(
            Image.open("images/Unpressed.png").resize((vButtonSize, vButtonSize), Image.ANTIALIAS))
        pFlagBomb = ImageTk.PhotoImage(
            Image.open("images/FlaggedBomb.png").resize((vButtonSize, vButtonSize), Image.ANTIALIAS))
        for i in aBoard:
            for self in i:
                if self.isClicked:
                    vNumBombs = self.bombsNear
                    self.Button.configure(height=height / (vBoardSize + 1), width=height / (vBoardSize + 1))
                    if vNumBombs == 1:
                        self.Button.configure(image=pOne)
                        self.image = pOne
                    elif vNumBombs == 2:
                        self.Button.configure(image=pTwo)
                        self.image = pTwo
                    elif vNumBombs == 3:
                        self.Button.configure(image=pThree)
                        self.image = pThree
                    elif vNumBombs == 4:
                        self.Button.configure(image=pFour)
                        self.image = pFour
                    elif vNumBombs == 5:
                        self.Button.configure(image=pFive)
                        self.image = pFive
                    elif vNumBombs == 6:
                        self.Button.configure(image=pSix)
                        self.image = pSix
                    elif vNumBombs == 7:
                        self.Button.configure(image=pSeven)
                        self.image = pSeven
                    elif vNumBombs == 8:
                        self.Button.configure(image=pEight)
                        self.image = pEight
                    elif vNumBombs == 0:
                        self.Button.configure(image=pEmpty)
                        self.image = pEmpty
                else:
                    self.Button.configure(image=pUnpressed)
        main.geometry(("%dx%d" % (fGame.winfo_height() + 0.2, fGame.winfo_height())))



def  update(a):
    global lTimePassed
    global tStartTime
    global isStop
    global lClicks
    global vClicks
    while isStop:
        time.sleep(0.1)
        lTimePassed.configure(text = "Time passed: " + str(round((time.time()-tStartTime))))
        lClicks.configure(text = "Clicks: "+str(vClicks))
def choosedifficulty(self,vDifficulty,event,isRetry):
    global vBoardSize
    global vStartBombs
    global main
    global wConfigure
    global lHighScore
    global isStart
    global tStartTime
    global vFlagsLeft
    global aHighScores
    global vHighClicks
    global vHightime
    global aData
    global aNames
    global vSide
    global pOne
    global pTwo
    global pThree
    global pFour
    global pFive
    global pSix
    global pSeven
    global pEight
    global pFlag
    global pBomb
    global pUnpressed
    global pEmpty
    global pFlagBomb
    # Github Thingy
    # print("Meow!")
    file_name = 'HighScores.csv'
    file = open(file_name, 'r')
    data = list(csv.DictReader(file))
    print(data)
    for i in data:
        aNames.append(i['name'])
    if vDifficulty == 0:
        vStartBombs = 10
        vBoardSize = 9
        vSide = 70
    elif vDifficulty == 1:
        vStartBombs = 40
        vBoardSize = 16
        vSide = 45
    elif vDifficulty == 2:
        vStartBombs = 99
        vBoardSize = 24
        vSide = 25
    pOne = ImageTk.PhotoImage(Image.open("images/one.png").resize((vSide, vSide), Image.ANTIALIAS))
    pTwo = ImageTk.PhotoImage(Image.open("images/two.png").resize((vSide, vSide), Image.ANTIALIAS))
    pThree = ImageTk.PhotoImage(Image.open("images/three.png").resize((vSide, vSide), Image.ANTIALIAS))
    pFour = ImageTk.PhotoImage(Image.open("images/Four.png").resize((vSide, vSide), Image.ANTIALIAS))
    pFive = ImageTk.PhotoImage(Image.open("images/Five.png").resize((vSide, vSide), Image.ANTIALIAS))
    pSix = ImageTk.PhotoImage(Image.open("images/Six.png").resize((vSide, vSide), Image.ANTIALIAS))
    pSeven = ImageTk.PhotoImage(Image.open("images/Seven.png").resize((vSide, vSide), Image.ANTIALIAS))
    pEight = ImageTk.PhotoImage(Image.open("images/Eight.png").resize((vSide,vSide), Image.ANTIALIAS))
    pBomb = ImageTk.PhotoImage(Image.open("images/Bomb.png").resize((vSide, vSide), Image.ANTIALIAS))
    pFlag = ImageTk.PhotoImage(Image.open("images/Flag.png").resize((vSide, vSide), Image.ANTIALIAS))
    pEmpty = ImageTk.PhotoImage(Image.open("images/empty.png").resize((vSide, vSide), Image.ANTIALIAS))
    pUnpressed = ImageTk.PhotoImage(Image.open("images/Unpressed.png").resize((vSide, vSide), Image.ANTIALIAS))
    pFlagBomb = ImageTk.PhotoImage(Image.open("images/FlaggedBomb.png").resize((vSide,vSide), Image.ANTIALIAS))
    vFlagsLeft = vStartBombs
    main.deiconify()
    wConfigure.grab_release()
    wLost.grab_release()
    wConfigure.withdraw()
    # print(aBombs)
    tStartTime = time.time()
    setboards()
    # print(str(aHighScores[0]) + "," + str(aHighScores[1]))
def setbombs(vStartBombs,vBoardSize,aForbiddenTiles): # Working
    global aBombs
    # Picks a random streak of points at a size predetermined by the difficulty that will be bombs
    # returns a list of list of [x,y] parameters for placement.
    aBombs = []
    for i in range (0, vStartBombs):
        # print("A")
        x = aForbiddenTiles[0][0]
        y = aForbiddenTiles[0][1]
        while [x,y] in aForbiddenTiles:
            x = random.randint(0,vBoardSize - 1)
            y = random.randint(0,vBoardSize - 1)
        aBombs.append([x,y])


def setboards(): # Working
    # This will set the aBoards array to be a matrix of the tiles(a two dimentional array)
    global vBoardSize
    global aBoard
    global vSide
    global vFlagsLeft
    global vStartBombs
    global fGame
    global fInfo
    global vWindowSize
    vFlagsLeft = vStartBombs
    height = fGame.winfo_reqheight()
    fGame.destroy()
    fGame = Frame(main)
    aBoard = []
    for i in range(0,vBoardSize):
        aBoard.append([])
        for j in range(0,vBoardSize):
            a = Tile()
            a.xPos = i
            a.yPos = j
            a.Button = Button(fGame, height=vWindowSize / (vBoardSize + 1), width=vWindowSize / (vBoardSize + 1),
                              image=pUnpressed)
            a.Button.bind("<Button-1>",leftclickbutton)
            a.Button.bind("<Button-3>",rightclick)
            a.Button.bind("<Button-2>",middleClick)
            if ([i,j] in aBombs):
                a.isBomb = True
            dBombs[a.Button] = a
            aBoard[i].append(a)
    for i in range(0, vBoardSize):
        for j in range(0, vBoardSize):
            aBoard[i][j].Button.grid(row = i, column = j)
    for i in aBoard:
        for j in i:
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if [j.xPos + x,j.yPos + y] in aBombs:
                        j.bombsNear += 1
    fInfo.pack_forget()
    fGame.pack(side = LEFT, expand  = y,anchor = W )
    fInfo.pack(side = RIGHT,anchor = N)
    fGaneheight = fGame.winfo_reqheight()
    for i in range(0, vBoardSize):
        for j in range(0, vBoardSize):
            aBoard[i][j].Button.configure(height = fGaneheight/vBoardSize,width = fGaneheight/vBoardSize)

def leftclickbutton(event,isBombSent = False):
    global vBoardSize
    global vFlagsLeft
    global aBombs
    global aBoard
    global isStart
    global dBombs
    global lFlagsLeft
    global vClicks
    global vDifficulty
    global bOpenPlayer
    global sName
    global aNames
    if type(event) is not Tile:
        realself = dBombs[event.widget]
        vClicks += 1
    else:
        realself = event
    realself.isClicked = True
    # print(aBoard)
    realself.Button['command'] = 0
    vxPos = realself.xPos
    vyPos = realself.yPos
    if not isStart:
        aForbiddenTiles = []
        for i in range(-1,2):
            for j in range(-1,2):
                aForbiddenTiles.append([vxPos+i,vyPos+j])
        setbombs(vStartBombs,vBoardSize,aForbiddenTiles)
        setboards()
        bOpenPlayer.configure(state=DISABLED)
        # print(aNames[sName])
        # if vDifficulty == 0:
        #     lHighScore.configure(text=str(aNames[sName][0]) + "\n" + str(aNames[sName][1]))
        # elif vDifficulty == 1:
        #     lHighScore.configure(text=str(aNames[sName][2]) + "\n" + str(aNames[sName][3]))
        # elif vDifficulty == 2:
        #     lHighScore.configure(text=str(aNames[sName][4]) + "\n" + str(aNames[sName][5]))
        # else:
        #     lHighScore.configure(text=str(aNames[sName][6]) + "\n" + str(aNames[sName][7]))
    isStart = True
    if realself.bombsNear == 0:
        for x in range(-1,2):
            if len(aBoard) > vxPos +x >= 0:
                for y in range(-1,2):
                    if len(aBoard[vxPos + x]) > vyPos + y >= 0:
                        self = aBoard[vxPos+x][vyPos+y]
                        vNumBombs = self.bombsNear
                        if vNumBombs == 1:
                            self.Button.configure(image =  pOne)
                            self.image = pOne
                        elif vNumBombs == 2:
                            self.Button.configure(image = pTwo)
                            self.image = pTwo
                        elif vNumBombs == 3:
                            self.Button.configure(image = pThree)
                            self.image = pThree
                        elif vNumBombs == 4:
                            self.Button.configure(image = pFour)
                            self.image = pFour
                        elif vNumBombs == 5:
                            self.Button.configure(image = pFive)
                            self.image = pFive
                        elif vNumBombs == 6:
                            self.Button.configure(image = pSix)
                            self.image = pSix
                        elif vNumBombs == 7:
                            self.Button.configure(image = pSeven)
                            self.image = pSeven
                        elif vNumBombs == 8:
                            self.Button.configure(image = pEight)
                            self.image = pEight
                        elif vNumBombs == 0:
                            self.Button.configure(image = pEmpty)
                            self.image = pEmpty
                            # print(pEmpty)
                            if not self.isClicked:
                                leftclickbutton(self,False)
                        if self.isFlag:
                            self.isFlag = False
                            vFlagsLeft += 1

                        self.isClicked = True

    else:
        if realself.isFlag:
            realself.isFlag = False
            vFlagsLeft += 1
        vNumBombs =realself.bombsNear
        self = realself
        if vNumBombs == 1:
            self.Button.configure(image=pOne)
            self.image = pOne
        elif vNumBombs == 2:
            self.Button.configure(image=pTwo)
            self.image = pTwo
        elif vNumBombs == 3:
            self.Button.configure(image=pThree)
            self.image = pThree
        elif vNumBombs == 4:
            self.Button.configure(image=pFour)
            self.image = pFour
        elif vNumBombs == 5:
            self.Button.configure(image=pFive)
            self.image = pFive
        elif vNumBombs == 6:
            self.Button.configure(image=pSix)
            self.image = pSix
        elif vNumBombs == 7:
            self.Button.configure(image=pSeven)
            self.image = pSeven
        elif vNumBombs == 8:
            self.Button.configure(image=pEight)
            self.image = pEight

        if self.isFlag:
            self.isFlag = False
            vFlagsLeft += 1
        if ([self.xPos, self.yPos] in aBombs):
            self.Button.configure(image=pBomb)
            leftclickbomb(self)
    lFlagsLeft.configure(text = "Flags left: " + str(vFlagsLeft))
    checkwin()
    # print("Meow")
def leftclickbomb(event):
    global pOne
    global pTwo
    global pThree
    global pFour
    global pFive
    global pSix
    global pSeven
    global pEight
    global pBomb
    global pFlagBomb
    global aBomb
    if not isDebug:
        # print("Unready")
        wLost.deiconify()
        wLost.grab_set()
        # Reveal all:
        for i in aBoard:
            for j in i:
                if j.bombsNear == 0:
                    j.Button.configure(image = pEmpty)
                    j.image = pEmpty
                elif j.bombsNear == 1:
                    j.Button.configure(image=pOne)
                    j.image = pOne
                elif j.bombsNear == 2:
                    j.Button.configure(image=pTwo)
                    j.image = pTwo
                elif j.bombsNear == 3:
                    j.Button.configure(image=pThree)
                    j.image = pThree
                elif j.bombsNear == 4:
                    j.Button.configure(image=pFour)
                    j.image = pFour
                elif j.bombsNear == 5:
                    j.Button.configure(image=pFive)
                    j.image = pFive
                elif j.bombsNear == 6:
                    j.Button.configure(image=pSix)
                    j.image = pSix
                elif j.bombsNear == 7:
                    j.Button.configure(image=pSeven)
                    j.image = pSeven
                elif j.bombsNear == 8:
                    j.Button.configure(image=pEight)
                    j.image = pEight
                if j.isBomb and j.isFlag:
                    j.Button.configure(image = pFlagBomb)
                elif j.isBomb:
                    j.Button.configure(image = pBomb)

def rightclick(event):
    global dBombs
    global lFlagsLeft
    global vFlagsLeft
    global isDebug
    global vClicks
    global isStart
    flag = False
    self = dBombs[event.widget]
    a =  re.findall("\d+", self.Button['image'])
    a = int(a[0])
    # print(a)
    if isStart:
        if self.isFlag:
            self.isFlag = False
            self.Button.configure(image = pUnpressed)
            vFlagsLeft += 1
        elif (not self.isClicked) or isDebug:
            if vFlagsLeft > 0 and self.isFlag == False:
                self.isFlag = True
                self.Button.configure(image=pFlag)
                vFlagsLeft -= 1
        lFlagsLeft.configure(text = "Flags left: " + str(vFlagsLeft))
        vClicks += 1
        checkwin()
def middleClick(realself):
    global aBoard
    global dBombs
    global vClicks
    realself = dBombs[realself.widget]
    vCounter = 0
    vxPos = realself.xPos
    vyPos = realself.yPos
    vClicks += 1
    for i in range(-1,2):
        for j in range(-1,2):
            if vBoardSize > vxPos + i >= 0 and vBoardSize > vyPos + j >= 0:
                if aBoard[vxPos + i][vyPos + j].isFlag:
                    vCounter += 1
    for i in range(-1, 2):
        for j in range(-1, 2):
            if vBoardSize > vxPos + i >= 0 and vBoardSize > vyPos + j >= 0 and vCounter == realself.bombsNear:
                self = aBoard[vxPos + i][vyPos + j]
                if (not self.isFlag):
                    self.isClicked = True
                    if self.bombsNear == 0:
                        self.Button.configure(image=pEmpty)
                        leftclickbutton(self)
                    elif self.bombsNear == 1:
                        self.Button.configure(image=pOne)
                        self.image = pOne
                    elif self.bombsNear == 2:
                        self.Button.configure(image=pTwo)
                        self.image = pTwo
                    elif self.bombsNear == 3:
                        self.Button.configure(image=pThree)
                        self.image = pThree
                    elif self.bombsNear == 4:
                        self.Button.configure(image=pFour)
                        self.image = pFour
                    elif self.bombsNear == 5:
                        self.Button.configure(image=pFive)
                        self.image = pFive
                    elif self.bombsNear == 6:
                        self.Button.configure(image=pSix)
                        self.image = pSix
                    elif self.bombsNear == 7:
                        self.Button.configure(image=pSeven)
                        self.image = pSeven
                    elif self.bombsNear == 8:
                        self.Button.configure(image=pEight)
                        self.image = pEight
                    if self.isBomb:
                        leftclickbomb(self)
                    if self.isBomb and self.isFlag:
                        self.Button.configure(image=pFlagBomb)
def resetboard():
    global aBoard
    global aBombs
    global dBombs
    global bOpenPlayer
    global vClicks
    global isStart
    isStart = False
    aBoard = []
    aBombs = []
    dBombs = {}
    vClicks = 0
    for i in range(0,len(aBoard)):
        for j in range(0,len(aBoard[i])):
            aBoard[i][j].Button.configure(state = "normal", image = pUnpressed)
    main.withdraw()
    wConfigure.deiconify()
    wLost.withdraw()
    wLost.grab_release()
    wWin.withdraw()
    bOpenPlayer.configure(state="normal")
def checkwin():
    global aBoard
    isRight = True
    for i in aBoard:
        for j in i:
            if j.isBomb == True and j.isFlag != True:
                isRight = False
    if isRight:
        won()
def setIsStop(event = None):
    global isStop
    isStop = True
def won():
    global main
    global wWin
    global lWon
    global tStartTime
    global aHighScores
    global vClicks
    global aData
    global vDifficulty
    global lHighScore
    global isRetry
    global bOpen
    isRetry = True
    main.withdraw()
    wWin.deiconify()
    tTime = time.time()-tStartTime
    lWon.configure(text = "You won! Time taken = " + str(round(tTime)))
    if vClicks < int(aHighScores[1]):
        aHighScores[1] = vClicks
    if tTime < int(aHighScores[0]):
        aHighScores[0] = tTime
    aData[vDifficulty] = str(aHighScores[0]) + "," + str(aHighScores[1]) + '\n'
    lHighScore.configure(text = "Least clicks: " + str(aHighScores[1]) + "\nLeast Time: " + str(round(aHighScores[0])))
    lHighScore.pack()
    bOpenPlayer.configure(state="normal")
    # print("Unready")
    w = open("HighScores.txt","w")
    # print(aData)
    w.writelines(aData)


# Binding exit full screen
# main.bind("<Escape>",exitfullscreen)
# Setting wSetPlayer:
lSetPlayer = Label(wSetPlayer, text="Enter player name:")
eSetPlayer = Entry(wSetPlayer)
bSetPlayer = Button(wSetPlayer, text="Finish", command=setplayer)
lSetPlayer.pack()
eSetPlayer.pack()
bSetPlayer.pack()

# Setting wLost:
bPlayLost = Button(wLost,text = "Play again!", command = resetboard)
lLost = Label(wLost,text = "welp: ")
lLost.pack()
bPlayLost.pack()
# Setting wWon:
lWon = Label(wWin,text = "You won!")
bPlayWon = Button(wWin,text = "Play again!", command = resetboard)
lWon.pack()
bPlayWon.pack()
# Setting wConfigure:
# Initializing Labels and setting Grab on wConfigure:
wConfigure.grab_set()
lChooseDiff = Label(wConfigure, text = "Choose difficulty: (Board Size, Number of bombs)")
# Setting the buttons to set difficulty:
# Beginner:
bDiffBeginner = Button(wConfigure,text = "Beginner (9x9, 40)")
bDiffBeginner.bind("<Button-1>", lambda event, diff=0: choosedifficulty(bDiffBeginner,diff,event,isRetry))
# Intermediate:
bDiffIntermediate = Button(wConfigure,text = "Intermediate (16x16, 40")
bDiffIntermediate.bind("<Button-1>", lambda event, diff=1: choosedifficulty(bDiffIntermediate,diff,event,isRetry))
# Expert:
bDiffExpert = Button(wConfigure, text = "Expert (24x24, 99)")
bDiffExpert.bind("<Button-1>", lambda event, diff=2: choosedifficulty(bDiffExpert,diff,event,isRetry))
# Packing the widgets to wConfigure:
lChooseDiff.pack()
bDiffBeginner.pack(side = LEFT)
bDiffIntermediate.pack(side = LEFT)
bDiffExpert.pack(side = LEFT)
# Setting main:
# setting Board:
fGame.pack(side = LEFT,expand = 1)
fInfo.pack(side = LEFT)
# print(aBombs)
# Setting fInfo:
lPlayer = Label(fInfo, text=sName)
bOpenPlayer = Button(fInfo, text="Set Name", command=openplayer)
lBuild = Label(fInfo, text="Build: " + str(vBuild), anchor=W)
lClicks = Label(fInfo, text="Clicks: " + str(vClicks), anchor=W)
lTimePassed = Label(fInfo, text="Time passed: " + str((time.time() - tStartTime)), anchor=W)
lFlagsLeft = Label(fInfo, text="flags left: 10", anchor=W)
lHighScore = Label(fInfo, text="", anchor=W, justify=LEFT)
bResize = Button(fInfo, text="Resize Board", anchor=W, command=resize)
lPlayer.pack(anchor=W)
bOpenPlayer.pack(anchor=W)
lBuild.pack(anchor=W)
lClicks.pack(anchor=W)
lTimePassed.pack(anchor=W)
lFlagsLeft.pack(anchor=W)
lHighScore.pack(anchor=W)
bResize.pack(anchor=W)
#Starting Autofire:
main.after(0,setIsStop())
main.after(0, setIsStop())
start_new_thread(update,(5,))
print(fInfo.winfo_width())
main.mainloop()
