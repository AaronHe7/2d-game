import pygame


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
[0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]]


player_speed = 5
player_jump_speed = 15
gravity = -1
