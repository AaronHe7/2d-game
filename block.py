import pygame, copy 

class Block:
    def __init__(self, id, name, durability, required_tool, exact_tool_required = False, pass_through = False, dropid = 'self', use = None):
        self.id = id
        if dropid == 'self':
            self.dropid = id
        else:
            self.dropid = dropid
        self.pass_through = pass_through
        self.name = name
        # 0 is none, 1 is pickaxe, 2 is axe, 3 is shovel, 4 is sword, 5 is hammer
        self.max_durability = durability
        self.durability = self.max_durability
        self.required_tool = required_tool
        self.frames_since_last_touched = 0 #the number of frames since the player has tried to break this block
        self.destroy_rate = 0.075
        self.exact_tool_required = exact_tool_required
        self.nbt_tags = {}
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
