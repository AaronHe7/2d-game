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
last_jump_frame = 0
maxrframe = 30
tilesize = 40
guiscale = 20

def load_block(block_name):
    block = pygame.image.load('blocks/' + block_name + '.png').convert()
    return pygame.transform.scale(block, (tilesize, tilesize))

sky = pygame.Surface((tilesize, tilesize))
grass_block = load_block('grass_block')
dirt_block = load_block('dirt_block')
wood_block = load_block('wood_block')
leaves_block = load_block('leaves_block')
stone_block = load_block('stone_block')

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

breaking_models = []
for i in range(10):
    breaking_model = pygame.image.load("blocks/breaking" + str(i) + ".png").convert_alpha()
    breaking_model = pygame.transform.scale(breaking_model, (tilesize, tilesize))
    breaking_models.append(breaking_model)

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
