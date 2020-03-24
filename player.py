import math
from assets import *
from terrain_gen import *

class Player:
    def __init__(self, x, y, tilemap):
        self.tilemap = tilemap
        # height and width
        self.hp = 20
        self.maxhp = 20
        self.h = 1.8
        self.w = 0.85
        self.x = x
        self.y = y
        # Velocity
        self.vx = 0
        self.vy = 0
        self.vxmultiplier = 1
        # Acceleration
        self.ay = 0
        self.on_ground = False
        # Other Variables for Animation
        self.direction = [0, 0]
        self.handstate = 0
        # Possession
        self.inventory = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    def update_position(self):
        self.vx *= self.vxmultiplier
        self.x += self.vx
        self.y -= self.vy
        self.vy += self.ay
        self.on_ground = False
        points_touching_ground = 0

        # Number of hitbox points on each side of the character
        hitbox_points = 20
        for i in range(3, hitbox_points-3):
            # The coordinates that vary as i varies
            x_variation_coord = math.floor(self.x + i * self.w/hitbox_points)
            y_variation_coord = math.floor(self.y + i * self.h/hitbox_points)

            left = [math.floor(self.x + 1/tilesize), y_variation_coord]
            right = [math.floor(self.x + self.w - 1/tilesize), y_variation_coord]
            top = [x_variation_coord, math.floor(self.y)]
            bottom = [x_variation_coord, math.floor(self.y + self.h)]

            if tilemap[top[0]][top[1]] != 0:
                self.vy = 0
                self.y += player_speed
            if tilemap[left[0]][left[1]] != 0:
                self.x -= self.vx
                self.vx = 0

            if tilemap[right[0]][right[1]] != 0:
                self.x -= self.vx
                self.vx = 0

            if tilemap[bottom[0]][bottom[1]] != 0:
                points_touching_ground += 1

        if not self.on_ground:
            self.ay = gravity

        # Player can jump again only if more than 1/10 of the player is touching the ground
        if points_touching_ground >= hitbox_points/10:
            if self.vy <= -0.5:
                self.hp -= (math.floor(-12 * self.vy - 5))
                self.vy = 0
            self.y = bottom[1] - self.h
            self.ay = 0
            self.vy = 0
            self.on_ground = True
            self.vx /= self.vxmultiplier
    






  
