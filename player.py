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
        self.on_ground = False
        points_touching_ground = 0
        
        # Number of hitbox points on each side of the character
        hitbox_points = 20
        for i in range(1, hitbox_points):
            # The coordinates that vary as i varies
            x_variation_coord = self.x + i * self.w/hitbox_points
            y_variation_coord = self.y + i * self.h/hitbox_points
            
            top = Coordinate(x_variation_coord, self.y, self.tilemap)
            bottom = Coordinate(x_variation_coord, self.y + self.h, self.tilemap)
            left = Coordinate(self.x, y_variation_coord, self.tilemap)
            right = Coordinate(self.x + self.w - 1, y_variation_coord, self.tilemap)
            
            if top.get_tile() != 0:
                self.vy = 0
                self.y += player_speed
            if left.get_tile() != 0:
                self.vx = 0
                self.x += player_speed
            if bottom.get_tile() != 0:                   
                points_touching_ground += 1
            if right.get_tile() != 0:
                self.vx = 0
                self.x -= player_speed

        if not self.on_ground:
            self.ay = gravity
            
        # Player can jump again only if more than 1/5 of the player is touching the ground
        if points_touching_ground >= hitbox_points/5:
            self.y = (bottom.get_row_col()['r'] - self.h/tilesize) * tilesize
            self.ay = 0
            self.vy = 0
            self.on_ground = True

        



# Helper class
class Coordinate:
    def __init__(self, x, y, tilemap):
        self.x = x
        self.y = y
        self.tilemap = tilemap
    def get_tile(self):
        row = self.y//tilesize
        col = self.x//tilesize
        if row < 0 or row >= len(self.tilemap) or col < 0 or col >= len(self.tilemap[0]):
            return 1
        return self.tilemap[int(self.y//tilesize)][int(self.x//tilesize)]
    def get_row_col(self):
        row = self.y//tilesize
        col = self.x//tilesize
        return {'r': row, 'c': col}
        
