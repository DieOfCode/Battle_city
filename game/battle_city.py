from game.load_level import LoadLevel
from game_object.tank import Player, Artillery, Enemy
from game_object.game_object import Missile, Blocks, Bonus
import pygame
import random
from screen import screen
import settings
from constant.constant import PLAYER_SPRITE, MISSILE, OBJ_SIZE, TANK_SIZE
from game import score


class Game:
    def __init__(self, level, game_score, enemy_in_game=[], i=0):
        self.load_level = LoadLevel()
        self.level = level
        self.level_map = self.load_level.load_level(level)
        self.enemy_in_game = enemy_in_game
        self.i = i
        self.type_for_level = dict(settings.LEVELS_ENEM)
        self.count_of_artillery = 0
        self.artillery_position = self.load_level.artillery_position
        self.current_level = list(self.type_for_level[self.level])
        self.count_of_enemy = len(self.type_for_level[self.level]) + len(self.artillery_position)
        self.game_over = screen.Screen()
        self.game_score = game_score
        self.best_score = score.load_score()
        self.is_game_over = False
        self.respawn_position_for_enemy = self.load_level.enemy_respawn_position
        self.bonus_position = self.load_level.bonus_respawn_position
        self.using_position = []
        self.bonus_for_level = list(settings.LEVEL_BONUS[self.level])
        self.bonus_in_game = []
        self.period_for_bonus = 0
        self.artillery_in_game = []

        self.all_target_for_art = []

    def main_loop(self):
        # START_SCREEN.stop()
        pygame.display.set_caption("Battle city")
        main_player = Player(145, 375, enemies=self.enemy_in_game, count_of_enemies=self.count_of_enemy,
                             level_map=self.level_map, bonus_on_level=self.bonus_in_game)
        self.all_target_for_art.append(main_player)
        main_screen = screen.Screen()

        while not self.is_game_over:
            settings.TIMER.tick(60)
            settings.GAME_DISPLAY.fill((0, 0, 0))
            main_screen.draw_sidebar(main_player, main_player.count_of_enemies, self.level)
            main_player.collision_missile_with_enemy()
            main_player.draw(settings.GAME_DISPLAY, PLAYER_SPRITE, (main_player.x, main_player.y))
            self.respawn(main_player)
            main_player.collision_with_bonus()
            self.game_over_func(main_player, main_player)

            for elements in self.level_map:
                elements.draw(settings.GAME_DISPLAY)
            for bul in main_player.missile:
                bul.draw(settings.GAME_DISPLAY, MISSILE)
                Missile.bullet_operation(main_player.missile)
            for bomb in main_player.bomb:
                main_player.del_bomb(bomb)
            self.check_bonus_status()
            self.period_for_bonus += 1
            main_player.enemy_collision_with_bomb()
            if self.load_level.artillery_position:
                self.create_artillery()
            if not self.enemy_in_game \
                    and not self.current_level \
                    and main_player.hp != 0:
                if self.level < 4:
                    main_screen.next_level_screen(main_player, self.level, self.game_score)
                else:
                    main_screen.victory_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_game_over = True
            main_player.player_control(pygame.key.get_pressed())
            pygame.display.update()
        pygame.quit()

    def create_artillery(self):
        for position in self.artillery_position:
            if self.count_of_artillery < len(self.artillery_position):
                self.enemy_in_game.append(Artillery(position[0], position[1], self.level_map))
                self.count_of_artillery += 1

    def check_bonus_status(self):
        if self.period_for_bonus == 150:
            self.period_for_bonus = 0
            self.respawn_bonus()
        if self.bonus_in_game:
            for bonus in self.bonus_in_game:
                bonus.draw_bonus()
                bonus.life_tick -= 1
                if bonus.life_tick == 0:
                    self.bonus_in_game.remove(bonus)

    def respawn(self, player: Player):
        tank_type = random.choice(self.current_level) if self.current_level else None
        self.create_tank(tank_type, player)
        for elem in self.enemy_in_game:
            if elem.kind == "artillery":
                elem.make_boom(player, self.enemy_in_game)
                elem.artillery_rotate(player)
            else:
                elem.shoot(elem.direction)
                for bullet in elem.missile:
                    bullet.draw(settings.GAME_DISPLAY, MISSILE)
                    Missile.bullet_operation(elem.missile)
                    if Missile.collision_with_player(elem.missile,
                                                     pygame.Rect(player.x, player.y, OBJ_SIZE, OBJ_SIZE)):
                        player.hp -= elem.damage
                elem.make_move(player)
                elem.update_position(settings.GAME_DISPLAY)
                self.game_over_func(player, elem)

    def end_game_action(self):
        self.level_map = self.load_level.load_level(1)
        settings.ENEMY_IN_LEVEL = len(settings.LEVELS_ENEM[1])
        if self.best_score < self.game_score:
            score.save_score(self.game_score)
        self.game_over.game_over_screen()

    def create_tank(self, tank_type, player):
        if tank_type:
            position = random.choice(self.respawn_position_for_enemy)
            if len(self.enemy_in_game) < 4 \
                    and position not in self.using_position \
                    and not self.check_empty_position(position, player):
                self.add_collision_position(position)
                if len(self.using_position) == 36:
                    self.using_position.clear()
                new_enemy = Enemy(position[0], position[1], kind=tank_type, enemies=self.enemy_in_game,
                                  level_map=self.level_map)
                self.enemy_in_game.append(new_enemy)
                self.all_target_for_art.append(new_enemy)
                self.current_level.remove(tank_type)

    def add_collision_position(self, position):
        self.using_position.append(position)
        for elem_x in [position[0] + 16, position[0], position[0] - 16]:
            for elem_y in [position[1], position[1] - 16, position[1] + 16]:
                self.using_position.append((elem_x, elem_y))

    def game_over_func(self, player: Player, tank):
        if player.hp <= 0 or \
                Missile.missile_collision(tank, self.level_map):
            self.end_game_action()

    def respawn_bonus(self):
        bonus_type = random.choice(self.bonus_for_level) if self.bonus_for_level else None
        if bonus_type:
            position = random.choice(self.bonus_position)
            self.bonus_in_game.append(Bonus(position[0], position[1], bonus_type))
            self.bonus_for_level.remove(bonus_type)

    def check_empty_position(self, position, player: Player):
        collision_object = self.enemy_in_game + [player] + player.bomb
        rec_list = []
        collide_list = []
        for elem in collision_object:
            if elem is Blocks:
                rec_list.append(pygame.Rect(elem.x, elem.y, OBJ_SIZE, OBJ_SIZE))
            else:
                rec_list.append(pygame.Rect(elem.x, elem.y, TANK_SIZE, TANK_SIZE))
        for elem in rec_list:
            collide_list.append(pygame.Rect(position[0], position[1], TANK_SIZE, TANK_SIZE).colliderect(elem))
        return 1 in collide_list
