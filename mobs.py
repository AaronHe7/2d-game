from player import player
from assets import *

class Creature:
  def __init__(self, x, y, tilemap):
        self.x = x
        self.y = y
        self.h = 1.8
        self.w = 0.85
        self.vx = 0
        self.vy = 0
        self.ay = 0
        self.hp = 20

  def update_position(self):
      self.x += self.vx
      self.y += self.vy
      self.vy += self.ay
      self.on_ground = False
      points_touching_ground = 0
      points_touching_wall = 0

      # Number of hitbox points on each side of the character
      hitbox_points = 20
      for i in range(3, hitbox_points):
          # The coordinates that vary as i varies
          x_variation_coord = math.floor(self.x + i * self.w/hitbox_points)
          y_variation_coord = math.ceil(self.y - i * self.h/hitbox_points)

          left = [math.floor(self.x + 1/tilesize), y_variation_coord]
          right = [math.floor(self.x + self.w - 1/tilesize), y_variation_coord]
          top = [x_variation_coord, math.ceil(self.y)]
          bottom = [x_variation_coord, math.ceil(self.y - self.h)]
          try:
            if tilemap[top[0]][top[1]].pass_through == False:
                self.vy = 0
                self.y -= player_speed
                
            if tilemap[left[0]][left[1]].pass_through == False:
                points_touching_wall += 1

            if tilemap[right[0]][right[1]].pass_through == False:
                points_touching_wall += 1

            if tilemap[bottom[0]][bottom[1]].pass_through == False:
                points_touching_ground += 1
          except:
            break
      
      if points_touching_ground < 1:
          self.ay = gravity

      # Creature can jump again only if more than 1/10 of the creature is touching the ground
      if points_touching_ground >= hitbox_points/10:
          if self.vy <= -0.5:
              self.hp -= (math.floor(-12 * self.vy - 5))
              self.vy = 0
          self.y = bottom[1] + self.h
          self.ay = 0
          self.vy = 0
          self.on_ground = True
      # Jump if there is a block in the way
      if points_touching_wall >= hitbox_points/5 and self.on_ground:
        self.x -= self.vx
        self.vx = 0
        self.vy = player_jump_speed
        self.on_ground = False

class Zombie(Creature):
  def __init__(self, x, y, tilemap):
    Creature.__init__(self, x, y, tilemap)
  def update_position(self):
    if player.x > self.x:
      self.vx = player_speed/2
    else:
      self.vx = -player_speed/2
    if (abs(self.x - player.x) < 0.1):
      self.vx = 0
      player.hp -= 0.1
    Creature.update_position(self)
