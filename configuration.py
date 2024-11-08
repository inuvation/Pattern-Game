def mainConfiguration():
    return {
        'deltaSegmentTolerance': 15
    }


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
