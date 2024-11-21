from modules.configuration import CONFIGURATION
from modules.utilities import sign, distance, getCommaSeperatedStringFromList, randInRange
from cmu_graphics import *
import random

class Enemy():
    id = 0

    def __init__(self, app, x=None, y=None):
        self.radius = 30

        if x == None or y == None:
            randNum = random.random()

            if randNum >= 0.5:
                x = app.width - self.radius*2
            else:
                x = self.radius*2

            y = randInRange(app.height/4, app.height*(3/4))

        self.x, self.y = x, y
        self.patterns = ['lor', 'triangle']
        self.velocity = CONFIGURATION['enemyVelocity']

        self.id = Enemy.id
        Enemy.id += 1

        self.app = app

    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return isinstance(other, Enemy) and (self.id == other.id)

    def tick(self):
        charX, charY = self.app.character.x, self.app.character.y

        self.x += sign(charX - self.x)*(self.velocity/app.stepsPerSecond)
        self.y += sign(charY - self.y)*(self.velocity/app.stepsPerSecond)

        if distance(self.x, self.y, charX, charY) <= app.character.radius + self.radius:
            self.kill()
            app.character.takeLife()

    def kill(self):
        self.app.enemies.remove(self)
        self.app.score += CONFIGURATION['scorePerEnemyKilled']

    def hasPattern(self, pattern):
        if self.patterns[-1] == pattern:
           return True
            
    def drawEnemy(self):
        drawCircle(self.x, self.y, self.radius, fill='green')
        drawLabel(getCommaSeperatedStringFromList(self.patterns), self.x, self.y + self.radius, align='top')