import math
from terrain_gen import *
from assets import *

class Player:
    def __init__(self, x, y, tilemap):
        self.tilemap = tilemap
        # height and width
        self.h = 2
        self.w = 1
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
            self.y = bottom.get_x_y()['y'] - self.h
            self.ay = 0
            self.vy = 0
            self.on_ground = True

        
class Coordinate:
    def __init__(self, x, y, tilemap):
        self.x = x
        self.y = y
        self.tilemap = tilemap
    def get_tile(self):
        x = math.floor(self.x)
        y = math.floor(self.y)
        
        if x not in self.tilemap or y not in self.tilemap[x]:
            return generate_terrain(x, y)
        return self.tilemap[x][y]
    def get_x_y(self):
        x = math.floor(self.x)
        y = math.floor(self.y)
        
        return {'x': x, 'y': y}



