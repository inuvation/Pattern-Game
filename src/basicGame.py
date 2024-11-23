from cmu_graphics import *
from modules.character import Character
from modules.enemy import Enemy
from modules.patterns import findPattern, loadPatternChanges, PATTERNS
from modules.configuration import CONFIGURATION

def restartGame(app, doFirstLoad):
    if not doFirstLoad:
        app.character.__init__(app)

    app.score = 0

    app.enemies = set()
    app.enemies.add(Enemy(app))

    app.paused = False
    app.gameOver = False

def onGameOver(app):
    app.gameOver = True

def drawGameOver(app):
    w, h = app.width/3, app.height/5

    drawRect((app.width - w)/2, (app.height - h)/2, w, h, fill='gray')
    drawLabel('Game over!', app.width/2, (app.height - h)/2 + 8, size = h/2, align='top')
    drawLabel('Press any key to restart', app.width/2, (app.height - h)/2 + h - 8, size = h/4, align='bottom')

def drawPaused(app):
    w, h = app.width/6, app.height/8

    drawRect((app.width - w)/2, 0, w, h, fill='gray')
    drawLabel('Paused', app.width/2, h/2, size = h/2)

def drawScore(app):
    drawLabel(f'Score: {app.score}', app.width, 0, size=100, align='right-top')

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

    app.lastPattern = None
    app.patternChanges = loadPatternChanges(PATTERNS)
    
    app.mousePoints = []

    app.enemySpawnDelay = CONFIGURATION['enemySpawnDelay']
    app.enemySpawnTick = 0

    restartGame(app, doFirstLoad=True)
    app.onGameOver = onGameOver # Must be called from the character file

def redrawAll(app):
    app.character.drawCharacter()
    app.character.drawLives()

    for enemy in app.enemies:
        enemy.drawEnemy()

    drawMousePoints(app)

    drawScore(app)

    if app.gameOver:
        drawGameOver(app)

    if app.paused:
        drawPaused(app)

def onMousePress(app, x, y):
    app.mousePoints = []

def onMouseRelease(app, x, y):
    if len(app.mousePoints) > 1:
        app.lastPattern = findPattern(PATTERNS, app.mousePoints, app.patternChanges)
        
        toRemove = set()

        for enemy in app.enemies:
            if enemy.hasPattern(app.lastPattern):
                toRemove.add(enemy)

        for enemy in toRemove:
            enemy.patterns.pop()
            
            if len(enemy.patterns) == 0:
                enemy.kill()  

def onMouseDrag(app, x, y):
    app.mousePoints.append((x, app.height - y))

def onKeyPress(app, key):
    if key == 'p':
        app.paused = not app.paused
    elif app.gameOver:
        restartGame(app, doFirstLoad=False)

def onStep(app):
    if not (app.paused or app.gameOver):
        takeStep(app)

def takeStep(app):
    app.enemySpawnTick += 1

    if app.enemySpawnTick >= app.enemySpawnDelay*app.stepsPerSecond:
        app.enemies.add(Enemy(app))

        app.enemySpawnTick = 0

    toRemove = set()

    for enemy in app.enemies:
        enemy.moveToCharacter()

        if distance(enemy.x, enemy.y, app.character.x, app.character.y) <= app.character.radius + enemy.radius:
            app.character.takeLife()
            toRemove.add(enemy)

    for enemy in toRemove:
        enemy.kill()

def main():
    app = runApp(width=1208, height=720)
 
if __name__ == '__main__':
    main()