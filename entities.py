entities_group = []
from assets import *

class Item:
    def __init__(self, id, location):
        self.id = id
        self.location = location
        self.amount = 1
        types = ['pickaxe', 'pickaxe', 'pickaxe', 'pickaxe']
        if self.id <= 100:
            self.hit_multiplier = 0.075
            self.type = 'block'
        else:
            self.hit_multiplier = item_hit_multipliers[id]
            self.type = types[id]
