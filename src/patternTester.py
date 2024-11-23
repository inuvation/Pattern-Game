from cmu_graphics import *
from modules.patterns import findPattern, loadPatternChanges, PATTERNS
from modules.utilities import getCommaSeperatedStringFromList

def onMousePress(app, x, y):
    app.mousePoints = []

def onMouseRelease(app, x, y):
    if len(app.mousePoints) > 1:
        app.lastPattern = findPattern(app.patterns, app.mousePoints, app.patternChanges)

def onMouseDrag(app, x, y):
    app.mousePoints.append((x, app.height - y))

def redrawAll(app):
    drawLabel(f'Draw a {app.commaSeperatedPatterns}', app.width/2, 25, size=20)

    if app.lastPattern != None:
        drawLabel(f'You have drawn a: {app.lastPattern}', app.width/2, 50, size=20, bold=True)

    if len(app.mousePoints) > 0:
        lastPointX = lastPointY = None

        for (x, y) in app.mousePoints:
            y = app.height - y

            if lastPointX != None and lastPointY != None:
                drawLine(x, y, lastPointX, lastPointY)
            lastPointX, lastPointY = x, y

def onAppStart(app):
    app.commaSeperatedPatterns = getCommaSeperatedStringFromList(PATTERNS)
    app.lastPattern = None
    app.patternChanges = loadPatternChanges(PATTERNS)
    
    print(f'loading shapes with pattern changes:', app.patternChanges)

    app.mousePoints = []

def main():
    app = runApp(width=640, height=360)

if __name__ == '__main__':
   main()