entities_group = []
from assets import *

class Item:
    def __init__(self, id, location = [-tilesize, -tilesize], amount = 1):
        self.id = id
        self.location = location
        self.amount = amount
        self.velx = 0
        self.vely = 0
        if self.id <= 100:
            self.hit_multiplier = 0.075
            self.type = 'block'
            self.tooltype = 'none'
        else:
            self.hit_multiplier = item_hit_multipliers[id]
            self.tooltype = item_tooltypes[id]
            self.type = 'item'
