from modules.configuration import CONFIGURATION
from modules.utilities import sign, distance, getCommaSeperatedStringFromList, randInRange
from modules.combos import combo
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
        self.patterns = combo()
        self.velocity = CONFIGURATION['enemyVelocity']

        self.id = Enemy.id
        Enemy.id += 1

        self.app = app

    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return isinstance(other, Enemy) and (self.id == other.id)

    def moveToCharacter(self):
        self.x += sign(self.app.character.x - self.x)*(self.velocity/app.stepsPerSecond)
        self.y += sign(self.app.character.y - self.y)*(self.velocity/app.stepsPerSecond)

    def kill(self):
        self.app.enemies.remove(self)
        self.app.score += CONFIGURATION['scorePerEnemyKilled']

    def hasPattern(self, pattern):
        if self.patterns[-1] == pattern:
           return True
            
    def drawEnemy(self):
        drawCircle(self.x, self.y, self.radius, fill='green')
        drawLabel(getCommaSeperatedStringFromList(self.patterns), self.x, self.y + self.radius, align='top')