entities_group = []
from assets import *

class Item:
    def __init__(self, id, location = [-tilesize, -tilesize], amount = 1):
        self.id = id #the id of the item
        self.location = location #the location of the item if it is an entity
        self.amount = amount #the amount of the item
        self.velx = 0 #used for entity drops
        self.vely = 0 #etc
        if self.id <= 100: #if the item is a block, it has no tooltype and has a hit multiplier of 1
            self.hit_multiplier = 1
            self.type = 'block'
            self.tooltype = 'none'
        else:
            self.hit_multiplier = item_hit_multipliers[id] #if the item is not a block, grant it the respectful hit multiplier
            self.tooltype = item_tooltypes[id] #grant the item the specified tooltype
            self.type = 'item' #determine whether or not the item is a block or an item
