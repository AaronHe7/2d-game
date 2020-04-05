import random, math
from block import *
from assets import *

class Terrain:
    def __init__(self):
        self.surface_level = 0
    def generate(self, x, y):
        surface_level = self.surface_level
        if y > surface_level: # air above surface level
            block = blocks[0]
        elif y == surface_level: # grass at surface level
            block = blocks[1]
        elif surface_level - 3 < y < surface_level: # dirt below suface level
            block = blocks[2]
        elif surface_level - 60 < y <= surface_level - 3: # stone starts at 3 below surface
            p = (-y + surface_level - 3)/10 + 0.3
            if random.uniform(0, 1) < p:
                block = blocks[5]
            else:
                block = blocks[2]
        elif y == surface_level - 60: # bedrock
            block = blocks[7]
        elif y < surface_level - 60: # void
            block = blocks[0]


        tilemap[x][y] = block.get_copy()

        # Generate tree at random
        if y == surface_level and random.randint(0, 15) == 0:
            tree = self.generate_tree(x, y + 1, random.randint(6, 11))
            for x in tree:
                if x not in tilemap:
                    tilemap[x] = {}
                for y in tree[x]:
                    tilemap[x][y] = tree[x][y].get_copy()
                    tilemap[x][y].pass_through = True

        # Increase or decrease surface level at random
        if y == surface_level + 1 and random.randint(0, 20) == 0:
            if random.randint(0, 1) == 1:
                surface_level += 1
            else:
                surface_level -= 1
        
    def generate_tree(self, x, y, height):
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

    def generate_cave(self, x, y, blocks_removed):
            pass
