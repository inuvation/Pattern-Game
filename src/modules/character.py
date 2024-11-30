from modules.configuration import CONFIGURATION
from cmu_graphics import *

heart = 'src/images/heart.png' # Taken from flatIcon (https://www.flaticon.com/free-icon/heart_9484251)
earth = 'src/images/earth.png' # Taken from flatIcon (https://www.flaticon.com/free-icon/heart_9484251)

class Character():
    def __init__(self, app):
        self.x, self.y = app.width/2, app.height/2
        self.lives = CONFIGURATION['startingLives']
        self.radius = 50

        self.app = app

    def addLife(self):
        self.lives += 1

    def takeLife(self):
        self.lives -= 1

        if self.lives <= 0:
            app.onGameOver(self.app)
            
    def drawCharacter(self):
        drawImage(earth, self.x - self.radius, self.y - self.radius, width=self.radius*2, height = self.radius*2, opacity=50)

    def drawLives(self):
        for i in range(self.lives):
            drawImage(heart, 0+ 100*i, 0, width=100, height=100)