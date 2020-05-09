import random
import os
import math
import datetime

import copy
from Tank import *
from GameObject import *
import Screen
import settings as s
from constant import *
import Score


class MainFunc:
    def __init__(self, level, level_map, game_score, enemy_in_game=[], i=0, ):
        self.level = level
        self.enemy_in_game = enemy_in_game
        self.i = i
        self.type_for_level = dict(s.LEVELS_ENEM)
        self.current_level = list(self.type_for_level[self.level])
        self.count_of_enemy = len(self.type_for_level[self.level])
        self.game_over = Screen.Screen()
        self.game_score = game_score
        self.best_score = Score.load_score()
        self.is_game_over = False
        self.level_map = level_map
        self.respawn_position = LoadLevel.RESP_POSITION
        self.using_position = []

    def main_loop(self):
        # START_SCREEN.stop()

        pygame.display.set_caption("Battle city")
        main_player = Player(145, 375, 1, enemies=self.enemy_in_game, count_of_enemies=self.count_of_enemy)
        main_screen = Screen.Screen()

        while not self.is_game_over:
            s.TIMER.tick(60)
            s.GAME_DISPLAY.fill((0, 0, 0))
            # BEST_MUSIC.set_volume(0.1)
            # BEST_MUSIC.play()
            main_screen.draw_sidebar(main_player, main_player.count_of_enemies)

            main_player.collision_missile_with_enemy()
            main_player.draw(s.GAME_DISPLAY, PLAYER_SPRITE, (main_player.x, main_player.y))
            self.respawn(main_player)
            for elements in self.level_map:
                elements.draw(s.GAME_DISPLAY)
            for bul in main_player.missile:
                bul.draw(s.GAME_DISPLAY, MISSILE)
                Missile.bullet_operation(main_player.missile)
            if not self.enemy_in_game \
                    and not self.current_level \
                    and main_player.life != 0:
                if self.level < 3:
                    main_screen.next_level_screen(main_player, self.level, self.game_score)
                else:
                    main_screen.victory_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_game_over = True
            keys = pygame.key.get_pressed()
            main_player.player_control(keys, level_map=self.level_map)
            pygame.display.update()
        pygame.quit()

    def respawn(self, player: Player):

        tank_type = random.choice(self.current_level) if self.current_level else None
        self.create_tank(tank_type)
        for elem in self.enemy_in_game:
            elem.shoot(elem.direction)
            for bullet in elem.missile:
                bullet.draw(s.GAME_DISPLAY, MISSILE)
                Missile.bullet_operation(elem.missile)
                if Missile.collision_with_player(elem.missile,
                                                 pygame.Rect(player.x, player.y, OBJ_SIZE, OBJ_SIZE)):
                    player.life -= 1
                if self.game_over_func(player, elem):
                    self.end_game_action(player)
            elem.make_move(player, level_map=self.level_map)
            elem.update_position(s.GAME_DISPLAY)

    def end_game_action(self, player):
        self.level_map = LoadLevel.load_level(1)
        s.ENEMY_IN_LEVEL = len(s.LEVELS_ENEM[1])
        self.game_score = Score.get_score(player)
        if self.best_score < self.game_score:
            Score.save_score(self.game_score)
        self.game_over.game_over_screen()

    def create_tank(self, tank_type):
        if tank_type:
            position = random.choice(self.respawn_position)
            if len(self.enemy_in_game) < 4 and position not in self.using_position:
                self.add_colision_position(position)
                if len(self.using_position) == 36:
                    self.using_position.clear()
                self.enemy_in_game.append(
                    Enemy(position[0], position[1], 0, kind=tank_type, enemies=self.enemy_in_game))
                self.current_level.remove(tank_type)

    def add_colision_position(self, position):
        self.using_position.append(position)
        self.using_position.append((position[0] + 16, position[1]))
        self.using_position.append((position[0], position[1] + 16))
        self.using_position.append((position[0] + 16, position[1] + 16))
        self.using_position.append((position[0] - 16, position[1]))
        self.using_position.append((position[0], position[1] - 16))
        self.using_position.append((position[0] - 16, position[1] - 16))
        self.using_position.append((position[0] - 16, position[1]))
        self.using_position.append((position[0], position[1] + 16))
        self.using_position.append((position[0] - 16, position[1] + 16))
        self.using_position.append((position[0] + 16, position[1] - 16))

    def game_over_func(self, player: Player, enemy):
        return player.life == 0 or \
               Missile.missile_collision(player, self.level_map) or \
               Missile.missile_collision(enemy, self.level_map)
