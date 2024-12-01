import math

from modules.utilities import *
from modules.configuration import CONFIGURATION
from cmu_graphics import *

PATTERNS = {
    'verticalLine': [
        (0, 0),
        (0, 1)
    ],
    'horizontalLine': [
        (0, 0),
        (1, 0)
    ],
    'square': [
        (0, 0),
        (1, 0),
        (1, 1),
        (0, 1),
        (0, 0)
    ],
    'triangle': [
        (0, 0),
        (1, 0),
        (0.5, 1),
        (0, 0)
    ],
    'lightning': [
        (0, 0),
        (1, 0.5),
        (0, 0.5),
        (1, 1)
    ],
    'land': [
        (0, 0),
        (0.5, 1),
        (1, 0)
    ],
    'lor': [
        (0, 1),
        (0.5, 0),
        (1, 1)
    ],
    'heart': [
        (0, 3/4),
        (1/4, 1),
        (1/2, 3/4),
        (3/4, 1),
        (1, 3/4),
        (1/2, 0),
        (0, 3/4)
    ],
}

# Dynamic Time Warp Utilities

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
            match = costMatrix[i - 1][j - 1]
            insertion = costMatrix[i - 1][j]
            deletion = costMatrix[i][j - 1]

            costMatrix[i][j] = distance(*pattern1[i - 1], *pattern2[j - 1]) + min(match, insertion, deletion)

    return costMatrix

def getCost(normalPattern1, normalPattern2):
    costMatrix = dynamicTimeWarpCost(normalPattern1, normalPattern2)
    topRow, topCol = len(costMatrix) - 1, len(costMatrix[0]) - 1
    cost = costMatrix[topRow][topCol]

    return cost

def findPattern(listOfPatterns, patternToCheck, directionChangesToCompare=None):
    lowestCost, closestShape = None, None

    normalizedPatternToCheck = normalize(patternToCheck)
    patternToCheckDirectionChanges = getDirectionalChanges(normalizedPatternToCheck)

    if directionChangesToCompare == None:
        directionChangesToCompare = loadPatternChanges(listOfPatterns)

    for patternName in listOfPatterns:
        directionChanges = directionChangesToCompare[patternName]
        if patternToCheckDirectionChanges < directionChanges: 
            # print(f'Skipped {patternName} for checked pattern having less directions')
            
            continue

        pattern = listOfPatterns[patternName]
        fowardCost = getCost(normalizedPatternToCheck, pattern)
        backwardCost = getCost(normalizedPatternToCheck, list(reversed(pattern)))
        cost = min(fowardCost, backwardCost)
        if lowestCost == None or cost < lowestCost:
            lowestCost, closestShape = cost, patternName

    # print(f'user drawn shape has {directionChanges}, {closestShape} has {}')

    return closestShape

def getDirectionalChanges(pattern, tolerance=None):
    if tolerance == None:
        tolerance = CONFIGURATION['deltaSegmentTolerance']

    directionalChanges = 0
    segmentsInLastChange = 0

    lastPoint = None
    lastDeltaX = lastDeltaY = None

    for point in pattern:
        if lastPoint != None:
            deltaX = point[0] - lastPoint[0]
            deltaY = point[1] - lastPoint[1]

            if lastDeltaX != None:
                if sign(deltaX) == sign(lastDeltaX) and sign(deltaY) == sign(lastDeltaY): # Moving cursor in same direction
                    segmentsInLastChange += 1

                    continue
                else: # Cursor direction changed
                    if segmentsInLastChange >= tolerance:
                        directionalChanges += 1
                    else:
                        segmentsInLastChange = 0

            lastDeltaX, lastDeltaY = deltaX, deltaY

        lastPoint = point

    return directionalChanges

def loadPatternChanges(patterns):
    directionalChanges = dict()

    for patternName in patterns:
        pattern = patterns[patternName]

        directionalChanges[patternName] = getDirectionalChanges(pattern, 0)

    return directionalChanges

def drawShape(shape, x, y, w, h, fill='white'):
    lastX, lastY = None, None
    
    for (localX, localY) in PATTERNS[shape]:
        newX, newY = x + localX*w, y + h - localY*h

        if shape == 'horizontalLine':
            newY -= h/2
        elif shape == 'verticalLine':
            newX += w/2

        if not (lastX == None or lastY == None):
            drawLine(newX, newY, lastX, lastY, fill=fill, lineWidth=4)

        lastX, lastY = newX, newY