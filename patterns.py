from cmu_graphics import *

# CONFIGURATION

def loadPatterns():
    return {
        'verticalLine': [
            (0.5, 0),
            (0.5, 1)
        ],
        'horizontalLine': [
            (0, 0.5),
            (1, 0.5)
        ],
        'test1': [
            (0, 0.5),
            (1, 0.25),
            (2, 0.5),
            (3, 0.85)
        ],
        'test2': [
            (0, 0.6),
            (1, 0.25),
            (2, 0.4),
            (3, 0.75),
            (4, 0.85)
        ],
    }

# UTILITIES

def findPattern(app, mouseSegments):
    for pattern in app.patterns:
        squaredDistance = 0

# CMU GRAPHICS

def onAppStart(app):
    app.patternError = 15 # Degree to which a player drawn shape can vary from the configured pattern
    app.patterns = loadPatterns()


def onMousePress(app, x, y):
    app.mouseSegments = []

def onMouseRelease(app, x, y):
    if len(app.mouseSegments) > 1:
        pattern = findPattern(app, app.mouseSegments)

        print(pattern)

def onMouseDrag(app, x, y):
    app.mouseSegments.append((x, y))


def main():
    app = runApp(width=640, height=360)

# main()