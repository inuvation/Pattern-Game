from modules.configuration import CONFIGURATION
from modules.utilities import getCommaSeperatedStringFromList, randInRange
from modules.patterns import drawShape
from uiElements import drawFrame, drawAsteroid, generateCraters
import modules.waves 
from modules.timer import Timer
from cmu_graphics import *
import random
import math


asteroid = 'src/images/asteroid.png' # Taken from flatIcon (https://www.flaticon.com/free-icon/asteroid_2530826?term=asteroid&page=1&position=2&origin=search&related_id=2530826)

class Enemy():
    id = 0

    def __init__(self, app, patterns, x=None, y=None):
        self.radius = 50

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

        self.craters = generateCraters(self.radius, pythonRound(randInRange(4,6)))

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

    def kill(self, reward=False):
        self.app.enemies.remove(self)

        if reward:
            self.app.score += CONFIGURATION['scorePerEnemyKilled']

        if len(self.app.enemies) == 0:
            Timer(app, 1, 1, modules.waves.startWave)

    def hasPattern(self, pattern):
        if self.patterns[-1] == pattern:
           return True
            
    def drawEnemy(self):
        drawAsteroid(self.craters, self.x, self.y, self.radius)

        shapePadding = app.margins*2
        shapeSize = 64
        numShapes = len(self.patterns)
        w = numShapes*shapeSize + (numShapes + 1)*shapePadding

        drawFrame(app, self.x - w/2, self.y + self.radius, w, shapeSize + shapePadding*2)

        for i in range(numShapes):
            drawShape(self.patterns[i], self.x - w/2 + (i + 1)*(shapePadding) + i*shapeSize, self.y + self.radius + shapePadding, shapeSize, shapeSize, fill=(i == (numShapes - 1) and 'white' or 'gray'))