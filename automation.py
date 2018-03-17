import pandas as pd

##class teamColors(object):
##    def __init__(self, name, color1, color2, alt):
##        self.name = name
##        self.color1 = color1
##        self.color2 = color2
##        self.alt = alt
##
##    def __str__(self):
##        return("Team colors: \n"
##               "Name: {0}\n"
##               "Color 1: {1}\n"
##               "Color 2: {2}\n"
##               .format(self.name, self.color1, self.color2))
           

wb = pd.read_excel('Team Colors.xlsx')

num = len(wb.index)

name = input('Enter School Name: ')

color_1 = ''
color_2 = ''

for k in range(0,num):
    if wb.iloc[k]['School'] == name:
        color_1 = wb.iloc[k]['Color 1']
        color_2 = wb.iloc[k]['Color 2']
if color_1 == '':    
    print('School not found\nEnter hex codes of school (# included)')
    color_1 = input('Color 1: ')
    color_2 = input('Color 2: ')

print(color_1)
print(color_2)

