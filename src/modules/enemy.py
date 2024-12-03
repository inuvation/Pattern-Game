from modules.configuration import CONFIGURATION
from modules.utilities import getCommaSeperatedStringFromList, randInRange
from modules.patterns import drawShape
from uiElements import drawFrame, drawAsteroid, generateCraters, drawHeart
import modules.waves 
from modules.timer import Timer
from cmu_graphics import *
import random
import math

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

        if len(self.app.enemies) == 0 and self.app.lastEnemy:
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

        drawFrame(app, self.x - w/2, self.y + self.radius, w, shapeSize + shapePadding*2, depth=numShapes*4)

        for i in range(numShapes):
            drawShape(self.patterns[i], self.x - w/2 + (i + 1)*(shapePadding) + i*shapeSize, self.y + self.radius + shapePadding, shapeSize, shapeSize, fill=(i == (numShapes - 1) and 'white' or 'gray'))

class HeartGivingStar(Enemy):
    def __init__(self, app):
        super().__init__(app, ['heart'])
        self.velocity = CONFIGURATION['heartVelocity']
        self.x = self.radius*2
        self.angle = randInRange(math.radians(25), math.radians(35))


    def kill(self, reward=False):
        self.app.enemies.remove(self)

        self.app.character.lives += 1

    def moveToCharacter(self):
        self.x += math.cos(self.angle)*(self.velocity/app.stepsPerSecond)
        self.y += math.sin(self.angle)*(self.velocity/app.stepsPerSecond)

        if self.x - self.radius > self.app.width or self.y - self.radius > self.app.height:
            Timer.defer(lambda: self.app.enemies.remove(self))

    def drawEnemy(self):
        drawHeart(app, self.x - self.radius, self.y - self.radius, self.radius*2, self.radius*2)

        shapePadding = app.margins*2
        shapeSize = 64
        numShapes = len(self.patterns)
        w = numShapes*shapeSize + (numShapes + 1)*shapePadding

        drawFrame(app, self.x - w/2, self.y + self.radius, w, shapeSize + shapePadding*2)

        for i in range(numShapes):
            drawShape(self.patterns[i], self.x - w/2 + (i + 1)*(shapePadding) + i*shapeSize, self.y + self.radius + shapePadding, shapeSize, shapeSize, fill=(i == (numShapes - 1) and 'white' or 'gray'))