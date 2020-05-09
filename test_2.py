import settings as s
import constant as c
import random
import GameObject as go
from GameObject import Missile
from GameObject import collision as co
from collections import Counter
import pygame
import Tank
import unittest

import LoadLevel


class Test(unittest.TestCase):
    def with_other_enemy_collision(self):
        enemy_l = [Tank.Enemy(100, 10, None, None, None), Tank.Enemy(15, 10, None, None, None),
                   Tank.Enemy(9, 10, None, None, None)]
        rec_l = []
        player_rect = pygame.Rect(15, 10, 26, 26)
        bool_l = []
        for elem in enemy_l:
            rec_l.append(pygame.Rect(elem.x, elem.y, 26, 26))
        rec_l.remove(player_rect)
        for elem in rec_l:
            data = player_rect.colliderect(elem)
            bool_l.append(data)
        if 1 in bool_l:
            return True
        return False

    def test_check(self):
        self.assertTrue(self.with_other_enemy_collision())
