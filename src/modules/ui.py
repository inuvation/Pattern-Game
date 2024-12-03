from cmu_graphics import *
import math

from modules.utilities import randInRange, clamp

def drawFrame(app, x, y, w, h, depth=8, opacity=100, invertColor=False, fill=None, secondaryFill=None, text=''):
    if fill == None: fill = app.primaryColor
    if secondaryFill == None: secondaryFill = app.secondaryColor

    drawPolygon(x, y + 1, x - depth, y + depth, x - depth, y + depth + h, x + w - depth, y + depth + h, x + w - 1, y + h, x + w - 1, y + 1, fill=(invertColor and fill or secondaryFill), opacity=opacity)

    drawRect(x, y, w, h, fill=gradient(invertColor and fill or secondaryFill, invertColor and secondaryFill or fill, start='center'), opacity=opacity)
    drawRect(x + app.margins, y + app.margins, w - app.margins*2, h - app.margins*2, fill=(invertColor and secondaryFill or fill), border=(invertColor and fill or secondaryFill), opacity=opacity)

    drawLabel(text, x + w/2, y + h/2, size = h/2, fill=app.textColor, font=app.font, border='black', opacity=opacity)

def drawHeart(app, x, y, w, h):
    circleWidth = w/2
    ovalWidth = circleWidth + app.margins
    ovalHeight = h/2

    drawOval(x + circleWidth/2, y + ovalHeight/2, ovalWidth, ovalHeight, fill='red') # Top left circle
    drawOval(x + circleWidth*(3/2) - app.margins/2, y + ovalHeight/2, ovalWidth, ovalHeight, fill='red') # Top right circle

    bottomMiddleX, bottomMiddleY = (ovalWidth/2)*math.cos(math.radians(135)), (ovalHeight/2)*math.sin(math.radians(135))

    drawPolygon(x + circleWidth/2 + bottomMiddleX, y + ovalHeight/2 + bottomMiddleY, x + circleWidth*(3/2) - app.margins/2 - bottomMiddleX, y + ovalHeight/2 + bottomMiddleY, x + circleWidth, y + h, fill='red') # Bottom half polygon connecting the bottom edge quadrants of circles

    drawCircle(x + circleWidth, y + ovalHeight*(2/3), ovalHeight/3, fill='red') # Covering hole in center

    drawOval(x + circleWidth/4, y + ovalHeight/4, ovalWidth/2.5, ovalHeight/7, fill='pink', rotateAngle=-45) # Shiny part on top left

def generateCraters(radius, amount):
    craters = []

    pieAngle = 360/amount

    for i in range(amount):
        craters.append((randInRange(radius/8, radius/4), randInRange(radius/4, radius*(3/4)), math.radians(i*pieAngle)))

    return craters

def generateLandMasses(x, y, radius, amount):
    landMasses = []

    pieAngle = 360 / amount
    initialOffset = randInRange(0, pieAngle)

    for i in range(amount):
        posR = randInRange(radius/4, radius*(2/3))
        posTheta = math.radians(initialOffset + i*pieAngle)
        polygon = []

        numSegmentsInLandMass = pythonRound(randInRange(4, 7))

        for j in range(numSegmentsInLandMass):
            landMassAngle = 360 / numSegmentsInLandMass

            cx, cy = posR*math.cos(posTheta), posR*math.sin(posTheta)
            segR = randInRange(posR*(2/5), posR*(3/5))
            segTheta = math.radians(j*landMassAngle)

            polygon.append(x + cx + segR*math.cos(segTheta)) # X Coordinate of segment in land mass
            polygon.append(y + cy + segR*math.sin(segTheta)) # Y Coordinate of segment in land mass

        landMasses.append(polygon)
            
    return landMasses

def drawEarth(landMasses, x, y, radius, fill='blue', secondaryFill='green'):
    drawCircle(x, y, radius, fill=fill)

    for polygon in landMasses:
        drawPolygon(*polygon, fill=secondaryFill)
 
