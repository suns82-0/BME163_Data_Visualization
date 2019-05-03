#!/usr/bin/env python3

'''
This program draws a swarm plot.

Author: Xing Sun
'''

import matplotlib.pyplot as plt
import matplotlib.patches as mplpatches
import numpy as np
import sys,random,math


plt.style.use('BME163.mplstyle')

coverDict = {}
sampleDict = {}
qualityScoresDict = {}
colorDict = {}


def print_dict(temp):
    for key in sorted(temp.keys()):
        print("%s : %s" % (key, temp[key]))

try:
    with open("BME163_Input_Data_3.txt") as inFile:
        for line in inFile.readlines():
            try:
                l = line.split()
                if int(l[0].split('_')[3]) <= 10:
                    subCov = l[0].split('_')[3]
                else:
                    subCov = '11'
                qualScore = float(l[0].split('_')[1])
                perId = float(l[1])
                try:
                    coverDict[subCov].append((perId, qualScore))
                except KeyError:
                    coverDict[subCov] = [(perId, qualScore)]
            except ValueError:
                continue
except FileNotFoundError:
    print("No input file supplied.")
    sys.exit(1)

def custom_swarm(panel, y_vals, x_position, panelWidth=None, panelHeight=None, xMin=None, xMax=None, \
                yMin=None, yMax=None, binSize=1, pointSize=None, shift=None, markerSize = .5, \
                color=None, figHeight=None, figWidth=None):


    finalX = np.zeros(len(y_vals))
    finalY = np.zeros(len(y_vals))
    sortedYVals = y_vals
    if isinstance(color, str):
        finalColors = color
    else:
        finalColors = color
    xRange = xMax - xMin
    yRange = yMax - yMin

    def findDistance(xlist, ylist, newPoint, minDistance, yRange, xRange, \
                    panelHeightInches, panelWidthInches):
        for x,y in zip(xlist,ylist):
            a = (abs(newPoint[0]-x)/xRange)*(panelWidthInches)
            b = (abs(newPoint[1]-y)/yRange)*(panelHeightInches)
            c = math.sqrt((a**2)+(b**2))
            if c <= minDistance:
                return False
        return True

    minimumXDistance = ((markerSize/2)/xRange)/(panelWidth*figWidth)+.002
    minimumYDistance = ((2*markerSize)/yRange)/(panelHeight*figWidth)
    minDistance = math.sqrt((minimumXDistance**2)+(minimumYDistance**2))

    left = True
    for index in range(len(sortedYVals)):
        val = sortedYVals[index]
        if index  == 0:
            finalX[index] = x_position
            finalY[index] = val
            if not isinstance(color,str):
                finalColors[index] = color[index]
        else:
            prevYVals = finalY[:index]
            prevXVals = finalX[:index]
            overlappingY = (((val-prevYVals)/yRange)*(panelHeight*figHeight)) <= minimumYDistance
            if not np.any(overlappingY):
                finalX[index] = x_position
                finalY[index] = val
                if not isinstance(color,str):
                    finalColors[index] = color[index]
            else:
                overlapY = prevYVals[overlappingY]
                overlapX = prevXVals[overlappingY]
                for pix in np.arange(0,binSize/2,.001):
                    newX = x_position+pix if not left else x_position-pix
                    newPoint = (newX, val)
                    if findDistance(overlapX, overlapY, newPoint, minDistance, \
                        yRange, xRange, panelHeight*figHeight, panelWidth*figWidth):
                        finalX[index] = newX
                        finalY[index] = val
                        if not isinstance(color,str):
                            finalColors[index] = color[index]
                        left = not left
                        break
    panel.scatter(finalX, finalY, s=markerSize, color=finalColors,\
                marker='o', linewidth=0, alpha=1)


for key in coverDict:
    indices = np.random.choice(len(coverDict[key]),1000)
    randSamples = np.array(coverDict[key])[indices]
    samples, qualityScores = zip(*randSamples)
    sampleDict[key] = np.array(samples)
    qualityScoresDict[key] = np.array(qualityScores)


colorRange = np.linspace(0,.7,8)
colors = [(1-i, 1-i, i) for i in colorRange]
for key in qualityScoresDict:
    rgbList = np.zeros(len(qualityScoresDict[key]), dtype=(float,3))
    for i in np.arange(0,8):
        mask = (qualityScoresDict[key] < i+8) & (qualityScoresDict[key] >= i+8-1)
        rgbList[mask] = colors[i]
    colorDict[key] = rgbList
    assert(len(colorDict[key]) == len(qualityScoresDict[key]))
    assert(len(colorDict[key]) == len(sampleDict[key]))


medians = {key : np.median(sampleDict[key]) for key in sampleDict}


figHeight = 3
figWidth = 7

plt.figure(figsize=(figWidth, figHeight),dpi=600)


mainWidth = 5/figWidth
mainHeight = 2/figHeight
secondPanelHeight = mainHeight
secondPanelWidth = 0.2/figWidth

mainPanel = plt.axes([0.1,0.2,mainWidth,mainHeight])
secondPanel = plt.axes([0.9, 0.2, secondPanelWidth, secondPanelHeight])

# print median lines for each coverage bin
for key in medians:
    mid = int(key)
    width = 0.35
    bottom = medians[key]
    mainPanel.plot([mid-width,mid+width],[bottom,bottom],lw=1, color='red',zorder=1)

# set dashed 95% line
mainPanel.plot([0,12],[95,95], lw=0.5, ls='--', color='black')

# plot color rectangles
for color in colors:
    patch = mplpatches.Rectangle((0, colors.index(color)+7), 1, 1, linewidth=0, facecolor=color)
    secondPanel.add_patch(patch)

yMin = np.min([np.min(sampleDict[key]) for key in sampleDict])
yMax = np.max([np.max(sampleDict[key]) for key in sampleDict])
xMax = np.max([np.max(int(key)) for key in sampleDict])
xMin = np.min([np.min(int(key)) for key in sampleDict])

for key in sampleDict:
    xvals = [int(key)]*len(sampleDict[key])
    y_vals, color = (list(x) for x in zip(*sorted(zip(sampleDict[key], colorDict[key]), key = lambda pair:pair[0])))
    custom_swarm(mainPanel, y_vals, int(key), color=color, markerSize=.5, binSize=0.7, \
            yMax=yMax, yMin=yMin, xMin=xMin, xMax=xMax, panelWidth=mainWidth, \
            panelHeight=mainHeight, figWidth=figWidth, figHeight=figHeight) 

mainPanel.tick_params(axis='both', which='both',\
                   bottom='on', labelbottom='on',\
                   left='on', labelleft='on',\
                   right='off', labelright='off',\
                   top='off', labeltop='off',\
                   labelsize=8)

secondPanel.tick_params(axis='both', which='both',\
                   bottom='off', labelbottom='off',\
                   left='on', labelleft='on',\
                   right='off', labelright='off',\
                   top='off', labeltop='off',\
                   labelsize=8)

ticks = [x for x in range(1,11)]
ticks.append('>10') 
mainPanel.set_xlim(0.5,11.5)
mainPanel.set_ylim(75,100)
secondPanel.set_ylim(7,15)
mainPanel.set_xticks(np.arange(1,12))
secondPanel.set_yticks(np.arange(7,16))
mainPanel.set_xticklabels(ticks)
mainPanel.set_yticks(np.arange(75,101,5))
mainPanel.set_ylabel('Identity (%)')
mainPanel.set_xlabel('Subread coverage')
secondPanel.set_ylabel('Read quality (Q)')

plt.savefig('Sun_Xing_BME163_Assignment_Week4.withcolor2.png',dpi=600)
