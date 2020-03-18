import sys, pygame

pygame.init()
fps = 60
clock = pygame.time.Clock()
width, height = 1280, 720
display = pygame.display.set_mode((width,height))

tilesize = 80
sky = pygame.image.load("sky.png")
grass_block = pygame.image.load("grass_block.png")
dirt_block = pygame.image.load("dirt_block.png")

textures = [sky, grass_block, dirt_block]
tilemap = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]]

while 1:
    display.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    for row in range(len(tilemap)):
        for column in range(len(tilemap[row])):
            display.blit(textures[tilemap[row][column]], (column * tilesize, row * tilesize))

    pygame.display.flip()
    clock.tick(fps)
