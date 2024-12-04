from cmu_graphics import *

from modules.character import Character
from modules.patterns import loadPatternChanges, PATTERNS, findPattern
from modules.utilities import clamp
from modules.timer import Timer
from modules.configuration import CONFIGURATION

from modules.ui import Button, drawFrame

import main
import modules.waves as waves
import screens.menu as menu

def initialize(app):
    app.difficulty = 'Easy'

    buttonW, buttonH = app.width/6, app.height/7.5

    app.mainMenuButton = Button(app, "Main Menu", app.margins*4, app.height - buttonH/2 - app.margins*4, buttonW*0.75, buttonH/2, main.onAppStart, depth=6, fill=app.darkColor, secondaryFill='dimGray')
    app.pauseButton = Button(app, "Pause", app.margins*8 + buttonW*0.75, app.height - buttonH/2 - app.margins*4, buttonW/2, buttonH/2, lambda app: setattr(app, 'paused', not app.paused), depth=6, fill=app.darkColor, secondaryFill='dimGray')
    app.mainMenuButton.visible = False
    app.pauseButton.visible = False
    
    app.character = Character(app)
    app.patternChanges = loadPatternChanges(PATTERNS)
    app.onGameOver = onGameOver # Must be called from the character file
    app.paused = False
    app.internalPause = False
    app.gameOver = False

def start(app):
    menu.hideStartButtons(app)
    
    restart(app, doFirstLoad=True)
    
    app.mainMenuButton.visible = True
    app.pauseButton.visible = True
    
    app.started = True

def restart(app, doFirstLoad):
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
    waves.start(app)

def draw(app):
    app.character.drawCharacter()
    app.character.drawLives()

    for enemy in app.enemies:
        enemy.drawEnemy()

    drawMousePoints(app)

    w, h = app.width/3, app.height/5
    x, y, = app.width - w - app.margins, app.margins
    drawFrame(app, x, y, w, h, invertColor=True, text=f'Score: {app.score}')

    if app.waveBanner:
        waves.drawWaveBanner(app)

    if app.gameOver:
        drawGameOver(app)

def onMouseRelease(app, x, y):
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
            enemy.patterns.pop(0)
            
            if len(enemy.patterns) == 0:
                enemy.kill(reward=True)  

        if len(toRemove) > 1: # Give a bonus for comboing patterns
            app.score += CONFIGURATION['comboBonus']*(len(toRemove)**2)

def onMouseDrag(app, x, y):
    if not app.paused:
        app.mousePoints.append((x, app.height - y))

def onMousePress(app, x, y):
    app.mousePoints = []

def onGameOver(app, won):
    app.won = won
    app.gameOver = True
    app.mousePoints = []

def tick(app):
    for enemy in app.enemies:
            enemy.moveToCharacter()

            if distance(enemy.x, enemy.y, app.character.x, app.character.y) <= app.character.radius + enemy.radius:
                Timer.defer(app.character.takeLife)
                Timer.defer(enemy.kill)

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

def drawGameOver(app):
    w, h = app.width/2.5, app.height/5

    drawFrame(app, (app.width - w)/2, (app.height - h)/2, w, h)
    drawLabel(app.won and 'You win!' or 'Game over!', app.width/2, (app.height - h)/2 + app.margins*3, size = h/3.5, align='top', fill=app.textColor, font=app.font)
    drawLabel('Press any key to restart', app.width/2, (app.height - h)/2 + h - app.margins*3, size = h/5, align='bottom', fill=app.textColor, font=app.font)
