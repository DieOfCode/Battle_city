import unittest
from game_object.tank import Enemy, Player
from game_object.game_object import Missile, GameObject, Blocks, Bonus
from game import battle_city
import settings
from constant import constant


class BlockTest(unittest.TestCase):
    def setUp(self):
        self.test_enemy = Enemy(enemies=[Enemy(x=150, y=15, kind="casual", enemies=[], level_map=None)], x=1, y=1,
                                kind="hurt",
                                level_map=None)
        self.test_enemy.enemies.append(Enemy(x=self.test_enemy.x, y=self.test_enemy.y, kind=self.test_enemy.kind,
                                             enemies=self.test_enemy.enemies, level_map=None))
        self.test_player = Player(145, 375, enemies=self.test_enemy.enemies, count_of_enemies=[], level_map=None,
                                  bonus_on_level=None)
        self.test_player.missile.append(
            Missile(self.test_player.x + 4, self.test_player.y + 4, self.test_player.angle, self.test_player.dx,
                    self.test_player.dy, constant.OBJ_SIZE / 2))
        self.test_enemy.missile.append(
            Missile(self.test_player.x + 4, self.test_player.y + 4, self.test_player.angle, self.test_player.dx,
                    self.test_player.dy, constant.OBJ_SIZE / 2))

    def test_initialization(self):
        test_game_object = GameObject(50, 50, constant.OBJ_SIZE)
        self.assertTrue(isinstance(test_game_object, GameObject))

    def test_block_init(self):
        block_object = Blocks(0, 0, "WATER", constant.OBJ_SIZE)
        self.assertTrue(isinstance(block_object, Blocks))

    def test_blocks_equality(self):
        water = Blocks(0, 0, "WATER", constant.OBJ_SIZE)
        iron = Blocks(0, 0, "IRON", constant.OBJ_SIZE)
        self.assertFalse(water == iron)

    def test_terrain_draw(self):
        game_display = settings.GAME_DISPLAY
        water = Blocks(0, 0, 25, 'WATER')
        iron = Blocks(0, 0, 25, 'IRON')
        bush = Blocks(0, 0, 25, 'BUSH')
        brick = Blocks(0, 0, 25, 'BRICK')

        water.draw(game_display)
        iron.draw(game_display)
        bush.draw(game_display)
        brick.draw(game_display)
        self.assertTrue(True)

    def test_enemy_init(self):
        test_enemy = battle_city.Enemy(0, 0, 5, constant.OBJ_SIZE, [], "hurt")
        self.assertTrue(isinstance(test_enemy, battle_city.Enemy))

    def test_bonus_init(self):
        test_bonus = Bonus(1, 1, "LIFE")
        self.assertTrue(isinstance(test_bonus, GameObject))

    def test_missile_move(self):
        while self.test_player.missile:
            Missile.bullet_operation(self.test_player.missile)
        self.assertTrue(len(self.test_player.missile) == 0)

    def test_collision_with_player(self):
        self.assertTrue(Missile.collision_with_player(self.test_enemy.missile, self.test_player))
