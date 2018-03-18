import pandas as pd
import webcolors
import os


class team(object):
    name, school, side, color1, color2, alt1, alt2, player1, player2, player3, player4, player5 = ['']*12
    init = False
    def __init__(self):
        init = True

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
    wb = pd.read_excel('Team Colors.xlsx')

    num = len(wb.index)

    roster = ['']*5
    n = 0
    
    for k in range(0,num):
        if wb.iloc[k]['Team Name'] == name:
            roster[n] = wb.iloc[k]['Username']
            n = n + 1
    return(roster)
            
def setRoster(side, roster):

    for k in range(1,6):
        p = open('%sPlayer%d.txt' % (side, k),'w')
        p.write(roster[k-1])
        p.close
    

def writeHTML(side,color1,color2):
    s = ['<html>\n<head>\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<style>\n#secondary-color {\n  height: 100px;\n  width: 100px;\n  overflow: hidden;\n  background-color: ',
         '', ';\n}\n\n#triangle-topleft {\n  width: 0;\n  height: 0;\n  border-top: 100px solid ','',
         ';\n  border-right: 100px solid transparent;\n}\n\n</style>\n</head>\n<body>\n\t<div id="secondary-color">\n\t\t<div id="triangle-topleft"></div>\n\t</div>\n</body>\n</html> ']
    s[3] = color1
    s[1] = color2

    s1 = "".join(s)

    h = open('%sColors.html' % side,'w')
    h.write(s1)
    h.close()

def hexToRGB(color):
    r,g,b = webcolors.hex_to_rgb(color)
    return(r,g,b)
        
    

def newMatch():

    t1 = team()
    t2 = team()
    t1.side, t2.side = 'blue','orange'
    
    t1.school = input('Enter Home (blue team) School Name: ')
    t1.color1, t1.color2 = getColor(t1.school)
    t2.school = input('Enter Away (orange team) School Name: ')
    t2.color1, t2.color2 = getColor(t2.school)
    
    print("Home team: {0}\n\tHex Colors: {1}, {2}\n\tRGB colors: {3}, {4}" .format(t1.school,t1.color1,t1.color2,hexToRGB(t1.color1),hexToRGB(t1.color2)))
    print("Away team: {0}\n\tHex Colors: {1}, {2}\n\tRGB colors: {3}, {4}" .format(t2.school,t2.color1,t2.color2,hexToRGB(t2.color1),hexToRGB(t2.color2)))
    
    writeHTML(t1.side,t1.color1,t1.color2)
    writeHTML(t2.side,t2.color1,t2.color2)

    print('\nPress ENTER to exit')
    

newMatch()
input()
