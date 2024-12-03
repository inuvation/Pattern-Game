import math

from modules.ui import drawLabel
import screens.menu as menu

def draw(app):
    drawLabel('Tutorial', app.cx, app.cy/3, size=app.height/10, font=app.font, italic=True, fill=app.secondaryColor, border=app.primaryColor, rotateAngle=5*(math.sin(app.tick/15)), opacity=(100 - app.opacityFactor))

def start(app):
    app.tutorial = True
    
    menu.hideStartButtons(app)

    app.mainMenuButton.visible = True