from modules.patterns import PATTERNS
from modules.utilities import randInRange
import modules.enemy as enemy

import random

filtedPatterns = [key for key in PATTERNS.keys() if key != 'heart']

def getRandomPatterns(amount, replacement=False):
    if replacement:
        return random.choices(list(filtedPatterns), k=amount)
    else:
        return random.sample(list(filtedPatterns), k=amount)        

class BaseCombo():
    def spawn(self, app):
        enemy.Enemy(app, self.pattern())

class sameCombo(BaseCombo): # 1 pattern repeated
    def __init__(self, size=2):
        self.size = size

    def pattern(self):
        return getRandomPatterns(1)*self.size

class randomCombo(BaseCombo): # Random different patterns
    def __init__(self, size=2):
        self.size = size

    def pattern(self):
        return getRandomPatterns(self.size, replacement=False)

class repeatedCombo(BaseCombo): # Random different patterns but a randomly selected pattern is repeated {size} times
    def __init__(self, patterns=2, timesRepeated=2):
        self.patterns = patterns
        self.timesRepeated = timesRepeated

    def pattern(self):
        L = randomCombo(size=self.patterns).pattern()
        
        randIndex = round(randInRange(0, len(L) - 1))

        for i in range(self.timesRepeated):
            L.insert(randIndex, L[randIndex])

        return L
        