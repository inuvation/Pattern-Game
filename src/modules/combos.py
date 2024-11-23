from modules.patterns import PATTERNS
import random

# def comboWeights():
#     # Stage: [Probability of Difficulty N Combo, ...]
#     return [
#         [0.7, 0.3, 0], # Stage 1
#         [0.3, 0.5, 0.2], # Stage 2
#         [0, 0.3, 0.7]  # Stage 3
#     ]

# def loadCombos():
#     # Difficulty N Combos
#     return [
#         [], # 0000000 1 Combos
#         [], # Difficulty 2 Combos
#         []  # Difficulty 3 Combos
#     ]

def getRandomPatterns(amount, replacement=False):
    if replacement:
        return random.choices(list(PATTERNS.keys()), k=amount)
    else:
        return random.sample(list(PATTERNS.keys()), k=amount)        

def combo():
    return getRandomPatterns(3, replacement=False)

# class RandomCombo(Combo):
#     def __init__(self, size):
        


# class RepeatingCombo(Combo):
#     def __init__():
#         pass