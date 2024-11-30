from cmu_graphics import *

def drawFrame(app, x, y, w, h, invertColor=False, text=''):
    drawRect(x, y, w, h, fill=(invertColor and app.secondaryColor or app.primaryColor))
    drawRect(x + app.margins, y + app.margins, w - app.margins*2, h - app.margins*2, fill=None, border=(invertColor and app.primaryColor or app.secondaryColor))

    drawLabel(text, x + w/2, y + h/2, size = h/2, fill=app.textColor, font=app.font)

def drawHeart(app, x, y, w, h):
    drawRect(x, y, w, h, fill='white')

def redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill='black')
    drawFrame(app, app.margins, app.margins, 300, 200)

    drawHeart(app, 300 + app.margins, app.margins, 200, 200)

def onAppStart(app):
    # Theme
    app.font = 'montserrat'
    app.primaryColor = rgb(32, 0, 54)
    app.secondaryColor = rgb(210, 142, 255)
    app.textColor = 'white'
    app.margins = 8


def main():
    app = runApp(width=1208, height=720)

if __name__ == '__main__':
   main()