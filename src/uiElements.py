from cmu_graphics import *
from modules.utilities import randInRange
import math

def drawFrame(app, x, y, w, h, depth=8, opacity=100, invertColor=False, text=''):
    drawPolygon(x, y + 1, x - depth, y + depth, x - depth, y + depth + h, x + w - depth, y + depth + h, x + w - 1, y + h, x + w - 1, y + 1, fill=(invertColor and app.primaryColor or app.secondaryColor), opacity=opacity)

    drawRect(x, y, w, h, fill=gradient(invertColor and rgb(255, 255, 255) or rgb(0,0,0), invertColor and app.secondaryColor or app.primaryColor, start='center'), opacity=opacity)
    drawRect(x + app.margins, y + app.margins, w - app.margins*2, h - app.margins*2, fill=(invertColor and app.secondaryColor or app.primaryColor), border=(invertColor and app.primaryColor or app.secondaryColor), opacity=opacity)

    drawLabel(text, x + w/2, y + h/2, size = h/2, fill=app.textColor, font=app.font, border=(invertColor and 'black' or 'white'), opacity=opacity)

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

def redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill='black')

    drawFrame(app, app.margins, app.margins, 300, 200)
    drawHeart(app, 300 + app.margins, app.margins, 200, 200)
    drawAsteroid(app.craters, 300 + app.margins + 300, app.margins + 100, 100)
    drawEarth(app.landMasses, 300 + app.margins + 600, app.margins + 100, 100)

def onAppStart(app):
    # Theme
    app.font = 'montserrat'
    app.primaryColor = rgb(32, 0, 54)
    app.secondaryColor = rgb(210, 142, 255)
    app.textColor = 'white'
    app.margins = 8

    app.craters = generateCraters(100, 5)
    app.landMasses = generateLandMasses(300 + app.margins + 600, app.margins + 100, 100, 4)

def main():
    app = runApp(width=1208, height=720)

if __name__ == '__main__':
   main()