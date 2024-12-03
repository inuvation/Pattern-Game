CONFIGURATION = {
    'deltaSegmentTolerance': 15,
    'directionChangeTolerance': 2,
    'startingLives': 3,
    'scorePerEnemyKilled': 50,
    'comboBonus': 10, # bonus*(numEnemies**2) 40 for 2 enemies, 90 for 3, 160 for 4
    'heartVelocity': 75,
    'difficulties': {
        'Easy': {
            'index': 0,
            'fill': 'lightGreen',
            'secondaryFill': 'darkSeaGreen',
            'additionalVelocity': 0,
            'subtractedSpawnDelay': 0
        },
        'Medium': {
            'index': 1,
            'fill': 'darkOrange',
            'secondaryFill': 'orangeRed',
            'additionalVelocity': 10,
            'subtractedSpawnDelay': 0.5
        },
        'Hard': {
            'index': 2,
            'fill': 'fireBrick',
            'secondaryFill': 'darkRed',
            'additionalVelocity': 20,
            'subtractedSpawnDelay': 1
        }
    }
}