from cmu_graphics import *
from modules.character import Character
from modules.enemy import Enemy
from modules.patterns import findPattern, loadPatternChanges, loadPatterns
from modules.configuration import loadConfiguration

def restartGame(app, doFirstLoad):
    if not doFirstLoad:
        app.character.__init__()

    app.score = 0
    app.accuracy = 100

    app.enemies = []
    app.enemies.append(Enemy(app))

def drawScore(app):
    drawLabel(f'Score: {app.score}', app.width, 0, size=100, align='right-top')
    drawLabel(f'Accuracy: {app.accuracy}', app.width, 100, size=60, align='right-top')

def drawMousePoints(app):
    if len(app.mousePoints) > 0:
        lastPointX = lastPointY = None

        for (x, y) in app.mousePoints:
            y = app.height - y

            if lastPointX != None and lastPointY != None:
                drawLine(x, y, lastPointX, lastPointY)
            lastPointX, lastPointY = x, y

def onAppStart(app):
    app.character = Character(app)

    app.patterns = loadPatterns()
    app.lastPattern = None
    app.patternChanges = loadPatternChanges(app.patterns)
    
    app.mousePoints = []

    app.enemySpawnDelay = loadConfiguration()['enemySpawnDelay']
    app.enemySpawnTick = 0

    restartGame(app, doFirstLoad=True)

def redrawAll(app):
    app.character.drawCharacter()
    app.character.drawLives()

    for enemy in app.enemies:
        enemy.drawEnemy()

    drawMousePoints(app)

    drawScore(app)

def onMousePress(app, x, y):
    app.mousePoints = []

def onMouseRelease(app, x, y):
    if len(app.mousePoints) > 1:
        app.lastPattern = findPattern(app.patterns, app.mousePoints, app.patternChanges)
        
        for enemy in app.enemies:
                enemy.checkForPattern(app.lastPattern)

def onMouseDrag(app, x, y):
    app.mousePoints.append((x, app.height - y))

def onStep(app):
    app.enemySpawnTick += 1

    if app.enemySpawnTick >= app.enemySpawnDelay*app.stepsPerSecond:
        app.enemies.append(Enemy(app))

        app.enemySpawnTick = 0

    for enemy in app.enemies:
        enemy.tick()

def main():
    app = runApp(width=1208, height=720)
 
if __name__ == '__main__':
    main()