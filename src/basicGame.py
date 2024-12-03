from cmu_graphics import *
from modules.character import Character
from modules.patterns import findPattern, loadPatternChanges, PATTERNS
from modules.timer import Timer
from modules.waves import startWave, drawWaveBanner
from modules.utilities import clamp
from modules.background import drawBackground, BackgroundStar, ShootingStar
from modules.configuration import CONFIGURATION
from uiElements import drawFrame, animate, Button
import math

def drawGameOver(app):
    w, h = app.width/3, app.height/5

    drawFrame(app, (app.width - w)/2, (app.height - h)/2, w, h)
    drawLabel(app.won and 'You win!' or'Game over!', app.width/2, (app.height - h)/2 + app.margins*3, size = h/3.5, align='top', fill=app.textColor, font=app.font)
    drawLabel('Press any key to restart', app.width/2, (app.height - h)/2 + h - app.margins*3, size = h/5, align='bottom', fill=app.textColor, font=app.font)

def drawPaused(app):
    w, h = app.width/6, app.height/8

    drawRect((app.width - w)/2, 0, w, h, fill='gray')
    drawLabel('Paused', app.width/2, h/2, size = h/2, fill=app.textColor, font=app.font)

def drawPoints(app, points, opacity=100):
    lastPointX = lastPointY = None

    for (x, y) in points:
        y = app.height - y

        if lastPointX != None and lastPointY != None:
            drawLine(x, y, lastPointX, lastPointY, fill='white', lineWidth=4, opacity=opacity)
        lastPointX, lastPointY = x, y

def drawMousePoints(app):
    if len(app.mousePoints) > 0:
        drawPoints(app, app.mousePoints)

    if len(app.fadingMousePoints) > 0:
        for tickOfPoints in app.fadingMousePoints:
            points = app.fadingMousePoints[tickOfPoints]
            opacity = clamp(100*(1 - ((app.tick - tickOfPoints) / app.stepsPerSecond)), 0, 100)
            drawPoints(app, points, opacity=opacity)

def drawStartScreen(app):
    drawLabel('Cosmic Combos', app.cx, app.cy/2, size=app.height/10, font=app.font, italic=True, fill=app.secondaryColor, border=app.primaryColor, rotateAngle=5*(math.sin(app.tick/15)), opacity=app.opacityFactor)

    for button in app.buttons:
        button.draw()

def pressStartButton(app):
    app.starting = True

    Timer(app, 1, 1, startGame)

def startGame(app):
    restartGame(app, doFirstLoad=True)
    app.started = True

def onGameOver(app, won):
    app.won = won
    app.gameOver = True
    app.mousePoints = []

def restartGame(app, doFirstLoad):
    if not doFirstLoad:
        app.character.__init__(app)

    app.mousePoints = []
    app.fadingMousePoints = dict()

    app.score = 0

    app.enemies = set()
    app.lastEnemy = False

    app.paused = False
    app.internalPause = False
    app.gameOver = False
    app.won = False

    app.tick = 0

    app.waveIndex = 0
    startWave(app)

def onAppStart(app):
    app.tick = 0

    # Difficulty
    app.difficulty = 'Hard'

    # Theme
    app.font = 'montserrat'
    app.primaryColor = rgb(32, 0, 54)
    app.secondaryColor = rgb(210, 142, 255)
    app.textColor = 'white'
    app.margins = 8

    # Start Screen
    app.started = False
    app.cx, app.cy = app.width/2, app.height/2
    app.buttons = []

    startButtonW, startButtonH = app.width/4, app.height/5
    startButtonX, startButtonY = app.cx - startButtonW/2, app.cy - startButtonH/2
    Button(app, "Launch", startButtonX, startButtonY, startButtonW, startButtonH, pressStartButton)

    difficulties = CONFIGURATION['difficulties']
    numDifficulties = len(difficulties)
    difficultyW, difficultyH = app.width/8, app.height/10

    difficultiesStartX = (startButtonX + startButtonW/2) - ((difficultyW + app.margins*4)*numDifficulties)/2
    difficultiesStartY = startButtonY + startButtonH + app.margins*4

    for level in difficulties:
        difficulty = difficulties[level]

        difficultyButton = Button(app, level, difficultiesStartX + (difficultyW + app.margins*4)*difficulty['index'], difficultiesStartY, difficultyW, difficultyH, lambda app: setattr(app, 'difficulty', level), depth=6, group='difficulties', fill=difficulty['fill'], secondaryFill=difficulty['secondaryFill'])

        if level == 'Easy':
            Button.selectedInGroup['difficulties'] = difficultyButton

    app.starting = False
    app.opacityFactor = 100
    
    app.shootingStars = []
    ShootingStar.generate(app, 4)
    app.backgroundStars = []
    BackgroundStar.generate(app, 30)

    # Game Mechanics
    app.character = Character(app)
    app.patternChanges = loadPatternChanges(PATTERNS)
    app.onGameOver = onGameOver # Must be called from the character file
    app.paused = False
    app.internalPause = False
    app.gameOver = False

def redrawAll(app):
    drawBackground(app)

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
    else:
        drawStartScreen(app)

def onMousePress(app, x, y):
    app.mousePoints = []
    
    if not app.started:
        for button in app.buttons:
            button.checkClicked()

def onMouseRelease(app, x, y):
    if app.started:
        if len(app.mousePoints) > 1:
            currentTick = app.tick
            pattern = findPattern(PATTERNS, app.mousePoints, app.patternChanges)
            app.fadingMousePoints[currentTick] = app.mousePoints
            Timer(app, 1, 1, lambda _: app.fadingMousePoints.pop(currentTick))
            app.mousePoints = []

            toRemove = set()

            for enemy in app.enemies:
                if enemy.hasPattern(pattern):
                    toRemove.add(enemy)

            for enemy in toRemove:
                enemy.patterns.pop()
                
                if len(enemy.patterns) == 0:
                    enemy.kill(reward=True)  

            if len(toRemove) > 1: # Give a bonus for comboing patterns
                app.score += CONFIGURATION['comboBonus']*(len(toRemove)**2)
    else:
        for button in app.buttons:
            button.pressed = False

def onMouseDrag(app, x, y):
    if app.started and not app.gameOver:
        app.mousePoints.append((x, app.height - y))

def onMouseMove(app, x, y):
    if not app.started:
        for button in app.buttons:
            button.checkMouseInBounds(x, y)

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

        for button in app.buttons:
            button.hoverEffect()
    
        app.opacityFactor = animate(app.opacityFactor, app.starting, -25, 0, 100)

def main():
    app = runApp(width=1208, height=720)
 
if __name__ == '__main__':
    main()