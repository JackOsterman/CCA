import pandas as pd
import webcolors
import os
from PIL import Image, ImageDraw


class team(object):

    name, school, scoreboard, side, color1, color2, alt1, alt2 = ['']*8
    roster = ['']*5

    init = False
    def __init__(self):
        init = True

    def createTeam(self):
        self.name = input('Enter {0} side Team Name: '.format(self.side))
        self.school = getSchool(self.name)
        self.color1, self.color2 = getColor(self.school)
        print("{5} team: {0}\n\tHex Colors: {1}, {2}\n\tRGB colors: {3}, {4}" .format(self.school,self.color1,self.color2,hexToRGB(self.color1),hexToRGB(self.color2),self.side))

        self.roster = getRoster(self.name)

        self.roster = changeRoster(self.name,self.roster)

        setRoster(self.side,self.roster)

        print('Generating HTML Files...')
        createHTML(self.side,self.color1,self.color2)
        print('HTML files generated\n')

        print('Generating PNG files...')
        createPNG(self.side,self.color1,self.color2)
        print('PNG files generated\n')



def getColor(name):

    wb = pd.read_excel('Team Colors.xlsx')

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

def getRoster(name):
    wb = pd.read_excel('roster test.xlsx')

    num = len(wb.index)

    roster = ['']*5
    n = 0

    for k in range(0,num):
        if wb.iloc[k]['Team name'] == name:
            roster[n] = wb.iloc[k]['Username']
            n = n + 1
    return(roster)

def getSchool(name):
    wb = pd.read_excel('roster test.xlsx')

    num = len(wb.index)

    school = ''

    for k in range(0,num):
        if wb.iloc[k]['Team name'] == name:
            school = wb.iloc[k]['College']

    return(school)

def printRoster(name, roster):
    # print('{0} roster:\n{1}'.format(name,roster))
    for k in range(0,5):
        print('[{0}] {1}'.format(k,roster[k]))

def changePlayer(roster):
    playerNum = int(input('Enter number of player you wish to edit: '))
    roster[playerNum] = input('Enter new name for {0}: '.format(roster[playerNum]))

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
    t1.side, t2.side = 'blue','orange'

    t1.createTeam()
    t2.createTeam()

    # t1.name = input('Enter Home (blue team) Team Name: ')
    # t1.school = getSchool(t1.name)
    # t1.color1, t1.color2 = getColor(t1.school)
    #
    # t2.name = input('Enter Away (orange team) Team Name: ')
    # t2.school = getSchool(t2.name)
    # t2.color1, t2.color2 = getColor(t2.school)
    #
    # print("Home team: {0}\n\tHex Colors: {1}, {2}\n\tRGB colors: {3}, {4}" .format(t1.school,t1.color1,t1.color2,hexToRGB(t1.color1),hexToRGB(t1.color2)))
    # print("Away team: {0}\n\tHex Colors: {1}, {2}\n\tRGB colors: {3}, {4}\n" .format(t2.school,t2.color1,t2.color2,hexToRGB(t2.color1),hexToRGB(t2.color2)))
    #
    # t1.roster = getRoster(t1.name)
    #
    # t1.roster = changeRoster(t1.name,t1.roster)
    #
    # setRoster(t1.side,t1.roster)
    #
    # print('Generating HTML Files...')
    # createHTML(t1.side,t1.color1,t1.color2)
    # createHTML(t2.side,t2.color1,t2.color2)
    # print('HTML files generated\n')
    #
    # print('Generating PNG files...')
    # createPNG(t1.side,t1.color1,t1.color2)
    # createPNG(t2.side,t2.color1,t2.color2)
    # print('PNG files generated\n')

    print('\nPress ENTER to exit')


newMatch()
input()
