'''
Pygame and GUI Implementation
'''
import os
import sys
from typing import Union, Dict

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame 
import click

from mocks import StubCheckerboard

#from checkers import Board, TeamColor

WIDTH = 800
HEIGHT = 800
ROWS = 8
COLS = 8
SQ_SIZE = WIDTH // COLS

#colors
WHITE = (255, 255,255)
DARK = (155, 103,60)
YELLOW = (255, 204, 0)

IMG_SIZE = (90,90)

display = pygame.display.set_mode((WIDTH, HEIGHT))
RED_SPRITE = pygame.transform.scale(pygame.image.load('red.png'), IMG_SIZE)
BLACK_SPRITE = pygame.transform.scale(pygame.image.load('black.png'),IMG_SIZE)

#RED_SPRITE.set_size(0.5)
#BLACK_SPRITE.set_size(0.5)

#sample board
ex_board = StubCheckerboard()

#draw board method
def draw_board(window, board):
    

    window.fill(DARK)
    for row in range(ROWS):
        for col in range(row%2, ROWS, 2):
            pygame.draw.rect(window, WHITE, (row*SQ_SIZE, col*SQ_SIZE, SQ_SIZE, SQ_SIZE))

    for rows in range(ROWS):
        for cols in range(ROWS):
            curr_loc = board.board[cols][rows]
            if curr_loc is not None:
                if curr_loc == 'red':
                    window.blit(RED_SPRITE, (rows*SQ_SIZE+4, cols*SQ_SIZE+4))
                else:
                    window.blit(BLACK_SPRITE,(rows*SQ_SIZE+4, cols*SQ_SIZE+4) )


#implementation
pygame.init()
pygame.display.set_caption('Checkers')
pygame.display.update()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        draw_board(display, ex_board)
        pygame.display.update()

pygame.quit()
quit()

