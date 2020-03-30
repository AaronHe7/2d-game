import pygame
from block import Block

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
blocks = {}
textures = {}

def load_block(id, name):
    block = Block(id, name)
    blocks[id] = block
    
    block_img = pygame.image.load('blocks/' + name + '.png').convert()
    block_img = pygame.transform.scale(block_img, (tilesize, tilesize)) 
    textures[id] = block_img

def load_tile_img(file_name):
    file = pygame.image.load('player_sprites/' + file_name).convert_alpha()
    return pygame.transform.scale(file, (int(0.85 * tilesize), int(1.8 * tilesize)))

sky = pygame.Surface((tilesize, tilesize))
textures[0] = sky
blocks[0] = Block(0, 'sky')
blocks[0].pass_through = True

load_block(1, 'grass_block')
load_block(2, 'dirt_block')
load_block(3, 'wood_block')
load_block(4, 'leaves_block')
load_block(5, 'stone_block')

heart_icon = pygame.image.load("heart.png").convert_alpha()
heart_icon = pygame.transform.scale(heart_icon, (guiscale, guiscale))
half_heart_icon = pygame.image.load("half_heart.png").convert_alpha()
half_heart_icon = pygame.transform.scale(half_heart_icon, (guiscale, guiscale))
empty_heart_icon = pygame.image.load("empty_heart.png").convert_alpha()
empty_heart_icon = pygame.transform.scale(empty_heart_icon, (guiscale, guiscale))

player_idle0_right = load_tile_img("player_idle0_right.png")
player_idle0_left = load_tile_img("player_idle0_left.png")
player_run0_right = load_tile_img("player_run0_right.png")
player_run0_left = load_tile_img("player_run0_left.png")
player_falling_left = load_tile_img("player_falling_left.png")
player_falling_right = load_tile_img("player_falling_right.png")
player_run1_right = load_tile_img("player_run1_right.png")
player_run1_left = load_tile_img("player_run1_left.png")
player_run2_right = load_tile_img("player_run2_right.png")
player_run2_left = load_tile_img("player_run2_left.png")
player_idle1_right = load_tile_img("player_idle1_right.png")
player_idle1_left = load_tile_img("player_idle1_left.png")

wooden_pickaxe = pygame.image.load("wooden_pickaxe.png").convert_alpha()
wooden_pickaxe = pygame.transform.scale(wooden_pickaxe, (tilesize, tilesize))

hotbar = pygame.image.load("hotbar.png").convert()
inventory = pygame.image.load("inventory.png").convert_alpha()

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


gui_elements = [empty_heart_icon, half_heart_icon, heart_icon]


tilemap = {}

player_speed = 5/tilesize
player_jump_speed = 9/tilesize
gravity = -1/tilesize
