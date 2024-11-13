# Citations
# https://www.youtube.com/watch?v=ERKDHZyZDwA (Dynamic time warping 1: Motivation)
# https://www.youtube.com/watch?v=9GdbMc4CEhE (Dynamic time warping 2: Algorithm)

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