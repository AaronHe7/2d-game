import math

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
        top = Coordinate(self.x + self.w/2, self.y, self.tilemap)
        left = Coordinate(self.x, self.y + self.h/2, self.tilemap)
        right = Coordinate(self.x + self.w, self.y + self.h/2, self.tilemap)
        bottom = Coordinate(self.x + self.w/2, self.y + self.h + 1, self.tilemap)

        if top.get_tile()[0] != 0:
            self.vy = 0
            self.y += 5
        if left.get_tile()[0] != 0:
            self.vx = 0
            self.x += 5
        if bottom.get_tile()[0] != 0:
            self.vy = 0
            self.ay = 0
            self.on_ground = True
        if bottom.get_tile()[0] == 0:
            self.ay = -1
        if right.get_tile()[0] != 0:
            self.vx = 0
            self.x -= 5

        self.x += self.vx
        self.y -= self.vy
        self.vy += self.ay



# Helper class
class Coordinate:
    def __init__(self, x, y, tilemap):
        self.x = x
        self.y = y
        self.tilemap = tilemap
    def get_tile(self):
        row = math.floor(self.y/80)
        col = math.floor(self.x/80)
        if row < 0 or row >= len(self.tilemap) or col < 0 or col >= len(self.tilemap[0]):
            return 1
        return [self.tilemap[math.floor(self.y/80)][math.floor(self.x/80)],[row,col]]
