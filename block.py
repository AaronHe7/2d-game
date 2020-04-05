import pygame, copy 

class Block:
    def __init__(self, id, name, durability):
        self.id = id
        self.pass_through = False
        self.name = name
        required_tools = [0, 3, 3, 1, 0, 2, 2, 0]
        # 0 is none, 1 is pickaxe, 2 is axe, 3 is shovel, 4 is sword
        self.max_durability = durability
        self.durability = self.max_durability
        self.required_tool = required_tools[id]
        self.frames_since_last_touched = 0
        self.destroy_rate = 10000.075
    def reduce_durability(self, multiplier = 1):
        self.durability -= self.destroy_rate * multiplier
        self.durability = max(self.durability, 0)
        if self.durability == 0:
            pass
            # drop block here
            #self.delete()
    def delete(self):
        self.id = 0
        self.pass_through = True
    def get_copy(self):
        return copy.deepcopy(self)
