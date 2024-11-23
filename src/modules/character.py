from modules.configuration import CONFIGURATION
from cmu_graphics import *

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
            self.app.onGameOver(app)
            
    def drawCharacter(self):
        drawCircle(self.x, self.y, self.radius)

    def drawLives(self):
        for i in range(self.lives):
            drawCircle(50 + 100*i, 50, 50, fill='red')