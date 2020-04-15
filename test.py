import unittest
import BattleCity as bs
import settings as my_s
import datetime


class Test(unittest.TestCase):
    def test_test(self):
        self.assertTrue(1 == 1)

    def test_initialization(self):
        test_game_object = bs.GameObject(50, 50, my_s.OBJ_SIZE)
        self.assertTrue(isinstance(test_game_object, bs.GameObject))

    def test_block_init(self):
        block_object = bs.Blocks(0, 0, "WATER", my_s.OBJ_SIZE)
        self.assertTrue(isinstance(block_object, bs.Blocks))

    def test_blocks_equality(self):
        water = bs.Blocks(0, 0, "WATER", my_s.OBJ_SIZE)
        iron = bs.Blocks(0, 0, "IRON", my_s.OBJ_SIZE)
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
        test_enemy = bs.Enemy(0, 0, 5, my_s.OBJ_SIZE, [], "hurt")
        self.assertTrue(isinstance(test_enemy, bs.Enemy))

    def test_button_drawing(self):
        done = False
        if bs.create_menu_button(20, 300):
            done = True
        self.assertTrue(done)

    def test_mes_to_scr(self):
        bs.message_to_screen("BATTLE CITY", my_s.RED,
                             my_s.DISPLAY_WIDTH, my_s.DISPLAY_HEIGHT, my_s.FONT)
        self.assertTrue(True)

    def test_main_game_loop_cl(self):
        bs.main_loop()
        self.assertTrue(True)
