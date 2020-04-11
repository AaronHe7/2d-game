import pygame, sys
from assets import *

while True:
    pygame_events = pygame.event.get()
    display.fill((255, 255, 255))
    
    for event in pygame_events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    clock.tick(60)
    pygame.display.update()
