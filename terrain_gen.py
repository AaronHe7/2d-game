import random, math
from block import *
from assets import *

seed = 2324

class Terrain:
    def __init__(self):
        self.surface_level = 0
        self.blocks_since_cave = 0
        self.bedrock_level = -100
    def generate(self, x, y):
        random.seed((seed + 13441 * x + 13331 * y) % (10**9+7))
        if (x in tilemap and y in tilemap[x]):
            return
        surface_level = self.surface_level
        if y > surface_level: # air above surface level
            block = blocks[0]
        elif y == surface_level: # grass at surface level
            block = blocks['grass']
        elif surface_level - 3 < y < surface_level: # dirt below suface level
            block = blocks['dirt']
        elif self.bedrock_level < y <= surface_level - 3: # stone starts at 3 below surface
            p = (-y + surface_level - 3)/10 + 0.3
            block = blocks['stone']
            if random.uniform(0, 1) < p:
                if 3 < y <= -10:
                    block = blocks['stone']
                elif -80 <= y < -10:
                    if random.randint(0, 50) == 1:
                        block = blocks['coal_ore']
                    elif random.randint(0, 150) == 1:
                        block = blocks['iron_ore']
                    else:
                        block = blocks['stone']
                elif -99 <= y < -80:
                    if random.randint(0, 250) == 1:
                        block = blocks['bloodstone_ore']
                    elif random.randint(0, 300) == 1:
                        block = blocks['diamond_ore']
                    else:
                        block = blocks['stone']
            else:
                block = blocks['dirt']
        elif y == self.bedrock_level: # bedrock
            block = blocks['bedrock']
        elif y < self.bedrock_level: # void
            block = blocks[0]

        tilemap[x][y] = block.get_copy()

        # Generate Beach at Random
        if y == surface_level and random.randint(0, 45) == 0:
            beach = self.generate_beach(x, y, random.randint(4, 10), random.randint(1,4))
            for x in beach:
                if x not in tilemap:
                    tilemap[x] = {}
                for y in beach[x]:
                    tilemap[x][y] = beach[x][y].get_copy()

        # Generate tree at random
        if y == surface_level and random.randint(0, 15) == 0:
            tree = self.generate_tree(x, y + 1, random.randint(6, 11))
            for x in tree:
                if x not in tilemap:
                    tilemap[x] = {}
                for y in tree[x]:
                    tilemap[x][y] = tree[x][y].get_copy()
                    tilemap[x][y].pass_through = True

        # Generate cave at random
        p_cave = (self.blocks_since_cave/300) ** 3
        if y == surface_level and random.uniform(0, 1) < p_cave:
            depth = random.randint(10, 20)
            width = random.randint(5, 6)
            self.blocks_since_cave = 0
            # Generate a cave with angle in the interval [215, 235] or [305, 325]
            if random.randint(0, 1) == 1:
                angle = random.uniform(215, 235)
            else:
                angle = random.uniform(305, 325)

            cave = self.generate_cave(x, y + 2, angle, depth, width)
            for x in cave:
                if x not in tilemap:
                    tilemap[x] = {}
                for y in cave[x]:
                    tilemap[x][y] = cave[x][y].get_copy()
        elif y == 0:
            self.blocks_since_cave += 1

        # Increase or decrease surface level at random
        if y == surface_level + 1 and random.randint(0, 20) == 0:
            if random.randint(0, 1) == 1:
                surface_level += 1
            else:
                surface_level -= 1

    def generate_beach(self, x, y, length, height):
        beach = {}
        for i in range(length):
            if x + i not in beach:
                beach[x + i] = {}
            for j in range(height):
                if j < height - 1:
                    if i == 0:
                        beach[x + i][y - j] = blocks['sand']
                    elif i == length - 1:
                        beach[x + i][y - j] = blocks['sand']
                    else:
                        beach[x + i][y - j] = blocks['water']
                else:
                    beach[x + i][y - j] = blocks['sand']
        return beach
        
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
                            
                    tree[x + j][y + i] = blocks['leaves']
                    tree[x - j][y + i] = blocks['leaves']
                    
        # Make sure tree doesn't overlap other structures
        for x in tree:
            for y in tree[x]:
                if tilemap.get(x, {}).get(y, False) and tilemap[x][y].id != 0:
                    return {}
        return tree

    def generate_cave(self, x, y, angle_degrees, depth, width, recursion_depth = 0):
        ang = angle_degrees * math.pi/180
        cave = {}
        surface_level = self.surface_level

        final_x = 0
        final_y = 0
        for i in range(depth * 8):
            length = i/8
            # angle offset added for more randomness
            ang_offset = random.uniform(-1, 1) * math.pi/180
            ang += ang_offset
            perp_ang = ang + math.pi/2
            current_x = x + math.floor(length * math.cos(ang))
            current_y = y + math.floor(length * math.sin(ang))

            final_x = current_x
            final_y = current_y
            
            for j in range(width * 4):
                dist_from_line = j/8
                x1 = math.floor(current_x - dist_from_line * math.cos(perp_ang))
                y1 = math.floor(current_y - dist_from_line * math.sin(perp_ang))
                x2 = math.floor(current_x + dist_from_line * math.cos(perp_ang))
                y2 = math.floor(current_y + dist_from_line * math.sin(perp_ang))
                if x1 not in cave:
                    cave[x1] = {}
                if x2 not in cave:
                    cave[x2] = {}
                if y1 <= surface_level:
                    cave[x1][y1] = blocks[0]
                if y2 <= surface_level:
                    cave[x2][y2] = blocks[0]
    
        p = 2 ** (-recursion_depth/2)
        if (random.uniform(0, 1) < p):
            branch1_ang = random.uniform(215, 235)
            branch1 = self.generate_cave(final_x, final_y, branch1_ang, depth + 5, width, recursion_depth + 1)
            
            for x in branch1:
                if x not in cave:
                    cave[x] = {}
                for y in branch1[x]:
                    cave[x][y] = branch1[x][y]

            # 1/5 chance to branch off twice
            if (random.randint(0, 4) == 0):
                branch2_ang = random.uniform(305, 325)
                branch2 = self.generate_cave(final_x, final_y, branch2_ang, depth + 5, width, recursion_depth + 1) 
                for x in branch2:
                    if x not in cave:
                        cave[x] = {}
                    for y in branch2[x]:
                        cave[x][y] = branch2[x][y]
        return cave
terrain = Terrain()
        
