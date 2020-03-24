import random
from block import *
def generate_terrain(x = 0 , y = 0, cell = 0, removal = 0):
    """if cell[6] == 1 or cell[6] == 4:
        if y > -5:
            return 4
    """
    if removal:
        block = Block(0)
        return block
    if y < 0:
        block = Block(0)
        return block
    elif y == 0:
        block = Block(1)
        return block
    elif y > 0:
        block = Block(5)
        return block
