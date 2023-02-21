'''
Pygame and GUI Implementation
'''

import pygame 

pygame.init()
display = pygame.display.set_mode((800,600))
pygame.display.update()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
quit()