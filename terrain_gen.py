import random, copy
from block import *
from assets import *

def generate_terrain(x = 0 , y = 0, cell = 0, removal = 0):
    y = -y
    """if cell[6] == 1 or cell[6] == 4:
        if y > -5:
            return 4
    """
    if removal:
        block = blocks[0]
    if y > 0:
        block = blocks[0]
    elif y == 0:
        block = blocks[1]
    elif y <= -5:
        block = blocks[5]
    elif -5 < y < 0:
        block = blocks[2]

    return copy.deepcopy(block)
    
