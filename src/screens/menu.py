import math

from modules.timer import Timer
from modules.ui import drawLabel, Button
from modules.background import ShootingStar, BackgroundStar
from modules.ui import animate
from modules.configuration import CONFIGURATION

import screens.game as game
import screens.tutorial as tutorial

def initialize(app):
    app.started = False
    app.cx, app.cy = app.width/2, app.height/2
    app.buttons = []

    startButtonW, startButtonH = app.width/4, app.height/5
    startButtonX, startButtonY = app.cx - startButtonW/2, app.cy/1.5 - startButtonH/2
    app.launchButton = Button(app, "Launch", startButtonX, startButtonY, startButtonW, startButtonH, pressStartButton)

    difficulties = CONFIGURATION['difficulties']
    numDifficulties = len(difficulties)
    difficultyW, difficultyH = app.width/6, app.height/7.5
    difficultiesStartX = (startButtonX + startButtonW/2) - ((difficultyW + app.margins*4)*numDifficulties)/2
    difficultiesStartY = startButtonY + startButtonH + app.margins*4
    for level in difficulties:
        difficulty = difficulties[level]

        difficultyButton = Button(app, level, difficultiesStartX + (difficultyW + app.margins*4)*difficulty['index'], difficultiesStartY, difficultyW, difficultyH, lambda app: setattr(app, 'difficulty', level), depth=6, group='difficulties', fill=difficulty['fill'], secondaryFill=difficulty['secondaryFill'])

        if level == 'Easy':
            Button.selectedInGroup['difficulties'] = difficultyButton

    app.tutorialButton = Button(app, "Tutorial", (app.width - difficultyW)/2, app.height - difficultyH - app.margins*4, difficultyW, difficultyH, tutorial.start, depth=6, fill=app.darkColor, secondaryFill='dimGray')

    app.shootingStars = []
    ShootingStar.generate(app, 4)
    app.backgroundStars = []
    BackgroundStar.generate(app, 30)

    app.tutorial = False
    app.starting = False
    app.opacityFactor = 100

def draw(app):
    drawLabel('Cosmic Combos', app.cx, app.cy/4, size=app.height/10, font=app.font, italic=True, fill=app.secondaryColor, border=app.primaryColor, rotateAngle=5*(math.sin(app.tick/15)), opacity=app.opacityFactor)

def tick(app):
    if not app.tutorial:
        for star in app.shootingStars:
            star.move()
    
    app.opacityFactor = app.launchButton.opacity = app.tutorialButton.opacity = animate(app.opacityFactor, app.starting or app.tutorial, -25, 0, 100)

    for button in app.buttons:
        if button.group == 'difficulties': button.opacity = app.opacityFactor

def pressStartButton(app):
    app.starting = True

    Timer(app, 1, 1, game.start)

def hideStartButtons(app):
    app.launchButton.visible = False
    app.tutorialButton.visible = False
    for button in app.buttons:
        if button.group == 'difficulties': button.visible = False