def drawAsteroid(craters, x, y, radius, fill='dimGray', secondaryFill='gray'):
    drawCircle(x, y, radius, fill=fill, border=secondaryFill)

    for (size, posR, posTheta) in craters:
        drawCircle(x + posR*math.cos(posTheta), y + posR*math.sin(posTheta), size, fill=secondaryFill)

def animate(alter, increase, scaleBy, lower, upper):
    if increase:
        alter = clamp(alter + scaleBy, lower, upper)
    else:
        alter = clamp(alter - scaleBy, lower, upper)

    return alter

class Button():
    selectedInGroup = dict()

    def __init__(self, app, text, x, y, w, h, onClick, depth=12, group=None, fill=None, secondaryFill=None):
        self.app = app
        self.text = text
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.onClick = onClick
        self.depth = depth

        self.hovered = False
        self.hoverFactor = 0

        self.pressed = False
        self.scaleFactor = 1

        self.app.buttons.append(self)

        self.group = group

        self.fill = fill
        self.secondaryFill = secondaryFill

        self.opacity = 100

        self.visible = True

        Button.selectedInGroup[group] = Button.selectedInGroup.get(group, None)

    def checkMouseInBounds(self, x, y):
        if not self.visible: return

        if x >= self.x and x <= self.x + self.w and y >= self.y and y <= self.y + self.h:
            self.hovered = True
        else:
            self.hovered = False

    def checkClicked(self):
        if not self.visible: return
        if not self.hovered: return

        if self.group:
            Button.selectedInGroup[self.group] = self

        self.onClick(self.app)

        self.pressed = True

    def draw(self):
        if not self.visible:
            return

        drawFrame(self.app, self.x - self.hoverFactor, self.y + self.hoverFactor, self.w, self.h, depth=(self.depth - self.hoverFactor), fill=self.fill, secondaryFill=self.secondaryFill, opacity=self.opacity)

        selected = Button.selectedInGroup[self.group] == self

        drawLabel(self.text, self.x + self.w/2 - self.hoverFactor, self.y + self.h/2 + self.hoverFactor, size=(self.h/2)*self.scaleFactor, font=self.app.font, fill=(self.group and (selected and 'white' or 'gray') or self.app.textColor), border=(selected and 'black' or None), opacity=self.opacity)

    def hoverEffect(self):
        self.hoverFactor = animate(self.hoverFactor, self.hovered, 2, 0, self.depth)
        self.scaleFactor = animate(self.scaleFactor, self.pressed, -0.05, 0.9, 1)

def redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill='black')

    drawFrame(app, app.margins, app.margins, 300, 200)
    drawHeart(app, 300 + app.margins, app.margins, 200, 200)
    drawAsteroid(app.craters, 300 + app.margins + 300, app.margins + 100, 100)
    drawEarth(app.landMasses, 300 + app.margins + 600, app.margins + 100, 100)

    for button in app.buttons:
        button.draw()

def onMousePress(app, x, y):
    for button in app.buttons:
        button.checkClicked()

def onMouseRelease(app, x, y):
    for button in app.buttons:
        button.pressed = False

def onMouseMove(app, x, y):
    for button in app.buttons:
        button.checkMouseInBounds(x, y)

def onStep(app):
    for button in app.buttons:
        button.hoverEffect()

def onAppStart(app):
    # Theme
    app.font = 'montserrat'
    app.primaryColor = rgb(32, 0, 54)
    app.secondaryColor = rgb(210, 142, 255)
    app.textColor = 'white'
    app.margins = 8

    app.opacityFactor = 100

    app.buttons = []
    Button(app, "Button", app.width/2, app.height/2, app.width/5, app.height/8, lambda _: print('clicked!'))

    app.craters = generateCraters(100, 5)
    app.landMasses = generateLandMasses(300 + app.margins + 600, app.margins + 100, 100, 4)

def main():
    app = runApp(width=1208, height=720)

if __name__ == '__main__':
   main()