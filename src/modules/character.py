from modules.configuration import CONFIGURATION
from uiElements import drawHeart, drawEarth, generateLandMasses
from cmu_graphics import *

heart = 'src/images/heart.png' # Taken from flatIcon (https://www.flaticon.com/free-icon/heart_9484251)
earth = 'src/images/earth.png' # Taken from flatIcon (https://www.flaticon.com/free-icon/heart_9484251)

class Character():
    def __init__(self, app):
        self.x, self.y = app.width/2, app.height/2
        self.lives = CONFIGURATION['startingLives']
        self.radius = 50

        self.landMasses = generateLandMasses(self.x, self.y, self.radius, 4) # Note: This will break if moving is added to the character as coordinates are "baked" into the generated polygon

        self.app = app

    def addLife(self):
        self.lives += 1

    def takeLife(self):
        self.lives -= 1

        if self.lives <= 0:
            app.onGameOver(self.app, won=False)
            
    def drawCharacter(self):
        # drawImage(earth, self.x - self.radius, self.y - self.radius, width=self.radius*2, height = self.radius*2)
        # drawCircle(self.x, self.y, self.radius, fill='green')
        drawEarth(self.landMasses, self.x, self.y, self.radius)

    def drawLives(self):
        for i in range(self.lives):
            drawHeart(self.app, app.margins*2 + (100 + app.margins)*i, app.margins, 100 - app.margins*2, 100 - app.margins*2)
