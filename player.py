import math
from assets import *

class Player:
    def __init__(self, x, y, tilemap):
        self.tilemap = tilemap
        # height and width
        self.h = 160
        self.w = 80
        self.x = x
        self.y = y
        # Velocity
        self.vx = 0
        self.vy = 0
        # Acceleration
        self.ay = 0
        self.on_ground = False
    def update_position(self):
        self.x += self.vx
        self.y -= self.vy
        self.vy += self.ay
        
        top = Coordinate(self.x + self.w/2, self.y, self.tilemap)
        left = Coordinate(self.x, self.y + self.h/2, self.tilemap)
        right = Coordinate(self.x + self.w, self.y + self.h/2, self.tilemap)
        bottom = Coordinate(self.x + self.w/2, self.y + self.h + 1, self.tilemap)

        if top.get_tile() != 0:
            self.vy = 0
            self.y += player_speed
        if left.get_tile() != 0:
            self.vx = 0
            self.x += player_speed
        if bottom.get_tile() != 0:
            if self.on_ground:
                self.vy = 0
            self.on_ground = True
            self.ay = 0
            self.y = (bottom.get_row_col()['r'] - player.h/tilesize) * 80
        if bottom.get_tile() == 0:
            self.ay = gravity
            self.on_ground = False
        if right.get_tile() != 0:
            self.vx = 0
            self.x -= player_speed

        



# Helper class
class Coordinate:
    def __init__(self, x, y, tilemap):
        self.x = x
        self.y = y
        self.tilemap = tilemap
    def get_tile(self):
        row = math.floor(self.y/tilesize)
        col = math.floor(self.x/tilesize)
        if row < 0 or row >= len(self.tilemap) or col < 0 or col >= len(self.tilemap[0]):
            return 1
        return self.tilemap[int(self.y//tilesize)][int(self.x//tilesize)]
    def get_row_col(self):
        row = math.floor(self.y/tilesize)
        col = math.floor(self.x/tilesize)
        return {'r': row, 'c': col}
        
