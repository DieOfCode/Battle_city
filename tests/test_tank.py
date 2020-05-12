import unittest
import pygame
from tank.Tank import *
from game_object.GameObject import *


class Test(unittest.TestCase):
    def setUp(self):
        self.test_enemy = Enemy(
            enemies=[Enemy(x=150, y=15, kind="casual", speed=0, enemies=[])], x=1, y=1, kind="hurt", speed=0)
        self.test_enemy.enemies.append(Enemy(x=self.test_enemy.x, y=self.test_enemy.y, kind=self.test_enemy.kind,
                                             enemies=self.test_enemy.enemies, speed=0))
        self.test_enemy.direction = 180
        self.test_player = Player(145, 375, 1, enemies=self.test_enemy.enemies, count_of_enemies=2)

    def test_type(self):
        self.assertEqual(self.test_enemy.speed, 2)

    def test_move_enemy(self):
        self.test_enemy.make_move(self.test_player, level_map=[])
        self.test_enemy.update_position(s.GAME_DISPLAY)
        self.assertEqual(self.test_enemy.y, 2.0)

    def test_shoot(self):
        self.test_enemy.shoot(self.test_enemy.direction)
        self.assertTrue(len(self.test_enemy.missile) == 1 and self.test_enemy.missile[0].direction_y == 1)

    def test_collision_with_enemy(self):
        self.assertTrue(self.test_player.with_enemy_collision((2, 1)))

    def test_collision_with_other_enemy(self):
        self.assertTrue(self.test_enemy.with_other_enemy_collision((150, 1)))

    def test_collision_with_player(self):
        self.assertFalse(with_player_collision((145, 375), self.test_player))

    def test_player_shoot(self):
        self.test_player.missile.append(Missile(151, 16, 1, 1, 1, c.OBJ_SIZE / 2))
        self.test_player.collision_missile_with_enemy()
        self.assertTrue(len(self.test_player.kill_enemy) == 1)
