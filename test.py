import os
import math
import datetime
import pygame
import pygame.locals
from settings import *

sprites = pygame.transform.scale(pygame.image.load("images/sprites.gif"), [192, 224])
PLAYER_SPRITE = sprites.subsurface(56 * 2, 72 * 2, 8 * 2, 8 * 2)

TIMER = pygame.time.Clock()
def main_loop():
    game_over = False
    pygame.display.set_caption("Battle city")
    b = pygame.mixer_music.load('sounds/DOOM.mp3')
    pygame.mixer_music.play(b)
    while not game_over:
        TIMER.tick(60)
        GAME_DISPLAY.fill((0, 0, 0))
        GAME_DISPLAY.blit(PLAYER_SPRITE, (10, 10))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        pygame.display.update()
main_loop()