import pygame
import unittest
from tank.Tank import *
from score.Score import *


class Test(unittest.TestCase):

    def test_get_score(self):
        test_player = Player(145, 375, 1, enemies=[], count_of_enemies=[])
        test_player.kill_enemy["hurt"] += 3
        test_player.kill_enemy["casual"] += 3
        self.assertEqual(750, get_score(test_player))

    def test_load_score(self):
        self.assertTrue(load_score())
