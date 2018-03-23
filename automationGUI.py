import pandas as pd
import webcolors
import os
# import tkinter
from appJar import gui
from PIL import Image, ImageDraw, ImageTk

class team(object):

    name, school, scoreboard, side, color1, color2, alt1, alt2,col = ['']*9
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
    name, extension, df = '','',''
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


def getColor(name,wb):

    # wb = pd.read_excel(colorFilename)
    color1 = ''
    color2 = ''

    if app.getEntry('colorFile') != '':
        num = len(wb.index)



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
    r = ['']*5
    if app.getEntry('rosterFile') != '':
        num = len(wb.index)

        n = 0

        for k in range(0,num):
            if wb.iloc[k]['Team Name'] == name:
                r[n] = wb.iloc[k]['Username']
                n = n + 1
    return(r)

def getRosterList(wb):
    teams = sorted(list(set(wb['Team Name'].tolist())),key=str.lower)
    return (teams)

def getSchoolList(wb):
    teams = sorted(list(set(wb['School'].tolist())),key=str.lower)
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

app = gui()
app.setTitle('CCA Automation')

rosterFile,colorFile, rosterPrev, colorPrev, teamPrevB, schoolPrevB, teamPrevO, schoolPrevO = ['']*8
roster = dataFile()
color = dataFile()
t1 = team()
t2 = team()
t1.side, t2.side = 'Blue','Orange'
t1.col, t2.col = 1,3


app.addLabel('rosterFileLabel','Open Roster File',0,1)
app.addFileEntry('rosterFile',0,2)
app.addLabel('colorFileLabel','Open Color File',1,1)
app.addFileEntry('colorFile',1,2)

app.addLabel('b','Blue',3,1)
app.addLabel('rosterOption','Select Team',4,2)
app.addOptionBox('teamsB',[''],4,1)
app.addLabel('schoolOption','Select School',5,2)
app.addOptionBox('schoolsB',[''],5,1)

app.addLabel('scoreboard','Scoreboard Name',6,2)
app.addEntry('scoreboardB',6,1)
app.addEntry('scoreboardO',6,3)

app.addLabel('players','Players',10,2)

app.addEntry('p1B',8,1)
app.addEntry('p2B',9,1)
app.addEntry('p3B',10,1)
app.addEntry('p4B',11,1)
app.addEntry('p5B',12,1)

app.addLabel('o','Orange',3,3)
app.addOptionBox('teamsO',[''],4,3)
app.addOptionBox('schoolsO',[''],5,3)

app.addEntry('p1O',8,3)
app.addEntry('p2O',9,3)
app.addEntry('p3O',10,3)
app.addEntry('p4O',11,3)
app.addEntry('p5O',12,3)

app.addHorizontalSeparator(7,1,3,colour=None)
app.addHorizontalSeparator(13,1,3,colour=None)

app.addEntry('color1B',14,1)
app.addLabel('color1Brgb','',15,1)
app.addEntry('color2B',16,1)
app.addLabel('color2Brgb','',17,1)

app.addEntry('color1O',14,3)
app.addLabel('color1Orgb','',15,3)
app.addEntry('color2O',16,3)
app.addLabel('color2Orgb','',17,3)

app.addLabel('c1','Color 1',14,2)
app.addLabel('c2','Color 2',16,2)
app.addLabel('preview','Preview',18,2)

# bluePrev = app.addCanvas('bluePrev')
# bluePrev.create_rectangle(50,50,fill = hexToRGB(app.getEntry('color1B')))

def Update():
    global rosterPrev
    global colorPrev
    global teamPrevB
    global teamPrevO
    global schoolPrevB
    global schoolPrevO

    if app.getEntry('rosterFile') != rosterPrev:
        updateTeams()
        rosterPrev = app.getEntry('rosterFile')
    if app.getEntry('colorFile') != colorPrev:
        updateSchools()
        colorPrev = app.getEntry('colorFile')

    if app.getOptionBox('teamsB') != teamPrevB:
        updateRosterB()
        teamPrevB = app.getOptionBox('teamsB')
    if app.getOptionBox('schoolsB') != schoolPrevB:
        updateColorB()
        schoolPrevB = app.getOptionBox('schoolsB')

    if app.getOptionBox('teamsO') != teamPrevO:
        updateRosterO()
        teamPrevO = app.getOptionBox('teamsO')
    if app.getOptionBox('schoolsO') != schoolPrevO:
        updateColorO()
        schoolPrevO = app.getOptionBox('schoolsO')


def updateTeams():
    roster.loadFile(app.getEntry('rosterFile'))
    app.changeOptionBox('teamsB',getRosterList(roster.df))
    app.changeOptionBox('teamsO',getRosterList(roster.df))

def updateSchools():
    color.loadFile(app.getEntry('colorFile'))
    app.changeOptionBox('schoolsB',getSchoolList(color.df))
    app.changeOptionBox('schoolsO',getSchoolList(color.df))

def updateRosterB():
    roster_= getRoster(app.getOptionBox('teamsB'),roster.df)

    app.setEntry('p1B',roster_[0])
    app.setEntry('p2B',roster_[1])
    app.setEntry('p3B',roster_[2])
    app.setEntry('p4B',roster_[3])
    app.setEntry('p5B',roster_[4])


    app.setEntry('scoreboardB',app.getOptionBox('teamsB'))

def updateColorB():
    color_= getColor(app.getOptionBox('schoolsB'),color.df)

    app.setEntry('color1B',color_[0])
    app.setEntry('color2B',color_[1])



def updateRosterO():
    roster_= getRoster(app.getOptionBox('teamsO'),roster.df)

    app.setEntry('p1O',roster_[0])
    app.setEntry('p2O',roster_[1])
    app.setEntry('p3O',roster_[2])
    app.setEntry('p4O',roster_[3])
    app.setEntry('p5O',roster_[4])

    app.setEntry('scoreboardO',app.getOptionBox('teamsO'))

def updateColorO():
    color_= getColor(app.getOptionBox('schoolsO'),color.df)

    app.setEntry('color1O',color_[0])
    app.setEntry('color2O',color_[1])

def getRosterB():
    roster = ['']*5
    roster[0]=app.getEntry('p1B')
    roster[1]=app.getEntry('p2B')
    roster[2]=app.getEntry('p3B')
    roster[3]=app.getEntry('p4B')
    roster[4]=app.getEntry('p5B')
    return(roster)

def getRosterO():
    roster = ['']*5
    roster[0]=app.getEntry('p1O')
    roster[1]=app.getEntry('p2O')
    roster[2]=app.getEntry('p3O')
    roster[3]=app.getEntry('p4O')
    roster[4]=app.getEntry('p5O')
    return(roster)


def Apply():
    setScoreboard(t1.side,app.getEntry('scoreboardB'))
    setScoreboard(t2.side,app.getEntry('scoreboardO'))

    setRoster('Blue',getRosterB())
    setRoster('Orange',getRosterO())

    createPNG('Blue',app.getEntry('color1B'),app.getEntry('color2B'))
    createPNG('Orange',app.getEntry('color1O'),app.getEntry('color2O'))

    app.setLabel('color1Brgb',hexToRGB(app.getEntry('color1B')))
    app.setLabel('color2Brgb',hexToRGB(app.getEntry('color2B')))
    app.setLabel('color1Orgb',hexToRGB(app.getEntry('color1O')))
    app.setLabel('color2Orgb',hexToRGB(app.getEntry('color2O')))

app.addButton('Apply',Apply,19,2)

app.registerEvent(Update)

app.go()
