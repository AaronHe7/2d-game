import sys, pygame
from player import *

pygame.init()
fps = 120
clock = pygame.time.Clock()
width, height = 1280, 720
display = pygame.display.set_mode((width,height))
pygame.display.set_caption("2D Game")

tilesize = 80
sky = pygame.image.load("sky.png")
sky = pygame.transform.scale(sky, (tilesize, tilesize))
grass_block = pygame.image.load("grass_block.png")
grass_block = pygame.transform.scale(grass_block, (tilesize, tilesize))
dirt_block = pygame.image.load("dirt_block.png")
dirt_block = pygame.transform.scale(dirt_block, (tilesize, tilesize))

textures = [sky, grass_block, dirt_block]
tilemap = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]]

player = Player(30, 300, tilemap)
player_model = pygame.Surface((player.w, player.h))
player_model.fill((0, 0, 0))

while 1:
    display.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                player.vx += 5
            if event.key == pygame.K_a:
                player.vx += -5
            if event.key == pygame.K_SPACE and player.on_ground == True:
                player.vy = 30
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                player.vx -= 5
            if event.key == pygame.K_a:
                player.vx += 5

    for row in range(len(tilemap)):
        for column in range(len(tilemap[row])):
            display.blit(player_model, (player.x, player.y))
            display.blit(textures[tilemap[row][column]], (column * tilesize, row * tilesize))

    player.update_position()
    pygame.display.flip()
    clock.tick(fps)
