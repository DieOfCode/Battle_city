import unittest
from random import choice
from game_object.tank import Player
from game import battle_city
from game import score


class TestGameFunction(unittest.TestCase):
    def setUp(self):
        self.test_game = battle_city.Game(game_score=0,
                                          enemy_in_game=[], level=1.5)
        self.test_player = Player(145, 375, enemies=[], count_of_enemies=[], level_map=[], bonus_on_level=[])

    def test_load_level_and_resp_position(self):
        test_resp_map = self.test_game.respawn_position_for_enemy
        for elem in self.test_game.level_map:
            self.assertNotIn((elem.x, elem.x), test_resp_map)

    def test_create_enemy(self):
        tank_type = choice(self.test_game.current_level) if self.test_game.current_level else None
        self.test_game.create_tank(tank_type, self.test_player)
        self.assertTrue(self.test_game.enemy_in_game[0].kind == "casual")

    def test_respawn(self):
        try:
            self.test_game.respawn(self.test_player)
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    def test_creat_artillery(self):
        pass


class TestScore(unittest.TestCase):

    def test_get_score(self):
        test_player = Player(145, 375, enemies=[], count_of_enemies=[], level_map=[], bonus_on_level=[])
        test_player.kill_enemy["hurt"] += 3
        test_player.kill_enemy["casual"] += 3
        self.assertEqual(750, score.get_score(test_player))

    def test_load_score(self):
        self.assertTrue(score.load_score())
