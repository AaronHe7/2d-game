import pygame

pygame.init()
fps = 60
clock = pygame.time.Clock()
width, height = 1280, 720
display = pygame.display.set_mode((width,height), pygame.HWSURFACE | pygame.FULLSCREEN)
pygame.display.set_caption("2D Game")
frame = 0
tilesize = 40
guiscale = 20

sky = pygame.Surface((tilesize, tilesize))
grass_block = pygame.image.load("grass_block.png").convert()
grass_block = pygame.transform.scale(grass_block, (tilesize, tilesize))
dirt_block = pygame.image.load("dirt_block.png").convert()
dirt_block = pygame.transform.scale(dirt_block, (tilesize, tilesize))
wood_block = pygame.image.load("wood_block.png").convert()
wood_block = pygame.transform.scale(wood_block, (tilesize, tilesize))
leaves_block = pygame.image.load("leaves_block.png").convert()
leaves_block = pygame.transform.scale(leaves_block, (tilesize, tilesize))
stone_block = pygame.image.load("stone_block.png").convert()
stone_block = pygame.transform.scale(stone_block, (tilesize, tilesize))

heart_icon = pygame.image.load("heart.png").convert_alpha()
heart_icon = pygame.transform.scale(heart_icon, (guiscale, guiscale))
half_heart_icon = pygame.image.load("half_heart.png").convert_alpha()
half_heart_icon = pygame.transform.scale(half_heart_icon, (guiscale, guiscale))
empty_heart_icon = pygame.image.load("empty_heart.png").convert_alpha()
empty_heart_icon = pygame.transform.scale(empty_heart_icon, (guiscale, guiscale))

player_idle0_right = pygame.image.load("player_idle0_right.png").convert_alpha()
player_idle0_right = pygame.transform.scale(player_idle0_right, (int(0.85 * tilesize), int(1.8 * tilesize)))
player_idle0_left = pygame.image.load("player_idle0_left.png").convert_alpha()
player_idle0_left = pygame.transform.scale(player_idle0_left, (int(0.85 * tilesize), int(1.8 * tilesize)))
player_run0_right = pygame.image.load("player_run0_right.png").convert_alpha()
player_run0_right = pygame.transform.scale(player_run0_right, (int(0.85 * tilesize), int(1.8 * tilesize)))
player_run0_left = pygame.image.load("player_run0_left.png").convert_alpha()
player_run0_left = pygame.transform.scale(player_run0_left, (int(0.85 * tilesize), int(1.8 * tilesize)))
player_falling_left = pygame.image.load("player_falling_left.png").convert_alpha()
player_falling_left = pygame.transform.scale(player_falling_left, (int(0.85 * tilesize), int(1.8 * tilesize)))
player_falling_right = pygame.image.load("player_falling_right.png").convert_alpha()
player_falling_right = pygame.transform.scale(player_falling_right, (int(0.85 * tilesize), int(1.8 * tilesize)))
player_run1_right = pygame.image.load("player_run1_right.png").convert_alpha()
player_run1_right = pygame.transform.scale(player_run1_right, (int(0.85 * tilesize), int(1.8 * tilesize)))
player_run1_left = pygame.image.load("player_run1_left.png").convert_alpha()
player_run1_left = pygame.transform.scale(player_run1_left, (int(0.85 * tilesize), int(1.8 * tilesize)))
player_run2_right = pygame.image.load("player_run2_right.png").convert_alpha()
player_run2_right = pygame.transform.scale(player_run2_right, (int(0.85 * tilesize), int(1.8 * tilesize)))
player_run2_left = pygame.image.load("player_run2_left.png").convert_alpha()
player_run2_left = pygame.transform.scale(player_run2_left, (int(0.85 * tilesize), int(1.8 * tilesize)))


player_models = []
player_models.append(player_idle0_left) # 0
player_models.append(player_idle0_right) # 1
player_models.append(player_run0_left) # 2
player_models.append(player_run0_right) # 3
player_models.append(player_falling_left) # 4
player_models.append(player_falling_right) # 5
player_models.append(player_run1_left) # 6
player_models.append(player_run1_right) # 7
player_models.append(player_run2_left) # 8
player_models.append(player_run2_right) # 9

textures = [sky, grass_block, dirt_block, wood_block, leaves_block, stone_block]
gui_elements = [empty_heart_icon, half_heart_icon, heart_icon]



tilemap = {}


player_speed = 5/tilesize
player_jump_speed = 9/tilesize
gravity = -1/tilesize
