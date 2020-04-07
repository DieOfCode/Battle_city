#!/usr/bin/env python3

import random
import os
import math
import datetime
import pygame
import pygame.locals
from settings import *

X_OR_Y_MAP = []


def message_to_screen(msg, color, width, height, font_type, y_displace=0, x_displace=0):
    text_surface, text_rect = text_objects(msg, color, font_type)
    text_rect.center = (width / 2) + x_displace, (height / 2) + y_displace
    GAME_DISPLAY.blit(text_surface, text_rect)


def create_menu_button(width, height):
    return pygame.Rect((width / 2), (height / 2), 120, 50)


def text_objects(text, color, font_type):
    text_surface = font_type.render(text, True, color)
    return text_surface, text_surface.get_rect()


def button_click(button):
    click = pygame.mouse.get_pressed()
    cur = pygame.mouse.get_pos()
    if button.x + button.width > cur[0] > button.x:
        if button.y + button.height > cur[1] > button.y:
            if click[0] == 1:
                return True
    return False


def start_screen():
    beginning = True
    while beginning:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    beginning = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        GAME_DISPLAY.fill(BLACK)
        message_to_screen("BATTLE CITY", RED, DISPLAY_WIDTH, DISPLAY_HEIGHT, FONT, -100)
        message_to_screen("It`s awful and i know it", WHITE,
                          DISPLAY_WIDTH, DISPLAY_HEIGHT, SMALL_FONT, -40)
        message_to_screen("Start", WHITE, DISPLAY_WIDTH, DISPLAY_HEIGHT, BUTTON_FONT, 20)
        start_button = create_menu_button(DISPLAY_WIDTH - 110, DISPLAY_HEIGHT - 40)
        if button_click(start_button):
            main_loop()
        pygame.display.update()
        TIMER.tick(FPS)


class GameObject():
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size


class Missile(GameObject):
    def __init__(self, x, y, angle, direction_x, direction_y, size):
        GameObject.__init__(self, x, y, size)
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.y = y
        self.speed_x = 3 * direction_x
        self.speed_y = 3 * direction_y
        self.angle = angle

    def draw(self, game_display, img):
        missile = pygame.transform.rotate(img, self.angle)
        game_display.blit(missile, (self.x, self.y))


class Tank:
    def __init__(self, x, y, speed, size, dx=0, dy=-1.0):
        self.x = x
        self.y = y
        self.speed = speed
        self.dx = dx
        self.dy = dy

        self.size = size
        self.angle = 0

    def draw(self, game_display, img):
        t = pygame.transform.rotate(img, self.angle)
        game_display.blit(t, (self.x, self.y))


class Player(Tank):
    def __init__(self, x, y, speed, size, map_game):
        Tank.__init__(self, x, y, speed, size)
        self.angle = 0
        self.missile = []
        self.map_game = map_game

    def player_control(self, keys):
        my_rect = pygame.Rect(self.x - 1, self.y, 1, 26)
        my_rect_2 = pygame.Rect(self.x + 25, self.y, 1, 26)
        my_rect_3 = pygame.Rect(self.x, self.y - 1, 26, 1)
        my_rect_4 = pygame.Rect(self.x, self.y + 26, 26, 1)
        t = my_rect.collidelistall(RECT_MAP)
        if keys[pygame.K_LEFT] and self.x > 0 and not my_rect.collidelistall(RECT_MAP):
            self.x -= self.speed
            self.angle = 90
            self.dx = -1
            self.dy = 0
        elif keys[pygame.K_RIGHT] and self.x < DISPLAY_WIDTH - 30 and not my_rect_2.collidelistall(RECT_MAP):
            self.x += self.speed
            self.angle = 270
            self.dx = 1
            self.dy = 0
        elif keys[pygame.K_UP] and self.y > 0 and not my_rect_3.collidelistall(RECT_MAP):
            self.y -= self.speed
            self.angle = 0
            self.dx = 0
            self.dy = -1
        elif keys[pygame.K_DOWN] and self.y < DISPLAY_HEIGHT - 30 and not my_rect_4.collidelistall(RECT_MAP):
            self.y += self.speed
            self.angle = 180
            self.dx = 0
            self.dy = 1

        if keys[pygame.K_SPACE] and len(self.missile) < 2:
            self.missile.append(Missile(self.x, self.y, self.angle, self.dx, self.dy, OBJ_SIZE))
            FIRE_SOUND.play()

    def bullet_operation(self):
        for bullet in self.missile:
            if 0 < bullet.x < DISPLAY_WIDTH and 0 < bullet.y < DISPLAY_HEIGHT:
                bullet.x += bullet.speed_x
                bullet.y += bullet.speed_y
            else:
                self.missile.pop(self.missile.index(bullet))


