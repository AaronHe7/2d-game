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
guiscale = 25
blocks = {}
textures = {}
mini_textures = {}
font = pygame.font.Font("font.ttf", 10)

def load_block(id, name):
    block = Block(id, name)
    blocks[id] = block
    
    block_img = pygame.image.load('blocks/' + name + '.png').convert()
    block_img = pygame.transform.scale(block_img, (tilesize, tilesize))
    mini_block_img = pygame.transform.scale(block_img, (tilesize // 2, tilesize // 2))
    
    textures[id] = block_img
    mini_textures[id] = mini_block_img

def load_tile_img(file_name):
    file = pygame.image.load('player_sprites/' + file_name).convert_alpha()
    sprite = pygame.transform.scale(file, (int(0.85 * tilesize), int(1.8 * tilesize)))
    return sprite

sky = pygame.Surface((tilesize, tilesize))
textures[0] = sky
blocks[0] = Block(0, 'sky')
blocks[0].pass_through = True

load_block(1, 'grass_block')
load_block(2, 'dirt_block')
load_block(3, 'wood_block')
load_block(4, 'leaves_block')
load_block(5, 'stone_block')

item_hit_multipliers = [0.25, 0.25, 0.25, 0.25, 0.25]

heart_icon = pygame.image.load("heart.png").convert_alpha()
heart_icon = pygame.transform.scale(heart_icon, (guiscale, guiscale))
half_heart_icon = pygame.image.load("half_heart.png").convert_alpha()
half_heart_icon = pygame.transform.scale(half_heart_icon, (guiscale, guiscale))
empty_heart_icon = pygame.image.load("empty_heart.png").convert_alpha()
empty_heart_icon = pygame.transform.scale(empty_heart_icon, (guiscale, guiscale))

full_hunger_icon = pygame.image.load("full_hunger.png").convert_alpha()
full_hunger_icon = pygame.transform.scale(full_hunger_icon, (guiscale, guiscale))
half_hunger_icon = pygame.image.load("half_hunger.png").convert_alpha()
half_hunger_icon = pygame.transform.scale(half_hunger_icon, (guiscale, guiscale))
empty_hunger_icon = pygame.image.load("empty_hunger.png").convert_alpha()
empty_hunger_icon = pygame.transform.scale(empty_hunger_icon, (guiscale, guiscale))

player_models = []

player_models.append(load_tile_img("player_idle0_left.png")) #0
player_models.append(load_tile_img("player_idle0_right.png")) #1
player_models.append(load_tile_img("player_run0_left.png")) #2
player_models.append(load_tile_img("player_run0_right.png")) #3
player_models.append(load_tile_img("player_falling_left.png")) #4
player_models.append(load_tile_img("player_falling_right.png")) #5
player_models.append(load_tile_img("player_run1_left.png")) #6
player_models.append(load_tile_img("player_run1_right.png")) #7
player_models.append(load_tile_img("player_run2_left.png")) #8
player_models.append(load_tile_img("player_run2_right.png")) #9
player_models.append(load_tile_img("player_idle1_left.png")) #10
player_models.append(load_tile_img("player_idle1_right.png")) #11
player_models.append(load_tile_img("player_hit0_left.png")) #12
player_models.append(load_tile_img("player_hit1_left.png")) #13
player_models.append(load_tile_img("player_hit2_left.png")) #14
player_models.append(load_tile_img("player_hit0_right.png")) #15
player_models.append(load_tile_img("player_hit1_right.png")) #16
player_models.append(load_tile_img("player_hit2_right.png")) #17

wooden_pickaxe = pygame.image.load("wooden_pickaxe.png").convert_alpha()
wooden_pickaxe = pygame.transform.scale(wooden_pickaxe, (tilesize, tilesize))

hotbar = pygame.image.load("hotbar.png").convert()
inventory = pygame.image.load("inventory.png").convert_alpha()
highlighted = pygame.image.load("inhand.png").convert_alpha()
crafting_menu = pygame.image.load("crafting_menu.png").convert()
dimming_overlay = pygame.image.load("dim.png").convert_alpha()
inventory_background = pygame.image.load("inventory_background.png").convert_alpha()
inventory_background = pygame.transform.scale(inventory_background, (600, 400))

breaking_models = []
for i in range(10):
    breaking_model = pygame.image.load("blocks/breaking" + str(i) + ".png").convert_alpha()
    breaking_model = pygame.transform.scale(breaking_model, (tilesize, tilesize))
    breaking_models.append(breaking_model)

item_models = []
item_models.append(wooden_pickaxe)

gui_elements = [empty_heart_icon, half_heart_icon, heart_icon]

hunger_icons = [empty_hunger_icon, half_hunger_icon, full_hunger_icon]

tilemap = {}

player_speed = 5/tilesize
player_jump_speed = 9/tilesize
gravity = -1/tilesize
