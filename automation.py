import pandas as pd
from html.parser import HTMLParser


class team(object):
    name, school, color1, color2, alt1, alt2, player1, player2, player3, player4, player5 = ['']*11
    init = False
    def __init__(self):
        init = True

def teamColor(name):

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

def newMatch():

    t1 = team()
    t2 = team()
    t1.school = input('Enter Home (blue team) School Name: ')
    t2.school = input('Enter Away (orange team) School Name: ')
    t1.color1, t1.color2 = teamColor(t1.school)
    t2.color1, t2.color2 = teamColor(t2.school)
    print("Home team: {0}\n\tColors: {1}, {2}" .format(t1.school,t1.color1,t1.color2))
    print("Away team: {0}\n\tColors: {1}, {2}" .format(t2.school,t2.color1,t2.color2))
    
##parser = MyHTMLParser()
##parser.feed('team1.html')

##newMatch()
