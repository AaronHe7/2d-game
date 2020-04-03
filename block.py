import pygame, copy

class Block:
    def __init__(self, id, name):
        self.id = id
        self.pass_through = False
        self.name = name
        durabilities = [0, 5, 5, 10, 3, 20]
        required_tools = [0, 3, 3, 1, 0, 2]
        # 0 is none, 1 is pickaxe, 2 is axe, 3 is shovel, 4 is sword
        self.max_durability = durabilities[id]
        self.durability = self.max_durability
        self.required_tool = required_tools[id]
        self.frames_since_last_touched = 0
                
    def get_copy(self):
        return copy.deepcopy(self)
