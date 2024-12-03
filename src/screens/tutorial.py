from cmu_graphics import *

from modules.ui import drawFrame, generateCraters, drawAsteroidEnemy, drawHeartEnemy, drawHeart
from modules.configuration import CONFIGURATION

import screens.menu as menu

def topLeft(app, x, y, w, h):
    drawAsteroidEnemy(app.tutorialCraters[0], x + w/2, y + h*app.tutorialEnemyRadiusRatio + app.margins*5, h*app.tutorialEnemyRadiusRatio*2, ['lor', 'triangle', 'land'])

def topRight(app, x, y, w, h):
    shapePadding = app.margins*2
    shapeSize = h/2
    numShapes = CONFIGURATION['startingLives']
    allShapesW = numShapes*shapeSize + (numShapes + 1)*shapePadding

    for i in range(numShapes):
        topX = x + (w - allShapesW)/2 + (i + 1)*(shapePadding) + i*shapeSize
        topY = y + (h - shapeSize)/2
        drawHeart(app, topX, topY, shapeSize, shapeSize)

        if i == (numShapes - 1):
            drawLine(topX, topY, topX + shapeSize, topY + shapeSize, lineWidth=app.margins, fill='white')
            drawLine(topX + shapeSize, topY, topX, topY + shapeSize, lineWidth=app.margins, fill='white')


def bottomLeft(app, x, y, w, h):
    drawHeartEnemy(app, x + w/2, y + h*app.tutorialEnemyRadiusRatio + app.margins*5, h*app.tutorialEnemyRadiusRatio*2)

def bottomRight(app, x, y, w, h):
    drawAsteroidEnemy(app.tutorialCraters[1], x + w/4, y + h*app.tutorialEnemyRadiusRatio + app.margins*5, h*app.tutorialEnemyRadiusRatio*2, ['lightning', 'verticalLine'])
    drawAsteroidEnemy(app.tutorialCraters[2], x + w*(3/4), y + h*app.tutorialEnemyRadiusRatio + app.margins*5, h*app.tutorialEnemyRadiusRatio*2, ['lightning', 'horizontalLine'])

def drawTutorialFrame(app, x, y, w, h, content, caption):
    drawFrame(app, x, y, w, h*(3/4), fill=app.darkColor, secondaryFill='dimGray')

    content(app, x, y, w, h*(3/4))

    drawFrame(app, x, y + h*(3/4), w, h/4, text=caption, textH=h/12, border=None, fill=app.darkColor, secondaryFill='dimGray')

def draw(app):    
    # Top Left
    drawTutorialFrame(app, app.margins*4, app.margins*4, app.gridElementW, app.gridElementH, topLeft, 'Draw patterns with cursor in the wave of asteroids')

    # Top Right
    drawTutorialFrame(app, app.margins*4 + app.gridElementW + app.margins*4, app.margins*4, app.gridElementW, app.gridElementH, topRight, 'If an asteroid gets too close you lose a heart')

    # Bottom Left
    drawTutorialFrame(app, app.margins*4, app.margins*4 + app.gridElementH + app.margins*4, app.gridElementW, app.gridElementH, bottomLeft, 'An extra heart spawns in the second wave')

    # Bottom Right
    drawTutorialFrame(app, app.margins*4 + app.gridElementW + app.margins*4, app.margins*4 + app.gridElementH + app.margins*4, app.gridElementW, app.gridElementH, bottomRight, 'Get extra points for matching patterns')

def start(app):
    app.gridElementW, app.gridElementH = (app.width - app.margins*4*3)/2, (app.height - app.margins*10 - app.height/7.5)/2

    app.tutorial = True
    app.tutorialEnemyRadiusRatio = (1/8)*(3/4)
    app.tutorialCraters = []
    for _ in range(4):
        app.tutorialCraters.append(generateCraters(app.gridElementH*app.tutorialEnemyRadiusRatio, 5))

    menu.hideStartButtons(app)

    app.mainMenuButton.visible = True