import random
import math

def sign(n):
    if n < 0: return -1
    elif n == 0: return 0 
    else: return 1

def distance(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

def createMatrix(rows, cols):
    return [([None] * cols) for row in range(rows)]

def normalize(matrix):
    x = [point[0] for point in matrix]
    y = [point[1] for point in matrix]

    minX = min(x)
    minY = min(y)

    maxX = max(x)
    maxY = max(y)

    scaleBy = max(maxX - minX, maxY - minY)

    normalizedMatrix = []
    for point in matrix:
        originX, originY = point[0] - minX, point[1] - minY
        normalizedX, normalizedY = originX / scaleBy, originY / scaleBy

        normalizedMatrix.append((normalizedX, normalizedY))

    return normalizedMatrix

def rotateNormalizedMatrix(matrix, angle):
    rotatedMatrix = []

    for point in matrix:
        x = point[0]
        y = point[0]

        # Center at the origin
        x -= 0.5
        y -= 0.5 

        # Rotation matrix
        newX = x*math.cos(angle) - y*math.sin(angle)
        newY = x*math.sin(angle) + y*math.cos(angle)

        # Rebound from (0, 0) to (1, 1)
        newX += 0.5
        newY += 0.5

        rotatedMatrix.append((newX, newY))

    return rotatedMatrix

def getCommaSeperatedStringFromList(L):
    string = ''

    i = 0
    for s in L:
        if i == 0: string += s
        else: string += f', {s}'
        
        i += 1

    return string

def randInRange(low, high):
    return low + (high - low)*random.random()

def clamp(n, low, high):
    return max(low, min(high, n))   