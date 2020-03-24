import sys, pygame, animations
from player import *
from assets import *
from gui import *
from terrain_gen import *

player = Player(0, -2, tilemap)

gui = Gui()
cell = []

while 1:
    if player.y > 2:
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
        if tilemap[math.floor(player.x + player.vx + player.w/2)][math.floor(player.y + player.h)] == 0 and player.on_ground:
            player.vx = 0
    if keys[pygame.K_SPACE] and player.on_ground and abs(frame - last_jump_frame) > 1/2 * fps:
        last_jump_frame = frame
        player.on_ground = False
        player.vy = player_jump_speed
             
    else:
        player.vxmultiplier = 1

    if mouse[0]:
        mouse_location = pygame.mouse.get_pos()
        mousex = player.x + (mouse_location[0] - player_x_display)/tilesize
        mousey = player.y + (mouse_location[1] - player_y_display)/tilesize
        if tilemap[math.floor(mousex)][math.floor(mousey)].durability > 0:
            tilemap[math.floor(mousex)][math.floor(mousey)].durability -= 1
        else:
            tilemap[math.floor(mousex)][math.floor(mousey)] = generate_terrain(removal = 1)

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

    x_start = int(player.x - ((width/2)//tilesize)) - 2
    x_end = int(player.x + ((width/2)//tilesize)) + 2
    y_start = int(player.y - ((height/2)//tilesize)) - 2
    y_end = int(player.y + ((height/2)//tilesize)) + 2

    for x in range(x_start, x_end):
        for y in range(y_start, y_end):
            if x not in tilemap:
                tilemap[x] = {}
            if y not in tilemap[x]:
                tilemap[x][y] = generate_terrain(x, y, cell)
            if tilemap[x][y].id != 0:
                display.blit(textures[tilemap[x][y].id], (int(player_x_display + tilesize * (x - player.x)), int(player_y_display +  tilesize *(y - player.y))))
                if tilemap[x][y].durability < tilemap[x][y].max_durability:
                    durability_index = 9 - (9 * tilemap[x][y].durability // tilemap[x][y].max_durability)
                    display.blit(breaking_models[durability_index], (int(player_x_display + tilesize * (x - player.x)), int(player_y_display +  tilesize *(y - player.y))))
                    

    if player.vx > 0:
        player.direction[0] = 1
    elif player.vx < 0:
        player.direction[0] = 0
    if player.vy == 0:
        player.direction[1] = 0
    elif player.vy > 0:
        player.direction[1] = 1
    elif player.vy < 0:
        player.direction[1] = -1

    player_model = player_models[animations.checkframe(player.direction, player.handstate, frame % maxrframe, [player.vx, player.vy], frame % 60, maxrframe)]
    display.blit(player_model, (int(player_x_display), int(player_y_display)))

    bar = gui.return_bar(player.hp)
    for icon in range(10):
        display.blit(gui_elements[bar[icon]], (icon*21 + 5, 5))

    frame += 1

    player.update_position()
    pygame.display.flip()
    clock.tick(fps)
