import unittest
import pygame

from screen.Screen import *


class Test(unittest.TestCase):
    def setUp(self):
        self.test_screen = Screen()

    def test_create_button(self):
        self.assertTrue(self.test_screen.create_menu_button(DISPLAY_WIDTH - 110, DISPLAY_HEIGHT - 40))

    def test_draw_sidebar(self):
        Screen.draw_sidebar(Player(1, 1, 1, [], 1), 4, 1)
        self.assertTrue(True)
