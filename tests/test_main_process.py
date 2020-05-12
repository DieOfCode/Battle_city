import pygame
import unittest
from tank.Tank import *
from score.Score import *
from tank.Tank import *
from main_processes import LoadLevel
from main_processes import BattleCity


class Test(unittest.TestCase):
    def setUp(self):
        self.test_main = BattleCity.MainFunc(game_score=0, level_map=LoadLevel.load_level("test_level"),
                                             enemy_in_game=[], level=1.5)

    def test_load_level_and_resp_position(self):
        test_resp_map = LoadLevel.RESP_POSITION
        for elem in self.test_main.level_map:
            self.assertNotIn((elem.x, elem.x), test_resp_map)

    def test_create_enemy(self):
        tank_type = random.choice(self.test_main.current_level) if self.test_main.current_level else None
        self.test_main.create_tank(tank_type)
        self.assertTrue(self.test_main.enemy_in_game[0].kind == "casual")
