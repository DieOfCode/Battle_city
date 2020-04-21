#!/usr/bin/env python3

import random
import os
import math
import datetime
import pygame
import pygame.locals
import argparse
from settings import *
from constant import *
from Tank import *
from GameObject import *
import StartScreen


def main_loop():
    # START_SCREEN.stop()
    game_over = False
    pygame.display.set_caption("Battle city")
    main_player = Player(250, 350, 2, 0)
    enemy = Enemy(250, 400, 2, 0, "hurt")
    while not game_over:
        TIMER.tick(60)
        GAME_DISPLAY.fill((0, 0, 0))
        BEST_MUSIC.set_volume(0.1)
        # BEST_MUSIC.play()
        for bul in main_player.missile:
            bul.draw(GAME_DISPLAY, MISSILE)
            main_player.bullet_operation()
        Missile.missile_collision(main_player)
        main_player.draw(GAME_DISPLAY, PLAYER_SPRITE, (main_player.x, main_player.y))
        enemy.make_move(main_player)
        enemy.update_position(GAME_DISPLAY)
        for elements in main_player.map_game:
            elements.draw(GAME_DISPLAY)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
        keys = pygame.key.get_pressed()
        main_player.player_control(keys)
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--game', action='store_const', const='1', help='This will be option One')
    # if parser.parse_args().game == '1':
    StartScreen.start_screen()
