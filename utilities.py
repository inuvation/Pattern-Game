# Citations
# https://www.youtube.com/watch?v=ERKDHZyZDwA (Dynamic time warping 1: Motivation)
# https://www.youtube.com/watch?v=9GdbMc4CEhE (Dynamic time warping 2: Algorithm)

import math
from functools import cache
from configuration import mainConfiguration

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

    normalisedPatternToCheck = normalise(patternToCheck)
    patternToCheckDirectionChanges = getDirectionalChanges(normalisedPatternToCheck)

    if directionChangesToCompare == None:
        directionChangesToCompare = loadPatternChanges(listOfPatterns)

    for patternName in listOfPatterns:
        directionChanges = directionChangesToCompare[patternName]
        if patternToCheckDirectionChanges < directionChanges: continue

        pattern = listOfPatterns[patternName]
        fowardCost = getCost(normalisedPatternToCheck, pattern)
        backwardCost = getCost(normalisedPatternToCheck, list(reversed(pattern)))
        cost = min(fowardCost, backwardCost)
        if lowestCost == None or cost < lowestCost:
            lowestCost, closestShape = cost, patternName

    # print(f'user drawn shape has {directionChanges}, {closestShape} has {}')

    return closestShape

def getDirectionalChanges(pattern, tolerance=None):
    if tolerance == None:
        tolerance = mainConfiguration()['deltaSegmentTolerance']

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

# General Utilities

def sign(n):
    if n < 0: return -1
    elif n == 0: return 0 
    else: return 1

def distance(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

def createMatrix(rows, cols):
    return [([None] * cols) for row in range(rows)]

def normalise(matrix): # CREATED BY CHATGPT
    # Step 1: Translate the points to start at (0, 0)
    x_coords = [point[0] for point in matrix]
    y_coords = [point[1] for point in matrix]

    # Find the minimum x and y to translate the points
    min_x = min(x_coords)
    min_y = min(y_coords)

    # Translate all points so that the minimum x and y become (0, 0)
    translated_points = [(x - min_x, y - min_y) for x, y in matrix]

    # Step 2: Normalize the points while preserving the aspect ratio
    max_x = max([point[0] for point in translated_points])
    max_y = max([point[1] for point in translated_points])

    # Calculate the overall maximum range to maintain aspect ratio
    overall_max = max(max_x, max_y) if max(max_x, max_y) != 0 else 1

    # Normalize the points using the overall maximum
    normalized_points = [(x / overall_max, y / overall_max) for x, y in translated_points]

    return normalized_points