def main_loop():
    game_over = False
    pygame.display.set_caption("Battle city")
    main_player = Player(250, 350, 2, 0, load_level())
    while not game_over:
        TIMER.tick(60)
        GAME_DISPLAY.fill((0, 0, 0))
        BEST_MUSIC.set_volume(0.1)
        # BEST_MUSIC.play()
        for bul in main_player.missile:
            bul.draw(GAME_DISPLAY, MISSILE)
            main_player.bullet_operation()

        if main_player.missile:
            if not missile_collision(main_player.missile, X_OR_Y_MAP):
                main_player.missile.pop(0)
        main_player.draw(GAME_DISPLAY, PLAYER_SPRITE)
        for elements in main_player.map_game:
            elements.draw(GAME_DISPLAY)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
        keys = pygame.key.get_pressed()
        main_player.player_control(keys)
        pygame.display.update()
    pygame.quit()


class Blocks(GameObject):
    def __init__(self, x, y, block_type, size):
        GameObject.__init__(self, x, y, size)
        self.block_type = block_type

    def draw(self, game_display, ):

        if self.block_type == 'IRON':
            game_display.blit(IRON_BRICK, (self.x, self.y))
        elif self.block_type == 'BUSH':
            game_display.blit(BUSH, (self.x, self.y))
        elif self.block_type == 'BRICK':
            game_display.blit(BRICK, (self.x, self.y))
        elif self.block_type == 'IRON_FLOOR':
            game_display.blit(IRON_FLOOR, (self.x, self.y))
        elif self.block_type == 'WATER':
            game_display.blit(WATER, (self.x, self.y))


def load_level():
    filename = 'levels/' + '1'
    if not os.path.isfile(filename):
        raise AssertionError()
    game_map = []
    file = open(filename, 'r')
    data = file.read().split('\n')
    file.close()
    x, y = 0, 0
    for row in data:
        for char in row:
            if char == '#':
                game_map.append(Blocks(x, y, "BRICK", OBJ_SIZE))
                RECT_MAP.append(pygame.Rect(x, y, OBJ_SIZE, OBJ_SIZE))
                X_OR_Y_MAP.append((x, y))
            elif char == '@':
                game_map.append(Blocks(x, y, 'IRON', OBJ_SIZE))
                RECT_MAP.append(pygame.Rect(x, y, OBJ_SIZE, OBJ_SIZE))
                X_OR_Y_MAP.append((x, y))
            elif char == '%':
                game_map.append(Blocks(x, y, 'BUSH', OBJ_SIZE))
            elif char == '~':
                game_map.append(Blocks(x, y, 'WATER', OBJ_SIZE))
            elif char == '-':
                game_map.append(Blocks(x, y, 'IRON_FLOOR', OBJ_SIZE))
            x += OBJ_SIZE
        x = 0
        y += OBJ_SIZE
    return game_map


def missile_collision(missile: list, rec_object):
    for elem in rec_object:
        if elem[0] <= missile[0].x <= elem[0] + OBJ_SIZE:
            if elem[1] <= missile[0].y <= elem[1] + OBJ_SIZE:
                return False
    return True


if __name__ == "__main__":
    start_screen()
