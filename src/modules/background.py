from cmu_graphics import *
from modules.timer import Timer
from modules.utilities import randInRange
import math

class ShootingStar():
    id = 0

    def __init__(self, app):
        self.respawning = True
        self.respawn(app)
    
        self.id = ShootingStar.id
        ShootingStar.id += 1

        self.app = app

    def respawn(self, app):
        if self.respawning:
            self.x = 0
            self.y = randInRange(app.height/6, app.height*(5/6))
            self.angle = randInRange(math.radians(-15), math.radians(15))

            self.velocity = app.width / randInRange(2, 4) # Across the screen in 2-4 seconds
            self.radius = randInRange(5, 15)

            self.respawning = False

    def move(self):
        self.x += math.cos(self.angle)*(self.velocity/self.app.stepsPerSecond)
        self.y += math.sin(self.angle)*(self.velocity/self.app.stepsPerSecond)

        if not self.respawning and self.x - self.radius > self.app.width or self.y - self.radius > self.app.height:
            self.respawning = True
            Timer(self.app, randInRange(0.5, 3), 1, self.respawn)
            
    def draw(self):
        drawStar(self.x, self.y, 20, 4, fill='white', opacity=app.opacityFactor)

        lineX = self.x - math.cos(self.angle)*(self.velocity/self.app.stepsPerSecond)*self.radius
        lineY = self.y - math.sin(self.angle)*(self.velocity/self.app.stepsPerSecond)*self.radius

        drawLine(self.x, self.y, lineX, lineY, fill='white', opacity=app.opacityFactor)

    @staticmethod
    def spawn(app):
        app.shootingStars.append(ShootingStar(app))

    @staticmethod
    def generate(app, amount):
        if amount < 1: return

        for i in range(1, amount + 1):
            Timer(app, randInRange(i - 1, i), 1, ShootingStar.spawn)

class BackgroundStar():
    def __init__(self, app):
        self.x = randInRange(0, app.width)
        self.y = randInRange(0, app.height)
        self.radius = randInRange(5, 10)
        self.opacity = randInRange(50, 100)

    def draw(self):
        drawStar(self.x, self.y, self.radius, 5, fill='white', opacity=self.opacity)

    @staticmethod
    def spawn(app):
        app.backgroundStars.append(BackgroundStar(app))

    @staticmethod
    def generate(app, amount):
        if amount < 1: return

        for i in range(1, amount + 1):
            BackgroundStar.spawn(app)

def drawBackground(app):
    drawRect(0, 0, app.width, app.height, fill='black')

    for star in app.shootingStars:
        star.draw()

    for star in app.backgroundStars:
        star.draw()