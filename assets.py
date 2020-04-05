import pygame, ast, math
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
break_radius = 5
blocks = {}
textures = {}
mini_textures = {}
font = pygame.font.Font("font.ttf", 10)
recipes = []
particles = []

with open("crafting_recipes/recipes.txt") as recipes:
    recipes = ast.literal_eval(recipes.read())

def load_block(id, name, durability):
    block = Block(id, name, durability)
    blocks[id] = block

    block_img = pygame.image.load('blocks/' + name + '.png').convert()
    block_img = pygame.transform.scale(block_img, (tilesize + 1, tilesize + 1))
    mini_block_img = pygame.transform.scale(block_img, (tilesize // 2, tilesize // 2))

    textures[id] = block_img
    mini_textures[id] = mini_block_img

player_models = {}

def load_tile_img(index, file_name):
    file = pygame.image.load('player_sprites/' + file_name).convert_alpha()
    sprite = pygame.transform.scale(file, (math.floor(0.85 * tilesize), math.floor(1.8 * tilesize)))
    player_models[index] = sprite

sky = pygame.Surface((tilesize, tilesize))
textures[0] = sky
blocks[0] = Block(0, 'sky', 0)
blocks[0].pass_through = True

load_block(1, 'grass', 5)
load_block(2, 'dirt', 5)
load_block(3, 'wood', 10)
load_block(4, 'leaves', 3)
load_block(5, 'stone', 20)
load_block(6, 'wood_planks', 20)
load_block(7, 'bedrock', float('inf'))

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

load_tile_img(0, "player_idle0_left.png")
load_tile_img(1, "player_idle0_right.png")
load_tile_img(2, "player_run0_left.png")
load_tile_img(3, "player_run0_right.png")
load_tile_img(4, "player_falling_left.png")
load_tile_img(5, "player_falling_right.png")
load_tile_img(6, "player_run1_left.png")
load_tile_img(7, "player_run1_right.png")
load_tile_img(8, "player_run2_left.png")
load_tile_img(9, "player_run2_right.png")
load_tile_img(10, "player_idle1_left.png") 
load_tile_img(11, "player_idle1_right.png") 
load_tile_img(12, "player_hit0_left.png") 
load_tile_img(13, "player_hit1_left.png") 
load_tile_img(14, "player_hit2_left.png") 
load_tile_img(15, "player_hit0_right.png") 
load_tile_img(16, "player_hit1_right.png") 
load_tile_img(17, "player_hit2_right.png") 
load_tile_img(18, "player_run3_left.png") 
load_tile_img(19, "player_run4_left.png") 
load_tile_img(20, "player_run5_left.png") 
load_tile_img(21, "player_run6_left.png") 
load_tile_img(22, "player_run7_left.png") 
load_tile_img(23, "player_run3_right.png") 
load_tile_img(24, "player_run4_right.png") 
load_tile_img(25, "player_run5_right.png") 
load_tile_img(26, "player_run6_right.png") 
load_tile_img(27, "player_run7_right.png") 
load_tile_img(28, "player_hit3_left.png") 
load_tile_img(29, "player_hit4_left.png") 
load_tile_img(30, "player_hit5_left.png") 
load_tile_img(31, "player_hit6_left.png")
load_tile_img(32, "player_hit3_right.png")
load_tile_img(33, "player_hit4_right.png")
load_tile_img(34, "player_hit5_right.png")
load_tile_img(35, "player_hit6_right.png")

load_tile_img(-100, "legs_idle_left.png")
load_tile_img(-101, "legs_idle_right.png")
load_tile_img(-102, "legs_falling_left.png")
load_tile_img(-103, "legs_falling_right.png")
load_tile_img(-104, "legs_run0_left.png")
load_tile_img(-105, "legs_run0_right.png")
load_tile_img(-106, "legs_run1_left.png")
load_tile_img(-107, "legs_run1_right.png")
load_tile_img(-108, "legs_run2_left.png")
load_tile_img(-109, "legs_run2_right.png")
load_tile_img(-110, "legs_run3_left.png")
load_tile_img(-111, "legs_run3_right.png")
load_tile_img(-112, "legs_run4_left.png")
load_tile_img(-113, "legs_run4_right.png")
load_tile_img(-114, "legs_run5_left.png")
load_tile_img(-115, "legs_run5_right.png")
load_tile_img(-116, "legs_run6_left.png")
load_tile_img(-117, "legs_run6_right.png")
load_tile_img(-118, "legs_run7_left.png")
load_tile_img(-119, "legs_run7_right.png")

load_tile_img(-1, "error.png") #Error for no image returned

wooden_pickaxe = pygame.image.load("wooden_pickaxe.png").convert_alpha()
wooden_pickaxe = pygame.transform.scale(wooden_pickaxe, (tilesize, tilesize))

hotbar = pygame.image.load("hotbar.png").convert()
inventory = pygame.image.load("inventory.png").convert_alpha()
highlighted = pygame.image.load("inhand.png").convert_alpha()
crafting_menu = pygame.image.load("crafting_menu.png").convert()
dimming_overlay = pygame.image.load("dim.png").convert_alpha()
dimming_overlay = pygame.transform.scale(dimming_overlay, (1280, 720))
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

player_speed = 4.5/tilesize
player_jump_speed = 10/tilesize
gravity = -0.75/tilesize
