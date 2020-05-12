import unittest
import pygame

from screen.Screen import *


class Test(unittest.TestCase):
    def setUp(self):
        self.test_screen = Screen()
        self.test_button = self.test_screen.create_menu_button(DISPLAY_WIDTH - 110, DISPLAY_HEIGHT - 40)

    def test_any_game_screen(self):
        try:
            i=0
            self.test_screen.victory_screen()
            self.test_screen.next_level_screen(player=Player(145, 375, 1, enemies=[], count_of_enemies=[]),
                                               num_of_level=1, game_score=100)

            self.test_screen.start_screen()
            self.assertTrue(True)
        except Exception:
            self.assertTrue(False)