import pygame

class Block:
    def __init__(self, id, name):
        self.id = id
        self.pass_through = False
        self.name = name
        durabilities = [0, 5, 5, 10, 3, 15]
        self.max_durability = durabilities[id]
        self.durability = self.max_durability
        
