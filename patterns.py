from cmu_graphics import *
import math

def distance(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

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

            
def createMatrix(rows, cols):
    return [([None] * cols) for row in range(rows)]

# CONFIGURATION

def loadPatterns():
    return {
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
            (1, 0),
        ],
        'lor': [
            (0, 1),
            (0.5, 0),
            (1, 1),
        ],
    }

def normalise(matrix): # CHATGPT
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


def findPattern(app, mouseSegments):
    lowestCost, closestShape = None, None

    normalisedMouseSegments = normalise(mouseSegments)

    for patternName in app.patterns:
        pattern = app.patterns[patternName]

        forwardCostMatrix = dynamicTimeWarpCost(normalisedMouseSegments, pattern)
        topRow, topCol = len(forwardCostMatrix) - 1, len(forwardCostMatrix[0]) - 1
        fowardCost = forwardCostMatrix[topRow][topCol]

        backwaredCostMatrix = dynamicTimeWarpCost(normalisedMouseSegments, list(reversed(pattern)))
        backwardCost = backwaredCostMatrix[topRow][topCol]

        cost = min(fowardCost, backwardCost)

        if lowestCost == None or cost < lowestCost:
            lowestCost, closestShape = cost, patternName

    return closestShape

# CMU GRAPHICS

def onAppStart(app):
    app.patternError = 15 # Degree to which a player drawn shape can vary from the configured pattern
    app.patterns = loadPatterns()
    app.stepsPerSecond = 5


def onMousePress(app, x, y):
    app.mouseSegments = []

def onMouseRelease(app, x, y):
    if len(app.mouseSegments) > 1:
        pattern = findPattern(app, app.mouseSegments)

        print(pattern)

def onMouseDrag(app, x, y):
    app.mouseSegments.append((x, app.height - y))


def main():
    app = runApp(width=640, height=360)

if __name__ == '__main__':
   main()