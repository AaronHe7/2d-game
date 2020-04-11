import pygame, ast, math
from block import Block

pygame.init()
fps = 60 #determines the frames per second
clock = pygame.time.Clock()
width, height = 1280, 720

fullscreen = False
if fullscreen:
    display = pygame.display.set_mode((width,height), pygame.HWSURFACE | pygame.FULLSCREEN)
else:
    display = pygame.display.set_mode((width,height))
pygame.display.set_caption("2D Game")

frame = 0 #frame used for tick count
last_jump_frame = 0 #frame used to determine difference in last jump by ticks
maxrframe = 30 #used for animating player

tilesize = 40 #the tilesize used to determine block size and player size
guiscale = 25 #the tilesize used to determine size of gui elements
minitilesize = 30 #mini tilesize used for size of inventory items

break_radius = 5 #the radius of the circle that the player is able to break

blocks = {} #collection of copyable block objects
textures = {} #collection of item and block textures
mini_textures = {} #mini item and block textures

cursor = {'carrying':''} #used for inventory management, 'carrying' key shows the object that the cursor is carrying
font = pygame.font.Font("gui/font.ttf", 10) #font used
fontx = 26
fonty = 22

particles = [] #the particles list

item_hit_multipliers = {} #a dictionary of all the item hit multipliers used to determine the mine speed of tools
item_tooltypes = {} #a dictionary of all the item tooltypes to determine the type of tool an item could be

current_menu = None #current menu the player has open

fog_of_war_textures = {}

def load_block(id, name, durability, required_tool, transparency = False, exact_tool_required = False, pass_through = False, dropid = 'self'):
    block = Block(id, name, durability, required_tool, exact_tool_required = exact_tool_required, pass_through = pass_through, dropid = dropid)
    blocks[id] = block
    blocks[name] = block

    if transparency == True:
        block_img = pygame.image.load('blocks/' + name + '.png').convert_alpha()
    else:
        block_img = pygame.image.load('blocks/' + name + '.png').convert()
    block_img = pygame.transform.scale(block_img, (tilesize + 1, tilesize + 1))
    mini_block_img = pygame.transform.scale(block_img, (minitilesize, minitilesize))

    textures[id] = block_img
    textures[name] = block_img
    mini_textures[id] = mini_block_img
    mini_textures[name] = mini_block_img

def load_item(id, name, hit_multiplier = 1, tooltype = 'none'):
    item_img = pygame.image.load('items/' + name + '.png').convert_alpha()
    item_img = pygame.transform.scale(item_img, (tilesize, tilesize))
    mini_item_img = pygame.transform.scale(item_img, (minitilesize, minitilesize))

    textures[id] = item_img
    textures[name] = item_img
    mini_textures[id] = mini_item_img
    mini_textures[name] = mini_item_img
    item_hit_multipliers[id] = hit_multiplier
    item_hit_multipliers[name] = hit_multiplier
    item_tooltypes[id] = tooltype
    item_tooltypes[name] = tooltype

player_models = {} #dictionary of all the player images.

def load_tile_img(index, file_name):
    file = pygame.image.load('player_sprites/' + file_name).convert_alpha()
    sprite = pygame.transform.scale(file, (math.floor(0.85 * tilesize), math.floor(1.8 * tilesize)))
    player_models[index] = sprite

sky = pygame.Surface((tilesize, tilesize))
textures[0] = sky
mini_textures[0] = sky
blocks[0] = Block(0, 'sky', 0, 0)
blocks[0].pass_through = True

#dropid : the id of item that the block drops when destroyed, if unspecified it will drop itself
#['shovel', 0] : the tool required to speed up the breaking and the TIER of the item required (for example, you need at least a stone pickaxe to break iron ore, yielding a tier of 1
#transparency : whether or not the block has transparency
#exact_tool_required : if this is true, the block will not drop the dropid item unless the correct tool is used. if unspecified it will always drop the item even if the wrong tool is used
#pass_through : if the block can be passed through by the player.

#required parameters are ID, NAME, DURABILITY, and REQUIRED_TOOL

load_block(1, 'grass', 5, ['shovel', 0])
load_block(2, 'dirt', 5, ['shovel', 0])
load_block(3, 'wood', 10, ['axe', 0])
load_block(4, 'leaves', 3, ['none', 0], transparency = True, exact_tool_required = True)
load_block(5, 'stone', 20, ['pickaxe', 0], exact_tool_required = True)
load_block(6, 'wood_planks', 10, ['axe', 0])
load_block(7, 'bedrock', float('inf'), ['none', 0])
load_block(8, 'iron_ore', 20, ['pickaxe', 1], exact_tool_required = True)
load_block(9, 'coal_ore', 20, ['pickaxe', 0], exact_tool_required = True)
load_block(10, 'diamond_ore', 30, ['pickaxe', 2], exact_tool_required = True)
load_block(11, 'bloodstone_ore', 50, ['pickaxe', 3], exact_tool_required = True)
load_block(12, 'furnace', 20, ['pickaxe', 0], exact_tool_required = True)
load_block(13, 'wood_wall', 10, ['axe', 0], pass_through = True)

