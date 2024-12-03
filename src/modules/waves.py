from cmu_graphics import *
from modules.timer import Timer
from modules.combos import *
from modules.enemy import HeartGivingStar
from modules.configuration import CONFIGURATION
from uiElements import drawFrame

WAVES = [ # Velocity and spawn delay are affected by the user chosen difficulty
    {
        'Velocity': 30,
        'SpawnDelay': 4,
        'Amount': [(randomCombo(2), 2), (sameCombo(2), 2), (randomCombo(2), 1), (sameCombo(3), 1)]
    },
    {
        'Velocity': 40,
        'SpawnDelay': 3,
        'Amount': [(repeatedCombo(2, 1), 2), (sameCombo(3), 2), 'heart', (randomCombo(3), 2), (randomCombo(3), 2)]
    },
    {
        'Velocity': 30,
        'SpawnDelay': 1,
        'Amount': [(repeatedCombo(4, 2), 1)]
    },
]

def buildWave(app, wave):
    app.lastEnemy = False

    Timer(app, 1, 1, lambda _: setattr(app, 'waveBanner', False)) # ChatGPT taught me setattr and lambda functions
    
    cumulativeTime = 0

    for comboType in wave:
        if comboType == 'heart':
            cumulativeTime += app.enemySpawnDelay

            Timer(app, cumulativeTime, 1, HeartGivingStar)
        else:
            for i in range(comboType[1]):
                cumulativeTime += app.enemySpawnDelay

                Timer(app, cumulativeTime, 1, comboType[0].spawn)

    Timer(app, cumulativeTime, 1, lambda _: setattr(app, 'lastEnemy', True))

def startWave(app):
    app.waveBanner = True
    app.waveIndex = app.waveIndex + 1
    
    if app.waveIndex > len(WAVES):
        app.onGameOver(app, won=True)

        return

    wave = WAVES[app.waveIndex - 1]

    difficulty = CONFIGURATION['difficulties'][app.difficulty]

    app.enemyVelocity = wave['Velocity'] + difficulty['additionalVelocity']
    app.enemySpawnDelay = wave['SpawnDelay'] - difficulty['subtractedSpawnDelay']

    Timer.defer(lambda: buildWave(app, wave['Amount']))


def drawWaveBanner(app):
    w, h = app.width/3, app.height/5
    x, y, = (app.width - w) / 2, (app.height - h) / 2
    
    drawFrame(app, x, y, w, h, text=f'Wave {app.waveIndex}')