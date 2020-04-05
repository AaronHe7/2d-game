import sys, pygame, animations, copy, random
from player import *
from assets import *
from gui import *
from terrain_gen import *
from entities import *

player = Player(0, 4, tilemap)

gui = Gui()

while 1:
    if player.y < -2:
        display.fill((75,75,85))
    else:
        display.fill((102, 204, 255))
    # Center player
    player_x_display = width/2 - player.w/2
    player_y_display = height/2 - player.h/2
    mouse_location = pygame.mouse.get_pos()
    mousex = math.floor(player.x + (mouse_location[0] - player_x_display)/tilesize)
    mousey = math.ceil(player.y - (mouse_location[1] - player_y_display)/tilesize)
    #display.blit(background, (int(-player.x), int(player.y)))

    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()

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
                generate_terrain(x, y)
            if tilemap[x][y].id != 0:
                # Display block relative to player
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
                drop.location[0] += drop.velx / 20
                drop.location[1] -= drop.vely / 20
                display.blit(mini_textures[drop.id], (drop.location))

    #draw player model
    if (mouse[0] == 1 or mouse[2] == 1) and frame % 4 == 0:
        player.handstate %= 7
        player.handstate += 1

    player_model = player_models[animations.checkframe(player.direction, player.handstate, frame % maxrframe, [player.vx, player.vy], frame, maxrframe)]
    legs_model = player_models[animations.checkframe(player.direction, player.handstate, frame % maxrframe, [player.vx, player.vy], frame, maxrframe, legs = True)]
    display.blit(legs_model, (int(player_x_display), int(player_y_display)))
    display.blit(player_model, (int(player_x_display), int(player_y_display)))

    #draw particles
                
    for particle in particles:
        particle[0][0] += particle[2][0]
        particle[0][1] += particle[2][1]
        particle[2][1] += 1
        particle[3] -= 0.1
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
        if mouse[0] or mouse[2]:
            if mouse[0]:
                temp_block = tilemap[mousex][mousey]
                if 320 <= mouse_location[0] <= 960 and 180 <= mouse_location[1] <= 540 and temp_block.id != 0:
                    if temp_block.durability > 0:
                        temp_block.frames_since_last_touched = 0
                        # for playtesting: instantly destroy block
                        temp_block.durability -=100
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
            if mouse[2]:
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
