import pygame

pygame.init()
fps = 60
clock = pygame.time.Clock()
width, height = 1280, 720
fullscreen = False
if fullscreen:
    display = pygame.display.set_mode((width,height), pygame.HWSURFACE | pygame.FULLSCREEN)
else:
    display = pygame.display.set_mode((width,height))
pygame.display.set_caption("2D Game")
frame = 0
rframe = 0
maxrframe = 30
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
player_idle1_right = pygame.image.load("player_idle1_right.png").convert_alpha()
player_idle1_right = pygame.transform.scale(player_idle1_right, (int(0.85 * tilesize), int(1.8 * tilesize)))
player_idle1_left = pygame.image.load("player_idle1_left.png").convert_alpha()
player_idle1_left = pygame.transform.scale(player_idle1_left, (int(0.85 * tilesize), int(1.8 * tilesize)))

wooden_pickaxe = pygame.image.load("wooden_pickaxe.png").convert_alpha()
wooden_pickaxe = pygame.transform.scale(wooden_pickaxe, (tilesize, tilesize))

breaking0 = pygame.image.load("breaking0.png").convert_alpha()
breaking0 = pygame.transform.scale(breaking0, (tilesize, tilesize))
breaking1 = pygame.image.load("breaking1.png").convert_alpha()
breaking1 = pygame.transform.scale(breaking1, (tilesize, tilesize))
breaking2 = pygame.image.load("breaking2.png").convert_alpha()
breaking2 = pygame.transform.scale(breaking2, (tilesize, tilesize))
breaking3 = pygame.image.load("breaking3.png").convert_alpha()
breaking3 = pygame.transform.scale(breaking3, (tilesize, tilesize))
breaking4 = pygame.image.load("breaking4.png").convert_alpha()
breaking4 = pygame.transform.scale(breaking4, (tilesize, tilesize))
breaking5 = pygame.image.load("breaking5.png").convert_alpha()
breaking5 = pygame.transform.scale(breaking5, (tilesize, tilesize))
breaking6 = pygame.image.load("breaking6.png").convert_alpha()
breaking6 = pygame.transform.scale(breaking6, (tilesize, tilesize))
breaking7 = pygame.image.load("breaking7.png").convert_alpha()
breaking7 = pygame.transform.scale(breaking7, (tilesize, tilesize))
breaking8 = pygame.image.load("breaking8.png").convert_alpha()
breaking8 = pygame.transform.scale(breaking8, (tilesize, tilesize))
breaking9 = pygame.image.load("breaking9.png").convert_alpha()
breaking9 = pygame.transform.scale(breaking9, (tilesize, tilesize))

breaking_models = []
breaking_models.append(breaking0)
breaking_models.append(breaking1)
breaking_models.append(breaking2)
breaking_models.append(breaking3)
breaking_models.append(breaking4)
breaking_models.append(breaking5)
breaking_models.append(breaking6)
breaking_models.append(breaking7)
breaking_models.append(breaking8)
breaking_models.append(breaking9)

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
player_models.append(player_idle1_left) # 10
player_models.append(player_idle1_right) # 11

item_models = []
item_models.append(wooden_pickaxe)

textures = []

textures.append(sky) # 0
textures.append(grass_block) # 1
textures.append(dirt_block) # 2
textures.append(wood_block) # 3
textures.append(leaves_block) # 4
textures.append(stone_block) # 5

gui_elements = [empty_heart_icon, half_heart_icon, heart_icon]



tilemap = {}


player_speed = 5/tilesize
player_jump_speed = 9/tilesize
gravity = -1/tilesize
