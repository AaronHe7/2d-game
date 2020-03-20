import pygame


tilesize = 80
guiscale = 20
sky = pygame.Surface((tilesize, tilesize))
grass_block = pygame.image.load("grass_block.png")
grass_block = pygame.transform.scale(grass_block, (tilesize, tilesize))
dirt_block = pygame.image.load("dirt_block.png")
dirt_block = pygame.transform.scale(dirt_block, (tilesize, tilesize))
wood_block = pygame.image.load("wood_block.png")
wood_block = pygame.transform.scale(wood_block, (tilesize, tilesize))
leaves_block = pygame.image.load("leaves_block.png")
leaves_block = pygame.transform.scale(leaves_block, (tilesize, tilesize))
heart_icon = pygame.image.load("heart.png")
heart_icon = pygame.transform.scale(heart_icon, (guiscale, guiscale))
half_heart_icon = pygame.image.load("half_heart.png")
half_heart_icon = pygame.transform.scale(half_heart_icon, (guiscale, guiscale))
empty_heart_icon = pygame.image.load("empty_heart.png")
empty_heart_icon = pygame.transform.scale(empty_heart_icon, (guiscale, guiscale))

textures = [sky, grass_block, dirt_block, wood_block, leaves_block]
gui_elements = [empty_heart_icon, half_heart_icon, heart_icon]



tilemap = {}


player_speed = 5/tilesize
player_jump_speed = 15/tilesize
gravity = -1/tilesize
