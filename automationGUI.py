import pandas as pd
import webcolors
import os
from tkinter import *
from PIL import Image, ImageDraw, ImageTk

class team(object):

    name, school, scoreboard, side, color1, color2, alt1, alt2 = ['']*8
    roster = ['']*5

    init = False
    def __init__(self):
        init = True

    def createTeam(self,rosterFile,colorFile):
        self.name = input('Enter {0} side Team Name: '.format(self.side))
        self.school = input('Enter {0} side School Name: '.format(self.side))
        # self.school = getSchool(self.name)
        self.color1, self.color2 = getColor(self.school,colorFile)

        setScoreboard(self.side,changeScoreboard(self.side,self.name))

        print("{5} team: {0}\n\tHex Colors: {1}, {2}\n\tRGB colors: {3}, {4}\n" .format(self.school,self.color1,self.color2,hexToRGB(self.color1),hexToRGB(self.color2),self.side))

        self.roster = getRoster(self.name,rosterFile)

        self.roster = changeRoster(self.name,self.roster)

        setRoster(self.side,self.roster)

        print('Generating HTML Files...')
        createHTML(self.side,self.color1,self.color2)
        print('HTML files generated\n')

        print('Generating PNG files...')
        createPNG(self.side,self.color1,self.color2)
        print('PNG files generated\n')

class dataFile(object):
    name, extension = '',''
    column = ['']*3

    init = False
    def __init__(self):
        init = True

    def loadFile(self,name):
        self.name = name
        # print('\n')
        if self.name.endswith('.csv'):
            self.df = pd.read_csv(self.name)
        else:
            self.df = pd.read_excel(self.name)
class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        # self.init_window()

    def init_window(self):

        self.master.title('CCA Scoreboard')

        # self.pack(fill=BOTH, expand = 1)

        Label(text = 'Roster File name (include the .csv or .xlsx)').grid(row = 0, column = 1)
        rosterFile = Entry(master=None).grid(row = 0, column = 2, columnspan = 2)

        Label(text = 'Team Colors File name (include the .csv or .xlsx)').grid(row = 1, column = 1)
        colorFile = Entry(master=None).grid(row = 1, column = 2)

        Label(text = 'Blue team').grid(row = 2, column = 1)

        rosterList = getRosterList(Entry.get(rosterFile))

        selectedBlue = StringVar()
        selectedBlue.set(rosterList[0])

        rosterChoice = OptionMenu(root, selectedBlue, *rosterList).grid(row = 3,column = 1)

def getColor(name,wb):

    # wb = pd.read_excel(colorFilename)

    num = len(wb.index)

    color1 = ''
    color2 = ''

    for k in range(0,num):
        if wb.iloc[k]['School'] == name:
            color1 = wb.iloc[k]['Color 1']
            color2 = wb.iloc[k]['Color 2']
    if color1 == '':
        print('School not found\nEnter hex codes of school (# included)')
        color1 = input('Color 1: ')
        color2 = input('Color 2: ')


    return(color1, color2)

def getRoster(name,wb):

    # wb = pd.read_csv(rosterFilename)

    num = len(wb.index)

    roster = ['']*5
    n = 0

    for k in range(0,num):
        if wb.iloc[k]['Team Name'] == name:
            roster[n] = wb.iloc[k]['Username']
            n = n + 1
    return(roster)

def getRosterList(wb):
    teams = sorted(list(set(wb['Team Name'].tolist())),key=str.lower)
    return (teams)

# def getSchool(name): #Can't be implemented because data from AVGL does not include College name :(
#     wb = pd.read_excel('RL_registered_players_March19.xlsx')
#
#     num = len(wb.index)
#
#     school = ''
#
#     for k in range(0,num):
#         if wb.iloc[k]['Team Name'] == name:
#             school = wb.iloc[k]['College']
#
#     if school == '':
#         school = input('School not found, enter school name manually: ')
#
#     return(school)

