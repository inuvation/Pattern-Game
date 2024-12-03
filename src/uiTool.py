from cmu_graphics import *
from modules.ui import *

def redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill='black')

    drawFrame(app, app.margins, app.margins, 300, 200)
    drawHeart(app, 300 + app.margins, app.margins, 200, 200)
    drawAsteroid(app.craters, 300 + app.margins + 300, app.margins + 100, 100)
    drawEarth(app.landMasses, 300 + app.margins + 600, app.margins + 100, 100)

    for button in app.buttons:
        button.draw()

def onMousePress(app, x, y):
    for button in app.buttons:
        button.checkClicked()

def onMouseRelease(app, x, y):
    for button in app.buttons:
        button.pressed = False

def onMouseMove(app, x, y):
    for button in app.buttons:
        button.checkMouseInBounds(x, y)

def onStep(app):
    for button in app.buttons:
        button.hoverEffect()

def onAppStart(app):
    # Theme
    app.font = 'montserrat'
    app.primaryColor = rgb(32, 0, 54)
    app.secondaryColor = rgb(210, 142, 255)
    app.textColor = 'white'
    app.margins = 8

    app.opacityFactor = 100

    app.buttons = []
    Button(app, "Button", app.width/2, app.height/2, app.width/5, app.height/8, lambda _: print('clicked!'))

    app.craters = generateCraters(100, 5)
    app.landMasses = generateLandMasses(300 + app.margins + 600, app.margins + 100, 100, 4)

def main():
    app = runApp(width=1208, height=720)

if __name__ == '__main__':
   main()