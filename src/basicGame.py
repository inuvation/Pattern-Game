from cmu_graphics import *
from modules.character import Character
from modules.patterns import findPattern, loadPatternChanges, PATTERNS
from modules.timer import Timer
from modules.waves import startWave, drawWaveBanner
from modules.utilities import clamp
from modules.background import drawBackground, BackgroundStar, ShootingStar
from uiElements import drawFrame

background = 'src/images/background.png' # Generated with Microsoft Designer

def startGame(app):
    restartGame(app, doFirstLoad=True)
    app.started = True

def restartGame(app, doFirstLoad):
    if not doFirstLoad:
        app.character.__init__(app)

    app.mousePoints = []

    app.score = 0

    app.enemies = set()

    app.paused = False
    app.internalPause = False
    app.gameOver = False

    app.tick = 0

    app.waveIndex = 0
    startWave(app)

def onGameOver(app):
    app.gameOver = True
    app.mousePoints = []

def drawGameOver(app):
    w, h = app.width/3, app.height/5

    drawRect((app.width - w)/2, (app.height - h)/2, w, h, fill='gray')
    drawLabel('Game over!', app.width/2, (app.height - h)/2 + 8, size = h/2, align='top', fill=app.textColor, font=app.font)
    drawLabel('Press any key to restart', app.width/2, (app.height - h)/2 + h - 8, size = h/4, align='bottom', fill=app.textColor, font=app.font)

def drawPaused(app):
    w, h = app.width/6, app.height/8

    drawRect((app.width - w)/2, 0, w, h, fill='gray')
    drawLabel('Paused', app.width/2, h/2, size = h/2, fill=app.textColor, font=app.font)

def drawMousePoints(app):
    if len(app.mousePoints) > 0:
        lastPointX = lastPointY = None

        for (x, y) in app.mousePoints:
            y = app.height - y

            if lastPointX != None and lastPointY != None:
                drawLine(x, y, lastPointX, lastPointY, fill='white')
            lastPointX, lastPointY = x, y

def drawStartScreen(app):
    drawRect(app.startX - 4, app.startY + 4, app.w, app.h, fill=app.secondaryColor, opacity=app.opacityFactor)

    drawRect(app.startX - app.hoverFactor, app.startY + app.hoverFactor, app.w, app.h, fill=app.primaryColor, opacity=app.opacityFactor)
   
    drawLabel('Launch', app.cx - app.hoverFactor, app.cy + app.hoverFactor, size=(app.h/2)*app.scaleFactor, font=app.font, fill=app.textColor, opacity=app.opacityFactor)

def onAppStart(app):
    app.tick = 0

    # Theme
    app.font = 'montserrat'
    app.primaryColor = rgb(32, 0, 54)
    app.secondaryColor = rgb(210, 142, 255)
    app.textColor = 'white'
    app.margins = 8

    # Start Screen
    app.started = False
    app.w, app.h = app.width/4, app.height/5
    app.cx, app.cy = app.width/2, app.height/2
    app.startX, app.startY = app.cx - app.w/2, app.cy - app.h/2
    app.hovered = False
    app.hoverFactor = 0
    app.pressed = False
    app.scaleFactor = 1
    app.starting = False
    app.opacityFactor = 100
    
    app.shootingStars = []
    ShootingStar.generate(app, 4)
    app.backgroundStars = []
    BackgroundStar.generate(app, 30)

    # Game Mechanics
    app.character = Character(app)
    app.lastPattern = None
    app.patternChanges = loadPatternChanges(PATTERNS)
    app.onGameOver = onGameOver # Must be called from the character file
    app.paused = False
    app.internalPause = False
    app.gameOver = False

def redrawAll(app):
    drawBackground(app)
    drawStartScreen(app)

    if app.started:
        app.character.drawCharacter()
        app.character.drawLives()

        for enemy in app.enemies:
            enemy.drawEnemy()

        drawMousePoints(app)

        w, h = app.width/3, app.height/5
        x, y, = app.width - w - app.margins, app.margins
        drawFrame(app, x, y, w, h, invertColor=True, text=f'Score: {app.score}')

        if app.waveBanner:
            drawWaveBanner(app)

        if app.gameOver:
            drawGameOver(app)

        if app.paused:
            drawPaused(app)

def onMousePress(app, x, y):
    app.mousePoints = []

    if app.hovered:
        app.pressed = True

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

    if app.pressed and not app.starting:
        app.starting = True

        Timer(app, 1, 1, startGame)

def onMouseDrag(app, x, y):
    app.mousePoints.append((x, app.height - y))

def onMouseMove(app, x, y):
    if not app.started:
        if x >= app.startX and x <= app.startX + app.w and y >= app.startY and y <= app.startY + app.h:
            app.hovered = True
        else:
            app.hovered = False

def onKeyPress(app, key):
    if key == 'p':
        app.paused = not app.paused
    elif app.gameOver:
        restartGame(app, doFirstLoad=False)

def onStep(app):
    if not (app.paused or app.gameOver):
        takeStep(app)

def takeStep(app):
    app.tick += 1

    Timer.runDeffered()

    for timer in Timer.timers:
        timer.tick(app)
        
    if app.started:
        for enemy in app.enemies:
            enemy.moveToCharacter()

            if distance(enemy.x, enemy.y, app.character.x, app.character.y) <= app.character.radius + enemy.radius:
                Timer.defer(app.character.takeLife)
                Timer.defer(enemy.kill)
    else:
        for star in app.shootingStars:
            star.move()
    
        if app.hovered or app.starting:
            app.hoverFactor = clamp(app.hoverFactor + 2, 0, 4)
        else:
            app.hoverFactor = clamp(app.hoverFactor - 2, 0, 4)

        if app.pressed or app.starting:
            app.scaleFactor = clamp(app.scaleFactor - 0.05, 0.9, 1)
        else:
            app.scaleFactor = clamp(app.scaleFactor + 0.05, 0.9, 1)

        if app.starting:
            app.opacityFactor = clamp(app.opacityFactor - 25, 0, 100)
        else:
            app.opacityFactor = clamp(app.opacityFactor + 25, 0, 100)

def main():
    app = runApp(width=1208, height=720)
 
if __name__ == '__main__':
    main()