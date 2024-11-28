from modules.configuration import CONFIGURATION
from modules.utilities import getCommaSeperatedStringFromList, randInRange
import modules.waves 
from modules.timer import Timer
from cmu_graphics import *
import random
import math

class Enemy():
    id = 0

    def __init__(self, app, patterns, x=None, y=None):
        self.radius = 30

        if x == None or y == None:
            randNum = random.random()

            if randNum >= 0.5:
                x = app.width - self.radius*2
            else:
                x = self.radius*2

            y = randInRange(app.height/8, app.height*(7/8))

        self.x, self.y = x, y
        self.velocity = app.enemyVelocity

        self.patterns = patterns

        self.id = Enemy.id
        Enemy.id += 1

        self.app = app
        app.enemies.add(self)

    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return isinstance(other, Enemy) and (self.id == other.id)

    def moveToCharacter(self):
        angleToCharacter = math.atan2(self.app.character.y - self.y, self.app.character.x - self.x)

        self.x += math.cos(angleToCharacter)*(self.velocity/app.stepsPerSecond)
        self.y += math.sin(angleToCharacter)*(self.velocity/app.stepsPerSecond)

    def kill(self):
        self.app.enemies.remove(self)
        self.app.score += CONFIGURATION['scorePerEnemyKilled']

        if len(self.app.enemies) == 0:
            Timer(app, 1, 1, modules.waves.startWave)

    def hasPattern(self, pattern):
        if self.patterns[-1] == pattern:
           return True
            
    def drawEnemy(self):
        drawCircle(self.x, self.y, self.radius, fill='green')
        drawLabel(getCommaSeperatedStringFromList(self.patterns), self.x, self.y + self.radius, align='top')