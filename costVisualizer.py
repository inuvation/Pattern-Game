from cmu_graphics import *
from utilities import dynamicTimeWarpCost
from configuration import loadPatterns

import math

def drawGraph(app, pattern, x, y, w, h, horizontal=True):
    drawRect(x, y, w, h, fill='white', border='black')

    graphLen = len(pattern) + 1

    lastPointX, lastPointY = None, None

    for (dotX, dotY) in pattern:
        dotX += 1 # A dynamic time warp matrix adds 1 to each dimension of the sequence

        if horizontal:
            horizontalX, horizontalY = dotX*(w/graphLen) + (w/graphLen)/2, (1 - dotY)*h
        else:
            horizontalX, horizontalY = dotY*w, h - (dotX*(h/graphLen) + (h/graphLen)/2)

        screenX, screenY = x + horizontalX, y + horizontalY
        if lastPointX != None and lastPointY != None:
            drawLine(screenX, screenY, lastPointX, lastPointY)
        lastPointX, lastPointY = screenX, screenY

        drawCircle(screenX, screenY, app.padding)
        drawLabel(f'({dotX}, {dotY})', screenX, screenY + app.padding*2)

def drawGrid(app, x, y, w, h):
    drawRect(x, y, w, h, fill='white', border='black')

    len1 = len(app.pattern1) + 1
    len2 = len(app.pattern2) + 1
    boxW = w / len1
    boxH = h / len2

    for i in range(0, len1): # Column
        for j in range(0, len2): # Row
            rectX, rectY = x + i*boxW, y + (h - (j + 1)*boxH)
            # Border
            drawRect(rectX, rectY, boxW, boxH, fill='white', border='black')
            
            # Cell Row, Column
            drawLabel(f'{j}, {i}', rectX + app.padding, rectY + app.padding, align='left-top')

            # Cell Cost
            value = app.costMatrix[i][j]
            if app.costMatrix[i][j] == math.inf:
                label = 'infinity'
            else:
                label = rounded(value*100) / 100
            drawLabel(label, rectX + boxW/2, rectY + boxH/2)

def redrawAll(app):
    # Vertical Graph
    verticalGraphX, verticalGraphY = app.margin, app.margin
    graphW = (app.width - app.margin*3)/3
    graphH = (app.height - graphW - app.margin*3)
    drawGraph(app, app.pattern2, verticalGraphX, verticalGraphY, graphW, graphH, False)  

    # Grid
    gridW, gridH = graphW*2, graphH
    gridX = app.width - gridW - app.margin
    drawGrid(app, gridX, verticalGraphY, gridW, gridH)

    # Horizontal Graph
    verticalGraphY = verticalGraphY + gridH + app.margin
    drawGraph(app, app.pattern1, gridX, verticalGraphY, gridW, graphW, True) 

def onAppStart(app):
    app.patterns = loadPatterns()
    app.margin = 16
    app.padding = 16

    app.pattern1 = app.patterns['land']
    app.pattern2 = app.patterns['lor']

    app.costMatrix = dynamicTimeWarpCost(app.pattern1, app.pattern2)

def main():
    app = runApp(width=768, height=768)

if __name__ == '__main__':
   main()