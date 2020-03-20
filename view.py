import sys, pygame
from player import *
from assets import *

pygame.init()
fps = 120
clock = pygame.time.Clock()
width, height = 1280, 720
display = pygame.display.set_mode((width,height))
pygame.display.set_caption("2D Game")

player = Player(30, 300, tilemap)
player_model = pygame.Surface((player.w, player.h))
player_model.fill((0, 0, 0))


while 1:
    display.fill((102, 204, 255))

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

    for row in range(len(tilemap)):
        for column in range(len(tilemap[row])):
            if tilemap[row][column] != 0:
                display.blit(textures[tilemap[row][column]], (column * tilesize, row * tilesize))

    display.blit(player_model, (player.x, player.y))
    player.update_position()
    pygame.display.flip()
    clock.tick(fps)
