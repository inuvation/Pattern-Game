# Citations
# https://www.youtube.com/watch?v=ERKDHZyZDwA (Dynamic time warping 1: Motivation)
# https://www.youtube.com/watch?v=9GdbMc4CEhE (Dynamic time warping 2: Algorithm)

from cmu_graphics import *
from patterns import loadPatterns
import math

def dynamicTimeWarpCost(pattern1, pattern2):
    len1, len2 = len(pattern1) + 1, len(pattern2) + 1

    costMatrix = createMatrix(len1, len2)

    # 0,0 starts as 0, where all other elements in the first row and column are infinity 
    for i in range(len1): 
        costMatrix[i][0] = math.inf

    for j in range(len2): 
        costMatrix[0][j] = math.inf

    costMatrix[0][0] = 0

    for i in range(1, len1):
        for j in range(1, len2):
            pass

    return costMatrix

            
def createMatrix(rows, cols):
    return [([None] * cols) for row in range(rows)]

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
            drawLabel(app.costMatrix[i][j], rectX + boxW/2, rectY + boxH/2)

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
    app.padding = 8

    app.pattern1 = app.patterns['test1']
    app.pattern2 = app.patterns['test2']

    app.costMatrix = dynamicTimeWarpCost(app.pattern1, app.pattern2)

def main():
    app = runApp(width=768, height=768)

main()