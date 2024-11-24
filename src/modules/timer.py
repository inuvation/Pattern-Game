class Timer():
    timers = set()
    defers = []

    nextId = 0

    def __init__(self, app, length, looping, callback):
        self.length = length

        self.endTick = app.tick + length*app.stepsPerSecond

        self.looping = looping

        self.callback = callback

        self.id = Timer.nextId
        Timer.nextId += 1

        Timer.timers.add(self)

    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return isinstance(other, Timer) and self.id == other.id
    
    def destroy(self):
        Timer.timers.remove(self)

    def tick(self, app):
        if app.tick >= self.endTick:
            self.callback(app)

            if self.looping:
                self.endTick = app.tick + self.length*app.stepsPerSecond
            else:
                Timer.defer(self.destroy)

    @staticmethod
    def defer(function):
        Timer.defers.append(function)

    @staticmethod
    def runDeffered():
        for function in Timer.defers:
            function()

        Timer.defers = []