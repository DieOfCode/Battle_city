#!/usr/bin/env python3
import random
import os
import math
import datetime
import pygame
import pygame
import argparse
import GameOverScreen
from Tank import *
from GameObject import *
import StartScreen
from settings import *
from constant import *


def main_loop():
    # START_SCREEN.stop()
    game_over = False
    pygame.display.set_caption("Battle city")
    main_player = Player(250, 350, 1, 0)
    enemy = Enemy(400, 400, 1, 0, "hurt")
    game_over_screen = GameOverScreen.GameOver()
    while not game_over:
        TIMER.tick(60)
        GAME_DISPLAY.fill((0, 0, 0))
        BEST_MUSIC.set_volume(0.1)
        # BEST_MUSIC.play()
        enemy.shoot(main_player, enemy.direction)
        for bul in main_player.missile:
            bul.draw(GAME_DISPLAY, MISSILE)
            Missile.bullet_operation(main_player.missile)
        for bullet in enemy.missile:
            bullet.draw(GAME_DISPLAY, MISSILE)
            Missile.bullet_operation(enemy.missile)
            if not Missile.collision_with_player(enemy.missile,
                                                 pygame.Rect(main_player.x, main_player.y, OBJ_SIZE, OBJ_SIZE)):
                game_over_screen.game_over_screen()
        Missile.missile_collision(main_player)
        Missile.missile_collision(enemy)
        main_player.draw(GAME_DISPLAY, PLAYER_SPRITE, (main_player.x, main_player.y))
        enemy.make_move(main_player)
        enemy.update_position(GAME_DISPLAY)
        for elements in s.MAP:
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
    screen = StartScreen.Screen()
    screen.start_screen()
