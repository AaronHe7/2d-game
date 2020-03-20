import pygame


tilesize = 80
sky = pygame.Surface((tilesize, tilesize))
grass_block = pygame.image.load("grass_block.png")
grass_block = pygame.transform.scale(grass_block, (tilesize, tilesize))
dirt_block = pygame.image.load("dirt_block.png")
dirt_block = pygame.transform.scale(dirt_block, (tilesize, tilesize))

textures = [sky, grass_block, dirt_block]
tilemap = {}


player_speed = 8/tilesize
player_jump_speed = 15/tilesize
gravity = -1/tilesize
