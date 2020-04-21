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
from BattleCity import main_loop




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
        # START_SCREEN.play()
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
            BUTTON_MUSIC.play()
            main_loop()
        pygame.display.update()
        TIMER.tick(FPS)
