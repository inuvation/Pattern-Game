from modules.patterns import PATTERNS
import random

def getRandomPatterns(amount, replacement=False):
    if replacement:
        return random.choices(list(PATTERNS.keys()), k=amount)
    else:
        return random.sample(list(PATTERNS.keys()), k=amount)        

def combo():
    return getRandomPatterns(3, replacement=False)
