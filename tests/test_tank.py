import unittest
from game_object.tank import Enemy, Player, Artillery
from game_object.game_object import Missile, Bomb, Bonus
import settings
from constant.constant import OBJ_SIZE
from game.load_level import LoadLevel


class TestTank(unittest.TestCase):
    def setUp(self):
        self.test_load_level = LoadLevel()
        self.test_level = self.test_load_level.load_level(1.5)
        self.test_enemy = Enemy(
            enemies=[Enemy(x=150, y=15, kind="fast", enemies=[], level_map=None)], x=1, y=1, kind="hurt",
            level_map=self.test_level)
        self.test_enemy.enemies.append(Enemy(x=self.test_enemy.x, y=self.test_enemy.y, kind=self.test_enemy.kind,
                                             enemies=self.test_enemy.enemies, level_map=self.test_level))
        self.test_enemy.direction = 180
        self.test_player = Player(145, 375, enemies=self.test_enemy.enemies, count_of_enemies=2,
                                  bonus_on_level=[Bonus(145, 375, "LIFE")], level_map=self.test_level)
        test_bomb = Bomb(100, 100)
        self.test_player.bomb.append(test_bomb)
        self.test_player.level_map.append(test_bomb)
        self.test_artillery = Artillery(300, 300, level_map=self.test_level)

    def test_type(self):
        self.assertEqual(self.test_enemy.speed, 2)

    def test_move_enemy(self):
        self.test_enemy.make_move(self.test_player)
        self.test_enemy.update_position(settings.GAME_DISPLAY)
        self.assertEqual(self.test_enemy.y, 2.0)

    def test_shoot(self):
        self.test_enemy.shoot(self.test_enemy.direction)
        self.assertTrue(len(self.test_enemy.missile) == 1 and self.test_enemy.missile[0].direction_y == 1)

    def test_collision_with_enemy(self):
        self.assertTrue(self.test_player.with_enemy_collision((2, 1)))

    def test_collision_with_other_tank(self):
        self.assertTrue(self.test_enemy.with_other_tank_collision((150, 1), self.test_player))

    def test_player_shoot(self):
        self.test_player.missile.append(Missile(151, 16, 1, 1, 1, OBJ_SIZE))
        self.test_player.collision_missile_with_enemy()
        self.assertTrue(len(self.test_player.kill_enemy) == 1)

    def test_bomb_del(self):
        for bomb in self.test_player.bomb:
            bomb.tick_life += 200
            self.test_player.del_bomb(bomb)
            self.assertTrue(self.test_player.bomb == [])

    def test_bomb_kill_enemy(self):
        test_kill_bomb = Bomb(1, 1)
        self.test_player.bomb.append(test_kill_bomb)
        self.test_player.level_map.append(test_kill_bomb)
        self.test_player.enemy_collision_with_bomb()
        self.assertTrue(len(self.test_player.kill_enemy) == 1)

    def test_collision_with_bonus(self):
        self.test_player.collision_with_bonus()
        self.assertTrue(self.test_player.hp == 200)

    def test_artillery_shoot(self):
        self.test_artillery.count_for_shoot = 150
        self.test_artillery.make_boom(self.test_player, self.test_enemy.enemies)
        self.assertTrue(self.test_player.hp < 0)

    def test_artillery_rotate(self):
        self.test_artillery.artillery_rotate(self.test_player)
        self.assertTrue(self.test_artillery.angle == 90)
