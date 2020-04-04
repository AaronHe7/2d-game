import sys, pygame, animations, copy, random
from player import *
from assets import *
from gui import *
from terrain_gen import *
from entities import *

player = Player(0, 2, tilemap)

gui = Gui()
cell = []

while 1:
    if player.y < -2:
        display.fill((75,75,85))
    else:
        display.fill((102, 204, 255))
    # Center player
    player_x_display = width/2 - player.w/2
    player_y_display = height/2 - player.h/2

    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()

    if keys[pygame.K_d]:
        player.vx = player_speed
    if keys[pygame.K_a]:
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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d and player.vx > 0:
                player.vx = 0
            if event.key == pygame.K_a and player.vx < 0:
                player.vx = 0

        if event.type == pygame.KEYDOWN:
            pass

    x_start = int(player.x - ((width/2)//tilesize)) - 5
    x_end = int(player.x + ((width/2)//tilesize)) + 5
    y_start = int(player.y - ((height/2)//tilesize)) - 5
    y_end = int(player.y + ((height/2)//tilesize)) + 5

    for x in range(x_start, x_end):
        for y in range(y_start, y_end):
            if x not in tilemap:
                tilemap[x] = {}
            if y not in tilemap[x]:
                generate_terrain(x, y, cell)
            if tilemap[x][y].id != 0:
                display.blit(textures[tilemap[x][y].id], (int(player_x_display + tilesize * (x - player.x)), int(player_y_display -  tilesize * (y - player.y))))
                if tilemap[x][y].durability < tilemap[x][y].max_durability:
                    if tilemap[x][y].frames_since_last_touched > 60:
                        tilemap[x][y].durability += 0.1
                    durability_index = int(9 - 9 * tilemap[x][y].durability // tilemap[x][y].max_durability)
                    display.blit(breaking_models[durability_index], (int(player_x_display + tilesize * (x - player.x)), int(player_y_display -  tilesize *(y - player.y))))
                tilemap[x][y].frames_since_last_touched += 1

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
                for row in range(len(player.inventory)):
                    for column in range(len(player.inventory[row])):
                        if player.inventory[row][column].id == drop.id and player.inventory[row][column].amount < 64:
                            player.inventory[row][column].amount += drop.amount / 4
                            break
                        elif player.inventory[row][column].id == 0:
                            player.inventory[row][column] = drop
                            break
                entities_group.remove(drop)
            else:
                drop.velx = -(drop.location[0] - 640 - tilesize // 20)
                drop.vely = (drop.location[1] - 360)
                drop.location[0] += drop.velx // 20
                drop.location[1] -= drop.vely // 20
                display.blit(mini_textures[drop.id], (drop.location))

    #draw player model

    if 4 > player.handstate > 0:
        if frame%5 == 0:
            player.handstate += 1

    if player.handstate == 4:
        player.handstate = 1

    player_model = player_models[animations.checkframe(player.direction, player.handstate, frame % maxrframe, [player.vx, player.vy], frame, maxrframe)]
    display.blit(player_model, (int(player_x_display), int(player_y_display)))

    #draw object in player's hand

    if player.vx == 0 and player.vy == 0 and player.on_ground == True:
        if frame%120 < 60:
            vertical_offset = 0
        if frame%120 >= 60:
            vertical_offset = 3

    if player.direction[1] == -1 and player.inhand.id != 0:
        display.blit(mini_textures[player.inhand.id],  (648 - (tilesize - 35) * player.direction[0], 350))
    else:
        if player.inhand.id <= 100 and player.inhand.id != 0:
            if player.handstate == 0:
                display.blit(mini_textures[player.inhand.id], (646 + (tilesize - 17) * player.direction[0], 393 + vertical_offset))
            elif player.handstate == 1:
                display.blit(mini_textures[player.inhand.id], (646 + (tilesize - 26) * player.direction[0], 383))
            elif player.handstate == 2:
                display.blit(mini_textures[player.inhand.id], (646 + (tilesize - 23) * player.direction[0], 385))
            elif player.handstate == 3:
                display.blit(mini_textures[player.inhand.id], (646 + (tilesize - 20) * player.direction[0], 395))
        if player.inhand.id >= 100:
            if player.direction[0] == 1:
                display.blit(mini_textures[player.inhand.id], (646 + (tilesize - 20) * player.direction[0], 390))
            if player.direction[0] == -1:
                display.blit(pygame.transform.flip(textures[player.inhand.id], False, True), (636 + (tilesize - 2) * player.direction[0], 380))

    #draw particles
                
    for particle in particles:
        particle[0][0] += particle[2][0]
        particle[0][1] += particle[2][1]
        particle[2][1] += 1
        particle[3] -= 0.2
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

    if keys[pygame.K_TAB]:
        #draw inventory aspects
        display.blit(dimming_overlay, (0, 0))
        display.blit(inventory_background, (340, 100))
        display.blit(hotbar, (542, 150))
        display.blit(inventory, (542, 150))
        display.blit(crafting_menu, (385, 150))
        display.blit(hotbar, (1060, 4))
        display.blit(player_model, (825, 175))
        for row in range(len(player.inventory)):
            for column in range(len(player.inventory[row])):
                if player.inventory[row][column].id != 0:
                    if player.inventory[row][column].amount <= 0:
                        empty = Item(0, [-tilesize, -tilesize])
                        player.inventory[row][column] = empty
                    display.blit(textures[player.inventory[row][column].id], (544 + column * 43, 152))
        if mouse[0]:
            pass
    else:
        #check if mouse 1 or mouse 2 is clicked, removing or building blocks.
        if mouse[0]:
            if player.handstate == 0:
                player.handstate = 1
            mouse_location = pygame.mouse.get_pos()
            mousex = math.floor(player.x + (mouse_location[0] - player_x_display)/tilesize)
            mousey = math.ceil(player.y - (mouse_location[1] - player_y_display)/tilesize)
            temp_block = tilemap[mousex][mousey]
            if 320 <= mouse_location[0] <= 960 and 180 <= mouse_location[1] <= 540:
                if temp_block.durability > 0:
                    temp_block.frames_since_last_touched = 0
                    if temp_block.required_tool == player.inhand.type:
                        temp_block.durability -= round(player.inhand.hit_multiplier, 3)
                    else:
                        temp_block.durability -= round(0.075, 3)
                    if temp_block.durability < 0:
                        temp_block.durability = 0
                    # ................location0.......................................colour1.........................................velocity2.........................radius3............
                    temp_particle = [[mouse_location[0], mouse_location[1]], [display.get_at(pygame.mouse.get_pos())[0] + random.randint(-20, 20), display.get_at(pygame.mouse.get_pos())[1] + random.randint(-20, 20), display.get_at(pygame.mouse.get_pos())[2] + random.randint(-20, 20)], [random.randint(-3, 3), random.randint(-5, -2)], random.randint(3, 6)]
                    particles.append(temp_particle)
                elif temp_block.durability <= 0.1 and temp_block.id > 0:
                    dropid = temp_block.id
                    # Set block to air when destroyed
                    drop = Item(dropid, [mouse_location[0], mouse_location[1]])
                    tilemap[mousex][mousey] = blocks[0]
                    entities_group.append(drop)
        else:
            player.handstate = 0

        if mouse[2]:
            mouse_location = pygame.mouse.get_pos()
            mousex = math.floor(player.x + (mouse_location[0] - player_x_display)/tilesize)
            mousey = math.ceil(player.y - (mouse_location[1] - player_y_display)/tilesize)
            temp_block = tilemap[mousex][mousey]
            able = 0

            if tilemap[mousex][mousey-1].id != 0:
                able += 1
            if tilemap[mousex-1][mousey].id != 0:
                able += 1
            if tilemap[mousex+1][mousey].id != 0:
                able += 1
            if tilemap[mousex][mousey+1].id != 0:
                able += 1

            if 320 <= mouse_location[0] <= 960 and 180 <= mouse_location[1] <= 540 and able > 0:
                if temp_block.id == 0 and player.inhand.id != 0 and player.inhand.amount > 0:
                    tilemap[mousex][mousey] = copy.deepcopy(blocks[player.inhand.id])
                    player.inhand.amount -= 1

    #draw hotbar

    display.blit(hotbar, (1060, 4))

    for row in range(len(player.inventory)):
        for column in range(len(player.inventory[row])):
            if player.inventory[row][column].id != 0:
                if player.inventory[row][column].amount <= 0:
                    empty = Item(0, [-tilesize, -tilesize])
                    player.inventory[row][column] = empty
                display.blit(textures[player.inventory[row][column].id], (1062 + column * 43, 6))
                text = font.render(str(math.floor(player.inventory[row][column].amount)), True, (255, 255, 255))
                if math.floor(player.inventory[row][column].amount < 10):
                    display.blit(text, (1093 + column * 43, 33))
                else:
                    display.blit(text, (1089 + column * 43, 33))

    #draw hotbar selection

    display.blit(highlighted, (1061 + (player.highlighted) * 43, 5))

    frame += 1

    player.update_position()
    player.update_vitals(frame)
    pygame.display.flip()
    clock.tick(fps)
