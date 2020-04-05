import random, math
from block import *
from assets import *

def generate_terrain(x = 0, y = 0, cell = 0):
    """if cell[6] == 1 or cell[6] == 4:
        if y > -5:
            return 4
    """
    if y > 0:
        block = blocks[0]
    elif y == 0:
        block = blocks[1]
    elif y <= -5:
        block = blocks[5]
    elif -5 < y < 0:
        block = blocks[2]

    tilemap[x][y] = block.get_copy()

    # Generate tree at random
    if y == 1 and random.randint(0, 15) == 0:
        tree = generate_tree(x, y, random.randint(6, 11))
        for x in tree:
            if x not in tilemap:
                tilemap[x] = {}
            for y in tree[x]:
                tilemap[x][y] = tree[x][y].get_copy()
                tilemap[x][y].pass_through = True

def generate_cave(x, y, size):
    cave = {}
    for i in range(size):
        if x not in cave:
            tree[x] = {}

def generate_tree(x, y, height):
    tree = {}
    for i in range(height):
        if x not in tree:
            tree[x] = {}
            
        # Tree trunk for first half of tree
        if i < height/2:
            tree[x][y + i] = blocks[3]
        else:
            type = 'triangle'
            if type == 'semicircle':
                leaf_length = math.ceil(height * math.sqrt(1 - ((i * 2/height - 1) ** 2)))//2
            elif type == 'triangle':
                leaf_length = height - i
            for j in range(leaf_length + 1):
                if x + j not in tree:
                    tree[x + j] = {}
                if x - j not in tree:
                    tree[x - j] = {}
                        
                tree[x + j][y + i] = blocks[4]
                tree[x - j][y + i] = blocks[4]
                
    # Make sure tree doesn't overlap other structures
    for x in tree:
        for y in tree[x]:
            if tilemap.get(x, {}).get(y, False) and tilemap[x][y].id != 0:
                return {}
    return tree

