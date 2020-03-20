import sys, pygame
from player import *
from assets import *
from terrain_gen import *
import random

pygame.init()
fps = 120
clock = pygame.time.Clock()
width, height = 1280, 720
display = pygame.display.set_mode((width,height))
pygame.display.set_caption("2D Game")

player = Player(0, -2, tilemap)
player_model = pygame.Surface((player.w * tilesize, player.h * tilesize))
player_model.fill((0, 0, 0))


while 1:
    print('x: ' + str(player.x) + ' ' + 'y: ' + str(player.y))
    display.fill((255, 255, 255))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        player.vx = player_speed
    if keys[pygame.K_a]:
        player.vx = -player_speed
    if keys[pygame.K_SPACE] and player.on_ground:
        player.on_ground = False
        player.vy = player_jump_speed
                
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d and player.vx > 0:
                player.vx = 0
            if event.key == pygame.K_a and player.vx < 0:
                player.vx = 0

    x_start = int(player.x - ((width/2)//tilesize)) - 10
    x_end = int(player.x + ((width/2)//tilesize)) + 10
    y_start = int(player.y - ((height/2)//tilesize)) - 10
    y_end = int(player.y + ((height/2)//tilesize)) + 10

    # Center player
    player_x_display = width/2 - player.w/2
    player_y_display = height/2 - player.h/2
    for x in range(x_start, x_end):
        for y in range(y_start, y_end):
            if x not in tilemap:
                tilemap[x] = {}
            if y not in tilemap[x]:
                if y > 0:
                    # Dirt
                    tilemap[x][y] = 2
                elif y == 0:
                    # Grass
                    tilemap[x][y] = 1
                elif y < 0:
                    tilemap[x][y] = 0
            display.blit(textures[tilemap[x][y]], (player_x_display + tilesize * (x - player.x), player_y_display +  tilesize *(y - player.y)))
    display.blit(player_model, (player_x_display, player_y_display))

    player.update_position()
    pygame.display.flip()
    clock.tick(fps)
