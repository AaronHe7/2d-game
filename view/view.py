import sys, pygame

pygame.init()
fps = 60
clock = pygame.time.Clock()
width, height = 1280, 720
display = pygame.display.set_mode((width,height))

tilesize = 80
sky = pygame.Surface((tilesize, tilesize))
grass = pygame.Surface((tilesize, tilesize))
sky.fill((125, 125, 235))
grass.fill((125, 235, 125))

textures = [sky, grass]
tilemap = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

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
