from cmu_graphics import *

from modules.timer import Timer
from modules.background import drawBackground
from modules.ui import drawFrame

import screens.game as game
import screens.menu as menu
import screens.tutorial as tutorial

def drawPaused(app):
    w, h = app.width/6, app.height/8

    drawFrame(app, (app.width - w)/2, app.margins*4, w, h, depth=6, fill='dimGray', secondaryFill=app.darkColor, text='Paused')

def onAppStart(app):
    app.tick = 0

    # Theme
    app.font = 'orbitron'
    app.primaryColor = rgb(32, 0, 54)
    app.secondaryColor = rgb(210, 142, 255)
    app.darkColor = rgb(25, 25, 25)
    app.textColor = 'white'
    app.margins = 8

    # Start Screen
    menu.initialize(app)

    # Game
    game.initialize(app)
    
def redrawAll(app):
    drawBackground(app)

    if app.started:
        game.draw(app)
    elif app.tutorial:
        tutorial.draw(app)
    else:
        menu.draw(app)
        
    for button in app.buttons:
        button.draw()

    if app.paused:
        drawPaused(app)

def onMousePress(app, x, y):    
    for button in app.buttons:
        button.checkClicked()

    game.onMousePress(app, x, y)

def onMouseRelease(app, x, y):
    for button in app.buttons:
            button.pressed = False

    if app.started:
        game.onMouseRelease(app, x, y)

def onMouseDrag(app, x, y):
    if app.started and not app.gameOver:
        game.onMouseDrag(app, x, y)

def onMouseMove(app, x, y):
    for button in app.buttons:
        button.checkMouseInBounds(x, y)

def onKeyPress(app, key):
    if key == 'p':
        app.paused = not app.paused
    elif app.gameOver:
        game.restart(app, doFirstLoad=False)

def onStep(app):
    for button in app.buttons:
        button.hoverEffect()

    if not (app.paused or app.gameOver):
        takeStep(app)

def takeStep(app):
    app.tick += 1

    Timer.runDeffered()

    for timer in Timer.timers:
        timer.tick(app)
        
    if app.started:
        game.tick(app)
    else:
        menu.tick(app)

def main():
    app = runApp(width=1208, height=720)
 
if __name__ == '__main__':
    main()