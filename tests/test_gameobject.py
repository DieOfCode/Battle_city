import unittest
import pygame
from tank.Tank import *
from game_object.GameObject import *
from main_processes import BattleCity as bs
from constant_and_setting import settings as my_s
from constant_and_setting import constant as my_c


class Test(unittest.TestCase):
    def setUp(self):
        self.test_enemy = Enemy(enemies=[Enemy(x=150, y=15, kind="casual", speed=0, enemies=[])], x=1, y=1, kind="hurt",
                                speed=0)
        self.test_enemy.enemies.append(Enemy(x=self.test_enemy.x, y=self.test_enemy.y, kind=self.test_enemy.kind,
                                             enemies=self.test_enemy.enemies, speed=0))
        self.test_player = Player(145, 375, 1, enemies=self.test_enemy.enemies, count_of_enemies=[])
        self.test_player.missile.append(
            Missile(self.test_player.x + 4, self.test_player.y + 4, self.test_player.angle, self.test_player.dx,
                    self.test_player.dy, c.OBJ_SIZE / 2))
        self.test_enemy.missile.append(
            Missile(self.test_player.x + 4, self.test_player.y + 4, self.test_player.angle, self.test_player.dx,
                    self.test_player.dy, c.OBJ_SIZE / 2))

    def test_initialization(self):
        test_game_object = bs.GameObject(50, 50, my_c.OBJ_SIZE)
        self.assertTrue(isinstance(test_game_object, bs.GameObject))

    def test_block_init(self):
        block_object = bs.Blocks(0, 0, "WATER", my_c.OBJ_SIZE)
        self.assertTrue(isinstance(block_object, bs.Blocks))

    def test_blocks_equality(self):
        water = bs.Blocks(0, 0, "WATER", my_c.OBJ_SIZE)
        iron = bs.Blocks(0, 0, "IRON", my_c.OBJ_SIZE)
        self.assertFalse(water == iron)

    def test_terrain_draw(self):
        game_display = my_s.GAME_DISPLAY
        water = bs.Blocks(0, 0, 25, 'WATER')
        iron = bs.Blocks(0, 0, 25, 'IRON')
        bush = bs.Blocks(0, 0, 25, 'BUSH')
        brick = bs.Blocks(0, 0, 25, 'BRICK')

        water.draw(game_display)
        iron.draw(game_display)
        bush.draw(game_display)
        brick.draw(game_display)
        self.assertTrue(True)

    def test_enemy_init(self):
        test_enemy = bs.Enemy(0, 0, 5, my_c.OBJ_SIZE, [], "hurt")
        self.assertTrue(isinstance(test_enemy, bs.Enemy))

    def test_missile_move(self):
        while self.test_player.missile:
            Missile.bullet_operation(self.test_player.missile)
        self.assertTrue(len(self.test_player.missile) == 0)

    def test_collision_with_player(self):
        self.assertTrue(Missile.collision_with_player(self.test_enemy.missile, self.test_player))
