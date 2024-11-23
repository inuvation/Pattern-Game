# Citations
# https://www.youtube.com/watch?v=ERKDHZyZDwA (Dynamic time warping 1: Motivation)
# https://www.youtube.com/watch?v=9GdbMc4CEhE (Dynamic time warping 2: Algorithm)

import random

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