#tooltype : the type of tool and the tier it is
#number after name : the hit multiplier of the item when hitting the correct type of block

load_item(200, 'stick')
load_item(201, 'iron_ingot')
load_item(202, 'gold_ingot')
load_item(203, 'bloodstone_ingot')
load_item(204, 'ash')

load_item(256, 'wooden_pickaxe', 2, tooltype = ['pickaxe', 0])
load_item(257, 'stone_pickaxe', 3, tooltype = ['pickaxe', 1])
load_item(258, 'iron_pickaxe', 5, tooltype = ['pickaxe', 2])
load_item(259, 'diamond_pickaxe', 6, tooltype = ['pickaxe', 3])
load_item(260, 'wooden_shovel', 2, tooltype = ['shovel', 0])
load_item(261, 'stone_shovel', 3, tooltype = ['shovel', 1])
load_item(262, 'iron_shovel', 3.5, tooltype = ['shovel', 2])
load_item(263, 'diamond_shovel', 4, tooltype = ['shovel', 3])
load_item(264, 'wooden_axe', 1.35, tooltype = ['axe', 0])
load_item(265, 'stone_axe', 1.75, tooltype = ['axe', 1])
load_item(266, 'iron_axe', 2, tooltype = ['axe', 2])
load_item(267, 'diamond_axe', 2.25, tooltype = ['axe', 3])

#load gui hunger and heart elements

heart_icon = pygame.image.load("gui/heart.png").convert_alpha()
heart_icon = pygame.transform.scale(heart_icon, (guiscale, guiscale))
half_heart_icon = pygame.image.load("gui/half_heart.png").convert_alpha()
half_heart_icon = pygame.transform.scale(half_heart_icon, (guiscale, guiscale))
empty_heart_icon = pygame.image.load("gui/empty_heart.png").convert_alpha()
empty_heart_icon = pygame.transform.scale(empty_heart_icon, (guiscale, guiscale))

full_hunger_icon = pygame.image.load("gui/full_hunger.png").convert_alpha()
full_hunger_icon = pygame.transform.scale(full_hunger_icon, (guiscale, guiscale))
half_hunger_icon = pygame.image.load("gui/half_hunger.png").convert_alpha()
half_hunger_icon = pygame.transform.scale(half_hunger_icon, (guiscale, guiscale))
empty_hunger_icon = pygame.image.load("gui/empty_hunger.png").convert_alpha()
empty_hunger_icon = pygame.transform.scale(empty_hunger_icon, (guiscale, guiscale))

#load player elements

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

#load inventory elements

hotbar = pygame.image.load("gui/hotbar.png").convert()
inventory = pygame.image.load("gui/inventory.png").convert_alpha()
highlighted = pygame.image.load("gui/inhand.png").convert_alpha()
crafting_menu = pygame.image.load("gui/crafting_menu.png").convert()
dimming_overlay = pygame.image.load("gui/dim.png").convert_alpha()
dimming_overlay = pygame.transform.scale(dimming_overlay, (1280, 720))
inventory_background = pygame.image.load("gui/inventory_background.png").convert()
inventory_background = pygame.transform.scale(inventory_background, (600, 400))
inventory_square = pygame.image.load("gui/inventory_square.png").convert()
furnace_background = pygame.image.load("gui/furnace_background.png").convert()

#load fog of war models

for alpha in range(255):
    fog_of_war = pygame.Surface((tilesize, tilesize)).convert_alpha()
    fog_of_war.fill((0, 0, 0, alpha))
    fog_of_war_textures[alpha] = fog_of_war

#load breaking models

breaking_models = []

for i in range(10):
    breaking_model = pygame.image.load("blocks/breaking" + str(i) + ".png").convert_alpha()
    breaking_model = pygame.transform.scale(breaking_model, (tilesize, tilesize))
    breaking_models.append(breaking_model)

gui_elements = [empty_heart_icon, half_heart_icon, heart_icon]

hunger_icons = [empty_hunger_icon, half_hunger_icon, full_hunger_icon]

tilemap = {}

player_speed = 4.5/tilesize
player_jump_speed = 10/tilesize
gravity = -0.75/tilesize