def changeScoreboard(side,name):
    c = 'n'
    while c == 'n':
        c = input('{0} team name is: {1}. Should this be the scoreboard name? (y,n): '.format(side,name))
        if c =='n':
            name = input('Enter new name for {0}: '.format(name))
    return(name)

def setScoreboard(side,name):
    s = open('%sName.txt' % side,'w')
    s.write(name)
    s.close

def changePlayer(roster):
    playerNum = int(input('Enter number of player you wish to edit: ')) - 1
    roster[playerNum] = input('Enter new name for {0}: '.format(roster[playerNum]))
    print('\n')

    return(roster)

def changeRoster(name,roster):
    choice = 'y'
    while choice == 'y':
        printRoster(name,roster)
        choice = input('Change player name? (y/n): ')
        if choice == 'y':
            roster = changePlayer(roster)
    return(roster)

def setRoster(side, roster):

    for k in range(1,6):
        p = open('%sPlayer%d.txt' % (side, k),'w')
        p.write(roster[k-1])
        p.close

def createHTML(side,color1,color2):
    s = ['<html>\n<head>\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<style>\n#secondary-color {\n  height: 100px;\n  width: 100px;\n  overflow: hidden;\n  background-color: ',
         '', ';\n}\n\n#triangle-topleft {\n  width: 0;\n  height: 0;\n  border-top: 100px solid ','',
         ';\n  border-right: 100px solid transparent;\n}\n\n</style>\n</head>\n<body>\n\t<div id="secondary-color">\n\t\t<div id="triangle-topleft"></div>\n\t</div>\n</body>\n</html> ']
    s[3] = color1
    s[1] = color2

    s1 = "".join(s)

    h = open('%sColors.html' % side,'w')
    h.write(s1)
    h.close()

def createPNG(side,color1,color2):
    img = Image.new('RGB',(200,200))
    draw = ImageDraw.Draw(img)
    draw.polygon([(0,0),(0,200),(200,200),(200,0)], fill = hexToRGB(color2))
    draw.polygon([(0,0),(0,199),(199,0)], fill = hexToRGB(color1))
    img.save('%sColors.png' % side)

def hexToRGB(color):
    r,g,b = webcolors.hex_to_rgb(color)
    return(r,g,b)

def newMatch():

    t1 = team()
    t2 = team()
    t1.side, t2.side = 'Blue','Orange'

    t1.createTeam(roster.df,colors.df)
    t2.createTeam(roster.df,colors.df)

# rosterFilename = input('Enter name of roster file (e.g. RL_registered_players_March19.csv): ')
# colorFilename = input('Enter name of team color file (e.g. Team Colors.xlsx): ')
# colorFilename = 'Team Colors.xlsx'
#
# print('----------------COLLEGE CARBALL ASSOCIATION----------------\n')
#
# print('Load Roster File')
# roster = dataFile()
# roster.loadFile()
#
# print('Load Team Colors File')
# colors = dataFile()
# colors.loadFile()
#
# cont = 'y'
# while cont == 'y':
#     newMatch()
#     cont = input('Run another match? (y/n): ')
#
#
# print('\nPress ENTER to exit')
# input()

roster, color = '',''

root = Tk()


Label(text = 'Roster File name (include the .csv or .xlsx)').grid(row = 0, column = 1)
rosterFile = Entry(master=None).grid(row = 0, column = 2, columnspan = 2)

Label(text = 'Team Colors File name (include the .csv or .xlsx)').grid(row = 1, column = 1)
colorFile = Entry(master=None).grid(row = 1, column = 2)
def close_window():
    roster = Entry.get(rosterFile)
    color = Entry.get(colorFile)
    root.destroy()
quitButton = Button(root, text="Submit",command=close_window).grid(row = 2, column = 1)

root.mainloop()

Label(text = roster).grid(row = 0, column = 0)

root1 = Tk()

Label

root1.mainloop()
