import sys, pygame, animations, copy, random, math
from player import *
from assets import *
from gui import *
from terrain_gen import *
from entities import *
from crafting import *
from mobs import *


crafting = Crafting(player.empty)
gui = Gui()
player.inventory[0][0] = Item(12, amount = 64)
player.inventory[0][1] = Item(259)
player.inventory[0][2] = Item(8, amount = 64)
player.inventory[0][3] = Item(11, amount = 64)
mobs = []
zombie = Zombie(player.x, player.y, tilemap)
#mobs.append(zombie)

while 1:
    pygame_events = pygame.event.get()
    if player.y < -2:
        display.fill((75,75,85))
    else:
        display.fill((102, 204, 255))
    # Center player
    player_x_display = width/2 - tilesize * player.w/2
    player_y_display = height/2 - tilesize * player.h/2
    mouse_location = pygame.mouse.get_pos()
    mousex = math.floor(player.x + (mouse_location[0] - player_x_display)/tilesize)
    mousey = math.ceil(player.y - (mouse_location[1] - player_y_display)/tilesize)

    player_mouse_dist = math.sqrt((player.x - mousex)**2 + (player.y - mousey)**2)

    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()

    mouse_down = [0, 0]
    keys_down = {pygame.K_TAB : 0}

    if keys[pygame.K_d]:
        player.vx = player_speed
    if keys[pygame.K_a]:
        player.vx = -player_speed
    if player.vx > player_speed:
        player.vx = player_speed
    if player.vx < -player_speed:
        player.vx = -player_speed
    if keys[pygame.K_LSHIFT] and player.on_ground:
        player.vxmultiplier = 0.5
        if tilemap[math.floor(player.x + player.vx + player.w/2)][math.ceil(player.y - player.h)].id == 0:
            player.vx = 0
    else:
        player.vxmultiplier = 1
    if keys[pygame.K_SPACE] and player.on_ground and abs(frame - last_jump_frame) > 3/8 * fps:
        last_jump_frame = frame
        player.on_ground = False
        player.vy = player_jump_speed

    if keys[pygame.K_1]:
        player.highlighted = 0
    elif keys[pygame.K_2]:
        player.highlighted = 1
    elif keys[pygame.K_3]:
        player.highlighted = 2
    elif keys[pygame.K_4]:
        player.highlighted = 3
    elif keys[pygame.K_5]:
        player.highlighted = 4

    player.inhand = player.inventory[0][player.highlighted]

    for event in pygame_events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d and player.vx > 0:
                player.vx = 0
            if event.key == pygame.K_a and player.vx < 0:
                player.vx = 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_down[0] = 1
            if event.button == 3:
                mouse_down[1] = 1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                keys_down[pygame.K_TAB] = 1


    x_start = math.floor(player.x - ((width/2)//tilesize)) - 5
    x_end = math.floor(player.x + ((width/2)//tilesize)) + 5
    y_start = math.floor(player.y - ((height/2)//tilesize)) - 5
    y_end = math.floor(player.y + ((height/2)//tilesize)) + 5

    for x in range(x_start, x_end):
        for y in range(y_start, y_end):
            if x not in tilemap:
                tilemap[x] = {}
            if y not in tilemap[x]:
                terrain.generate(x, y)
            if tilemap[x][y].id != 0:
                # Display block relative to player
                display.blit(textures[tilemap[x][y].id], (math.floor(player_x_display + tilesize * (x - player.x)), math.floor(player_y_display -  tilesize * (y - player.y))))
                # furnace
                if tilemap[x][y].id == 12 or tilemap[x][y].id == 14:
                    if 'furnace' not in tilemap[x][y].nbt_tags:
                        tilemap[x][y].nbt_tags['furnace'] = {'fuel' : player.empty, 'smelt' : player.empty, 'resultant' : player.empty, 'fuel_amount' : 0, 'progress' : 0, 'currently_cooking' : player.empty}
                    current_furnace = tilemap[x][y].nbt_tags['furnace']
                    if current_furnace['progress'] > 0:
                        tilemap[x][y].id = 14
                    else:
                        tilemap[x][y].id = 12
                    if current_furnace['fuel'].id in crafting.fuels:
                        if frame%60 == 0:
                            current_furnace['fuel'].amount -= 1
                            current_furnace['fuel_amount'] += crafting.fuels[current_furnace['fuel'].id]
                            if current_furnace['fuel'].amount < 1:
                                current_furnace['fuel'] = player.empty

                    if current_furnace['smelt'].id in crafting.furnace_recipes and current_furnace['fuel_amount'] > 0:
                        if current_furnace['progress'] == 0:
                            current_furnace['smelt'].amount -= 1
                            current_furnace['currently_cooking'] = current_furnace['smelt']
                            if current_furnace['smelt'].amount < 1:
                                current_furnace['smelt'] = player.empty
                            current_furnace['progress'] += 1

                    if current_furnace['progress'] > 0 and frame%15 == 0 and current_furnace['fuel_amount'] > 0: #change here to reduce / increase time of cooking
                        current_furnace['progress'] += 1
                        current_furnace['fuel_amount'] -= 1

                    if current_furnace['progress'] >= 100:
                        if current_furnace['resultant'].id == Item(crafting.furnace_recipes[current_furnace['currently_cooking'].id]).id:
                            current_furnace['resultant'].amount += 1
                        else:
                            current_furnace['resultant'] = Item(crafting.furnace_recipes[current_furnace['currently_cooking'].id])
                        current_furnace['progress'] = 0

                #durability and breaking of blocks
                if tilemap[x][y].durability < tilemap[x][y].max_durability:
                    if tilemap[x][y].frames_since_last_touched > 60:
                        tilemap[x][y].durability += 0.1
                    durability_index = math.floor(9 - 9 * tilemap[x][y].durability // tilemap[x][y].max_durability)
                    display.blit(breaking_models[durability_index], (math.floor(player_x_display + tilesize * (x - player.x)), math.floor(player_y_display -  tilesize *(y - player.y))))
                tilemap[x][y].frames_since_last_touched += 1
    
    for mob in mobs:
        x = math.floor(player_x_display + tilesize * (mob.x - player.x))
        y = math.floor(player_y_display -  tilesize * (mob.y - player.y))
        mob.update_position()
        pygame.draw.rect(display, (0, 0, 0), [x, y, mob.w * tilesize, mob.h * tilesize])

    #check player direction

    if player.vx > 0:
        player.direction[0] = 1
    elif player.vx < 0:
        player.direction[0] = -1
    if player.vy == 0:
        player.direction[1] = 0
    elif player.vy > 0:
        player.direction[1] = 1
    elif player.vy < 0:
        player.direction[1] = -1

    #draw dropped items and gravitate them towards the player

    for drop in entities_group:
        if drop.type == 'item' or drop.type == 'block':
            if width / 2 - player.w / 2 - tilesize < drop.location[0] < width / 2 + player.w / 2 + tilesize and height / 2 - player.h /2 - tilesize < drop.location[1] < height / 2 + player.h / 2 + tilesize * 1.5:
                locator = player.check_inventory(drop)
                entities_group.remove(drop)
                if locator[-1] == True:
                    player.inventory[locator[0]][locator[1]].amount += locator[2]
                elif locator[-1] == False:
                    player.inventory[locator[0]][locator[1]] = drop
            else:
                pass
                drop.velx = -(drop.location[0] - 640 - tilesize // 20)
                drop.vely = (drop.location[1] - 360)
                drop.location[0] += math.floor(drop.velx / 20)
                drop.location[1] -= math.floor(drop.vely / 20)
                display.blit(mini_textures[drop.id], (drop.location))

    #draw player model

    player_model = player_models[animations.checkframe(player.direction, player.handstate, frame % maxrframe, [player.vx, player.vy], frame, maxrframe)]
    legs_model = player_models[animations.checkframe(player.direction, player.handstate, frame % maxrframe, [player.vx, player.vy], frame, maxrframe, legs = True)]
    display.blit(legs_model, (math.floor(player_x_display), math.floor(player_y_display)))
    display.blit(player_model, (math.floor(player_x_display), math.floor(player_y_display)))

    #draw particles

    for particle in particles:
        particle[0][0] += particle[2][0]
        particle[0][1] += particle[2][1]
        particle[2][1] += 1
        particle[3] -= 0.15
        for i in range(len(particle[1])):
            if particle[1][i] > 254:
                particle[1][i] = 254
            if particle[1][i] < 1:
                particle[1][i] = 1
        if particle[3] <= 0:
            particles.remove(particle)
        pygame.draw.circle(display, particle[1], particle[0], int(particle[3]))

    #draw hunger and hp bars

    bar = gui.return_bar(player.hp)
    for icon in range(10):
        display.blit(gui_elements[bar[icon]], (icon*(guiscale + 1) + 5, 5))
    bar = gui.return_bar(player.hunger)
    for icon in range(10):
        display.blit(hunger_icons[bar[icon]], (icon*(guiscale + 1) + 7, 10 + guiscale))

    #draw inventory if tab is held

    if keys_down[pygame.K_TAB] and current_menu == None:
        current_menu = 'inventory'
        keys_down[pygame.K_TAB] = 0
    elif keys_down[pygame.K_TAB] and current_menu != None:
        current_menu = None

    if current_menu == 'furnace':
        #draw furnace aspects

        current_furnace = tilemap[current_container_location[0]][current_container_location[1]].nbt_tags['furnace']
        inventory_mouse_location = [(mouse_location[0] - 544) // 43, (mouse_location[1] - 152) // 43]

        display.blit(dimming_overlay, (0, 0))
        display.blit(furnace_background, (340, 100))
        display.blit(inventory_square, (470, 150)) #right fuel square
        display.blit(inventory_square, (387, 150)) #left burn square
        display.blit(inventory_square, (431, 325)) #resultant square
        display.blit(hotbar, (542, 150))
        display.blit(inventory, (542, 150))

        if player.handstate > 0:
            player.handstate = 0

        #draw the items in the inventory

        for row in range(len(player.inventory)):
            for column in range(len(player.inventory[row])):
                if player.inventory[row][column].id != 0:
                    if player.inventory[row][column].amount < 1:
                        empty = Item(0)
                        player.inventory[row][column] = empty
                    display.blit(mini_textures[player.inventory[row][column].id], (549 + column * 43, 157 + row * 43))
                    text = font.render(str(math.floor(player.inventory[row][column].amount)), True, (255, 255, 255))
                    if math.floor(player.inventory[row][column].amount < 10):
                        display.blit(text, (575 + column * 43, 179 + row * 43))
                    elif math.floor(player.inventory[row][column].amount >= 10):
                        display.blit(text, (571 + column * 43, 179 + row * 43))

        # allow inventory items to be moved

        if mouse_down[0] == 1:
            if 0 <= inventory_mouse_location[0] <= 4 and 0 <= inventory_mouse_location[1] <= 3:
                hovered_inventory_space = player.inventory[inventory_mouse_location[1]][inventory_mouse_location[0]]
                if cursor['carrying'].id == 0:
                    if hovered_inventory_space.id != 0:
                        cursor['carrying'] = hovered_inventory_space
                        player.inventory[inventory_mouse_location[1]][inventory_mouse_location[0]] = copy.deepcopy(player.empty)
                elif cursor['carrying'].id >= 0:
                    if hovered_inventory_space.id == cursor['carrying'].id and hovered_inventory_space.amount + cursor['carrying'].amount <= 64:
                        player.inventory[inventory_mouse_location[1]][inventory_mouse_location[0]].amount += cursor['carrying'].amount
                        cursor['carrying'] = copy.deepcopy(player.empty)
                    else:
                        player.inventory[inventory_mouse_location[1]][inventory_mouse_location[0]], cursor['carrying'] = cursor['carrying'], player.inventory[inventory_mouse_location[1]][inventory_mouse_location[0]]

            if 389 <= mouse_location[0] <= 429 and 152 <= mouse_location[1] <= 192:
                current_furnace['smelt'], cursor['carrying'] = cursor['carrying'], current_furnace['smelt']
                current_furnace['progress'] = 0
                
            if 472 <= mouse_location[0] <= 512 and 152 <= mouse_location[1] <= 192:
                current_furnace['fuel'], cursor['carrying'] = cursor['carrying'], current_furnace['fuel']

            if 433 <= mouse_location[0] <= 473 and 327 <= mouse_location[1] <= 367 and cursor['carrying'].id == 0:
                current_furnace['resultant'], cursor['carrying'] = cursor['carrying'], current_furnace['resultant']
                
        # allow inventory items to be split

        if mouse_down[1] == 1:
            if 0 <= inventory_mouse_location[0] <= 4 and 0 <= inventory_mouse_location[1] <= 3:
                hovered_inventory_space = player.inventory[inventory_mouse_location[1]][inventory_mouse_location[0]]
                if cursor['carrying'].id == 0 and hovered_inventory_space.id != 0 and hovered_inventory_space.amount > 1:
                    if hovered_inventory_space.amount%2 == 0:
                        player.inventory[inventory_mouse_location[1]][inventory_mouse_location[0]].amount /= 2
                        player.inventory[inventory_mouse_location[1]][inventory_mouse_location[0]].amount = math.floor(player.inventory[inventory_mouse_location[1]][inventory_mouse_location[0]].amount)
                        cursor['carrying'] = copy.deepcopy(player.inventory[inventory_mouse_location[1]][inventory_mouse_location[0]])
                    elif hovered_inventory_space.amount%2 == 1:
                        player.inventory[inventory_mouse_location[1]][inventory_mouse_location[0]].amount /= 2
                        player.inventory[inventory_mouse_location[1]][inventory_mouse_location[0]].amount = math.floor(player.inventory[inventory_mouse_location[1]][inventory_mouse_location[0]].amount)
                        cursor['carrying'] = copy.deepcopy(player.inventory[inventory_mouse_location[1]][inventory_mouse_location[0]])
                        player.inventory[inventory_mouse_location[1]][inventory_mouse_location[0]].amount += 1

            if 389 <= mousex <= 429 and 152 <= mousey <= 192:
                if cursor['carrying'].id == 0:
                    pass

        if cursor['carrying'].id != 0:
            display.blit(mini_textures[cursor['carrying'].id], (mouse_location[0] + tilesize // 3, mouse_location[1] + tilesize // 3))

        display.blit(mini_textures[current_furnace['smelt'].id], (394, 157))
        display.blit(mini_textures[current_furnace['resultant'].id], (438, 333))
        display.blit(mini_textures[current_furnace['fuel'].id], (477, 157))

        text = font.render(str(current_furnace['smelt'].amount), True, (255, 255, 255))
        display.blit(text, (384 + fontx, 150 + fonty))
        text = font.render(str(current_furnace['resultant'].amount), True, (255, 255, 255))
        display.blit(text, (431 + fontx, 325 + fonty))
        text = font.render(str(current_furnace['fuel'].amount), True, (255, 255, 255))
        display.blit(text, (470 + fontx, 150 + fonty))
        text = font.render('Fuel : ' + str(current_furnace['fuel_amount']), True, (255, 255, 255))
        display.blit(text, (473, 140))
        text = font.render('Progress : ' + str(current_furnace['progress']) + "%", True, (255, 255, 255))
        display.blit(text, (380, 140))

    if current_menu == 'inventory':
        #draw inventory aspects

        inventory_mouse_location = [(mouse_location[0] - 544) // 43, (mouse_location[1] - 152) // 43]
        crafting_mouse_location = [(mouse_location[0] - 387) // 43, (mouse_location[1] - 152) // 43]

        display.blit(dimming_overlay, (0, 0))
        display.blit(inventory_background, (340, 100))
        display.blit(hotbar, (542, 150))
        display.blit(inventory, (542, 150))
        display.blit(crafting_menu, (385, 150))
        display.blit(hotbar, (1060, 4))
        display.blit(legs_model, (825, 175))
        display.blit(player_model, (825, 175))
        display.blit(inventory_square, (430, 352))

        #make sure the player is not stuck in a swinging animation when tab is pressed

        if player.handstate > 0:
            player.handstate = 0

        #draw the items in the crafting grid

        for row in range(len(crafting.crafting_grid)):
            for column in range(len(crafting.crafting_grid[row])):
                if crafting.crafting_grid[row][column].id != 0:
                    display.blit(mini_textures[crafting.crafting_grid[row][column].id], (392 + column * 43, 157 + row * 43))
                    text = font.render(str(math.floor(crafting.crafting_grid[row][column].amount)), True, (255, 255, 255))
                    if math.floor(crafting.crafting_grid[row][column].amount < 10):
                        display.blit(text, (418 + column * 43, 179 + row * 43))
                    elif math.floor(crafting.crafting_grid[row][column].amount >= 10):
                        display.blit(text, (414 + column * 43, 179 + row * 43))

        #draw the items in the player's inventory

        for row in range(len(player.inventory)):
            for column in range(len(player.inventory[row])):
                if player.inventory[row][column].id != 0:
                    if player.inventory[row][column].amount < 1:
                        empty = Item(0)
                        player.inventory[row][column] = empty
                    display.blit(mini_textures[player.inventory[row][column].id], (549 + column * 43, 157 + row * 43))
                    text = font.render(str(math.floor(player.inventory[row][column].amount)), True, (255, 255, 255))
                    if math.floor(player.inventory[row][column].amount < 10):
                        display.blit(text, (575 + column * 43, 179 + row * 43))
                    elif math.floor(player.inventory[row][column].amount >= 10):
                        display.blit(text, (571 + column * 43, 179 + row * 43))

        # check if the crafting grid matches a recipe
        if crafting.check_recipes() != 0:
            crafting.resultant = crafting.check_recipes()
            display.blit(mini_textures[crafting.resultant[0]], (437, 359))
            text = font.render(str(math.floor(crafting.resultant[1])), True, (255, 255, 255))
            if math.floor(crafting.resultant[0]) < 10:
                display.blit(text, (463, 381))
            else:
                display.blit(text, (459, 381))
            if 432 <= mouse_location[0] <= 472 and 354 <= mouse_location[1] <= 394:
                if mouse_down[0] == 1:
                    if keys[pygame.K_LSHIFT] == 1:
                        pass
                    else:
                        if cursor['carrying'].id == 0:
                            cursor['carrying'] = Item(crafting.resultant[0], amount = crafting.resultant[1])
                            for row in range(len(crafting.crafting_grid)):
                                for column in range(len(crafting.crafting_grid[row])):
                                    if crafting.crafting_grid[row][column].id != 0:
                                        crafting.crafting_grid[row][column].amount -= 1
                                        if crafting.crafting_grid[row][column].amount < 1:
                                            crafting.crafting_grid[row][column] = player.empty
                        elif cursor['carrying'].id == crafting.resultant[0] and cursor['carrying'].amount + crafting.resultant[1] <= 64:
                            cursor['carrying'].amount += crafting.resultant[1]
                            for row in range(len(crafting.crafting_grid)):
                                for column in range(len(crafting.crafting_grid[row])):
                                    if crafting.crafting_grid[row][column].id != 0:
                                        crafting.crafting_grid[row][column].amount -= 1
                                        if crafting.crafting_grid[row][column].amount < 1:
                                            crafting.crafting_grid[row][column] = player.empty

        if cursor['carrying'].id != 0:
            display.blit(mini_textures[cursor['carrying'].id], (mouse_location[0] + tilesize // 3, mouse_location[1] + tilesize // 3))

        #allow inventory items to be moved

        if mouse_down[0] == 1:
            if 0 <= inventory_mouse_location[0] <= 4 and 0 <= inventory_mouse_location[1] <= 3:
                hovered_inventory_space = player.inventory[inventory_mouse_location[1]][inventory_mouse_location[0]]
                if cursor['carrying'].id == 0:
                    if hovered_inventory_space.id != 0:
                        cursor['carrying'] = hovered_inventory_space
                        player.inventory[inventory_mouse_location[1]][inventory_mouse_location[0]] = copy.deepcopy(player.empty)
                elif cursor['carrying'].id >= 0:
                    if hovered_inventory_space.id == cursor['carrying'].id and hovered_inventory_space.amount + cursor['carrying'].amount <= 64:
                        player.inventory[inventory_mouse_location[1]][inventory_mouse_location[0]].amount += cursor['carrying'].amount
                        cursor['carrying'] = copy.deepcopy(player.empty)
                    else:
                        player.inventory[inventory_mouse_location[1]][inventory_mouse_location[0]], cursor['carrying'] = cursor['carrying'], player.inventory[inventory_mouse_location[1]][inventory_mouse_location[0]]

            elif 0 <= crafting_mouse_location[0] <= 2 and 0 <= crafting_mouse_location[1] <= 2:
                hovered_crafting_space = crafting.crafting_grid[crafting_mouse_location[1]][crafting_mouse_location[0]]
                if cursor['carrying'].id == 0:
                    if hovered_crafting_space.id != 0:
                        cursor['carrying'] = hovered_crafting_space
                        crafting.crafting_grid[crafting_mouse_location[1]][crafting_mouse_location[0]] = copy.deepcopy(player.empty)
                elif cursor['carrying'].id > 0:
                    if hovered_crafting_space.id == cursor['carrying'].id and hovered_crafting_space.amount + cursor['carrying'].amount <= 64:
                        crafting.crafting_grid[crafting_mouse_location[1]][crafting_mouse_location[0]].amount += cursor['carrying'].amount
                        cursor['carrying'] = copy.deepcopy(player.empty)
                    else:
                        crafting.crafting_grid[crafting_mouse_location[1]][crafting_mouse_location[0]], cursor['carrying'] = cursor['carrying'], crafting.crafting_grid[crafting_mouse_location[1]][crafting_mouse_location[0]]

        # allow inventory and crafting items to be split

        if mouse_down[1] == 1:
            if 0 <= inventory_mouse_location[0] <= 4 and 0 <= inventory_mouse_location[1] <= 3:
                hovered_inventory_space = player.inventory[inventory_mouse_location[1]][inventory_mouse_location[0]]
                if cursor['carrying'].id == 0 and hovered_inventory_space.id != 0 and hovered_inventory_space.amount > 1:
                    if hovered_inventory_space.amount%2 == 0:
                        player.inventory[inventory_mouse_location[1]][inventory_mouse_location[0]].amount /= 2
                        player.inventory[inventory_mouse_location[1]][inventory_mouse_location[0]].amount = math.floor(player.inventory[inventory_mouse_location[1]][inventory_mouse_location[0]].amount)
                        cursor['carrying'] = copy.deepcopy(player.inventory[inventory_mouse_location[1]][inventory_mouse_location[0]])
                    elif hovered_inventory_space.amount%2 == 1:
                        player.inventory[inventory_mouse_location[1]][inventory_mouse_location[0]].amount /= 2
                        player.inventory[inventory_mouse_location[1]][inventory_mouse_location[0]].amount = math.floor(player.inventory[inventory_mouse_location[1]][inventory_mouse_location[0]].amount)
                        cursor['carrying'] = copy.deepcopy(player.inventory[inventory_mouse_location[1]][inventory_mouse_location[0]])
                        player.inventory[inventory_mouse_location[1]][inventory_mouse_location[0]].amount += 1

            elif 0 <= crafting_mouse_location[0] <= 2 and 0 <= crafting_mouse_location[1] <= 2:
                hovered_crafting_space = crafting.crafting_grid[crafting_mouse_location[1]][crafting_mouse_location[0]]
                if cursor['carrying'].id == 0 and hovered_crafting_space.id != 0 and hovered_crafting_space.amount > 1:
                    if hovered_crafting_space.amount%2 == 0:
                        crafting.crafting_grid[crafting_mouse_location[1]][crafting_mouse_location[0]].amount /= 2
                        crafting.crafting_grid[crafting_mouse_location[1]][crafting_mouse_location[0]].amount = math.floor(crafting.crafting_grid[crafting_mouse_location[1]][crafting_mouse_location[0]].amount)
                        cursor['carrying'] = copy.deepcopy(crafting.crafting_grid[crafting_mouse_location[1]][crafting_mouse_location[0]])
                    elif hovered_crafting_space.amount%2 == 1:
                        crafting.crafting_grid[crafting_mouse_location[1]][crafting_mouse_location[0]].amount /= 2
                        crafting.crafting_grid[crafting_mouse_location[1]][crafting_mouse_location[0]].amount = math.floor(crafting.crafting_grid[crafting_mouse_location[1]][crafting_mouse_location[0]].amount)
                        cursor['carrying'] = copy.deepcopy(crafting.crafting_grid[crafting_mouse_location[1]][crafting_mouse_location[0]])
                        crafting.crafting_grid[crafting_mouse_location[1]][crafting_mouse_location[0]].amount += 1

    if current_menu == None:
        #check if mouse 1 or mouse 2 is clicked, removing or building blocks.
        if mouse[0] or mouse[2]:
            if frame % 4 == 0:
                player.handstate %= 7
                player.handstate += 1
            if mouse[0]:
                block = tilemap[mousex][mousey]
                if player_mouse_dist <= break_radius and block.id != 0:
                    if block.required_tool[0] == player.inhand.tooltype[0] and block.required_tool[1] <= player.inhand.tooltype[1]:
                        block.reduce_durability(player.inhand.hit_multiplier)
                    else:
                        block.reduce_durability()
                    if block.durability > 0:
                        block.frames_since_last_touched = 0
                        # for playtesting: instantly destroy block
                        #block.durability -=100
                        # ................location0.......................................colour1.........................................velocity2.........................radius3............
                        temp_particle = [[mouse_location[0], mouse_location[1]], [display.get_at(pygame.mouse.get_pos())[0] + random.randint(-20, 20), display.get_at(pygame.mouse.get_pos())[1] + random.randint(-20, 20), display.get_at(pygame.mouse.get_pos())[2] + random.randint(-20, 20)], [random.randint(-3, 3), random.randint(-5, -2)], random.randint(3, 6)]
                        particles.append(temp_particle)
                    elif block.durability < 1 and block.id > 0:
                        # Set block to air when destroyed
                        tilemap[mousex][mousey] = blocks[0]
                        if block.exact_tool_required == False:
                            drop = Item(block.dropid, [mouse_location[0], mouse_location[1]])
                            entities_group.append(drop)
                        else:
                            if block.required_tool[0] == player.inhand.tooltype[0] and block.required_tool[1] <= player.inhand.tooltype[1]:
                                drop = Item(block.dropid, [mouse_location[0], mouse_location[1]])
                                entities_group.append(drop)

            # if the player clicks right click and is holding a block then check if it can be placed
            if mouse[2]:
                if tilemap[mousex][mousey].id != 0 and not keys[pygame.K_LSHIFT]: #if the tile right clicked is a block
                    if tilemap[mousex][mousey].id == 12 or tilemap[mousex][mousey].id == 14:
                        #ability to open furnace here
                        current_menu = 'furnace'
                        current_container_location = [mousex, mousey]
                else:
                    if player.inhand.id < 200:
                        block = tilemap[mousex][mousey]
                        able = 0

                        if tilemap[mousex][mousey-1].id != 0:
                            able += 1
                        if tilemap[mousex-1][mousey].id != 0:
                            able += 1
                        if tilemap[mousex+1][mousey].id != 0:
                            able += 1
                        if tilemap[mousex][mousey+1].id != 0:
                            able += 1

                        if player_mouse_dist <= break_radius and able > 0:
                            if block.id == 0 and player.inhand.id != 0 and player.inhand.amount > 0:
                                for i in range(20):
                                    temp_particle = [[mouse_location[0], mouse_location[1]], [textures[player.inhand.id].get_at([20, 20])[0] + random.randint(-20, 20), textures[player.inhand.id].get_at([20, 20])[1] + random.randint(-20, 20), textures[player.inhand.id].get_at([20, 20])[2] + random.randint(-20, 20)], [random.randint(-3, 3), random.randint(-5, -2)], random.randint(3, 6)]
                                    particles.append(temp_particle)
                                tilemap[mousex][mousey] = blocks[player.inhand.id].get_copy()
                                player.inhand.amount -= 1
        else:
            if player.handstate > 0 and frame%4 == 1:
                player.handstate += 1
            if player.handstate > 7:
                player.handstate = 0

    #draw hotbar

    display.blit(hotbar, (1060, 4))

    if player.handstate > 0:
        if player.inhand.id < 200:
            temp_item = pygame.transform.flip(mini_textures[player.inhand.id], 1, 0)
            display.blit(temp_item, (mouse_location[0] - int(temp_item.get_width() / 2) + 30, mouse_location[1] - int(temp_item.get_height() / 2) + 30))
        else:
            angle = -(-player.handstate * 180/6)
            temp_item = pygame.transform.rotate(mini_textures[player.inhand.id], angle)
            temp_item_offset_x = 60/9 * (-(player.handstate - 4) ** 2 + 9) * -1
            temp_item_offset_y = player.handstate * 20
            display.blit(temp_item, (mouse_location[0] - int(temp_item.get_width() / 2) + 30, mouse_location[1] - int(temp_item.get_height() / 2) + 30))

    for column in range(len(player.inventory[0])):
        if player.inventory[0][column].id != 0:
            if player.inventory[0][column].amount < 1:
                empty = Item(0)
                player.inventory[0][column] = empty
            display.blit(mini_textures[player.inventory[0][column].id], (1067 + column * 43, 11))
            text = font.render(str(math.floor(player.inventory[0][column].amount)), True, (255, 255, 255))
            if math.floor(player.inventory[0][column].amount < 10):
                display.blit(text, (1093 + column * 43, 33))
            else:
                display.blit(text, (1089 + column * 43, 33))

    #draw hotbar selection

    display.blit(highlighted, (1061 + (player.highlighted) * 43, 5))

    frame += 1

    player.update_position()
    player.update_vitals(frame)

    pygame.display.update()
    clock.tick(fps)
