from constant import constant
import settings
import random
from game_object.game_object import Missile, Bomb
from game_object.game_object import collision
from collections import Counter
import pygame


class Tank:
    def __init__(self, x, y, level_map=None):
        self.x = x
        self.y = y
        self.speed = 1
        self.dx = 0
        self.dy = -1.0
        self.size = constant.TANK_SIZE
        self.angle = 0
        self.level_map = level_map

    def draw(self, game_display, img, position):
        rotate_image = pygame.transform.rotate(img, self.angle)
        game_display.blit(rotate_image, position)

    def tank_collision_with_wall(self, new_position):
        player_rect = pygame.Rect(new_position[0], new_position[1], 26, 26)
        bool_l = []
        for elem in self.level_map:
            if elem.block_type not in ["BUSH", "BOMB"]:
                new_rect = pygame.Rect(elem.x, elem.y, 16, 16)
                data = player_rect.colliderect(new_rect)
                bool_l.append(data)
        return 1 in bool_l


class Player(Tank):
    def __init__(self, x, y, enemies, count_of_enemies, level_map, bonus_on_level):
        Tank.__init__(self, x, y, level_map)
        self.angle = 0
        self.missile = []
        self.hp = 150
        self.enemies = enemies
        self.count_of_enemies = count_of_enemies
        self.kill_enemy = Counter()
        self.score = 0
        self.enemies_pos = []
        self.damage = 50
        self.level_map = level_map
        self.bomb = []
        self.bonus_on_level = bonus_on_level

    def player_control(self, keys):

        if keys[pygame.K_LEFT] \
                and self.x > 0:
            self.angle = 90
            self.dx = -1
            self.dy = 0
            if not self.tank_collision_with_wall((self.x - self.speed, self.y)) \
                    and not self.with_enemy_collision((self.x - self.speed, self.y)):
                self.x -= self.speed

        elif keys[pygame.K_RIGHT] \
                and self.x < settings.GAME_DISP_WIDTH:
            self.angle = 270
            self.dx = 1
            self.dy = 0
            if not self.tank_collision_with_wall((self.x + self.speed, self.y)) \
                    and not self.with_enemy_collision((self.x + self.speed, self.y)):
                self.x += self.speed

        elif keys[pygame.K_UP] \
                and self.y > 0:
            self.angle = 0
            self.dx = 0
            self.dy = -1
            if not self.tank_collision_with_wall((self.x, self.y - self.speed)) \
                    and not self.with_enemy_collision((self.x, self.y - self.speed)):
                self.y -= self.speed

        elif keys[pygame.K_DOWN] \
                and self.y < settings.DISPLAY_HEIGHT - 30:
            self.angle = 180
            self.dx = 0
            self.dy = 1
            if not self.tank_collision_with_wall((self.x, self.y + self.speed)) \
                    and not self.with_enemy_collision((self.x, self.y + self.speed)):
                self.y += self.speed

        if keys[pygame.K_SPACE] and len(self.missile) < 1:
            self.missile.append(Missile(self.x + 4, self.y + 4, self.angle, self.dx, self.dy, constant.OBJ_SIZE))
            constant.FIRE_SOUND.set_volume(10)
            constant.FIRE_SOUND.play()
        if keys[pygame.K_z] \
                and len(self.bomb) < 3 \
                and not Bomb.collision_with_other_bomb(self.bomb, Bomb(self.x, self.y)):
            n_bomb = Bomb(self.x, self.y)
            self.level_map.append(n_bomb)
            self.bomb.append(n_bomb)

    def del_bomb(self, one_bomb: Bomb):
        one_bomb.tick_life += 1
        if one_bomb.tick_life > 200 and self.bomb:
            one_bomb.tick_life = 0
            self.bomb.remove(one_bomb)
            one_bomb.draw_explosion()
            self.level_map.remove(one_bomb)

    def collision_missile_with_enemy(self):
        for elem in self.enemies:
            for mis in self.missile:
                if pygame.Rect(mis.x, mis.y, 16, 16).colliderect(pygame.Rect(elem.x, elem.y, 26, 26)):
                    self.missile.remove(mis)
                    elem.hp -= self.damage
                    if elem.hp <= 0:
                        self.kill_enemy[elem.kind] += 1
                        self.enemies.remove(elem)
                        self.count_of_enemies -= 1

    def with_enemy_collision(self, new_position):
        player_rect = pygame.Rect(new_position[0], new_position[1], 26, 26)
        bool_l = []
        for elem in self.enemies:
            enemy_rect = pygame.Rect(elem.x, elem.y, 26, 26)
            bool_l.append(player_rect.colliderect(enemy_rect))
        return 1 in bool_l

    def enemy_collision_with_bomb(self):
        for enemy in self.enemies:
            for bomb in self.bomb:
                enemy_rect = pygame.Rect(enemy.x, enemy.y, 26, 26)
                if enemy_rect.colliderect(pygame.Rect(bomb.x, bomb.y, 26, 26)):
                    self.level_map.remove(bomb)
                    bomb.draw_explosion()
                    self.bomb.remove(bomb)
                    self.kill_enemy[enemy.kind] += 1
                    self.enemies.remove(enemy)

    def collision_with_bonus(self):
        player_rect = pygame.Rect(self.x, self.y, 26, 26)
        for bonus in self.bonus_on_level and self.bonus_on_level:
            if player_rect.colliderect(pygame.Rect(bonus.x, bonus.y, 26, 26)):
                if bonus.bonus_type == "LIFE":
                    self.hp += 50
                    self.bonus_on_level.remove(bonus)
                if bonus.bonus_type == "DAMAGE":
                    self.damage += 200
                    self.bonus_on_level.remove(bonus)
                if bonus.bonus_type == "SPEED":
                    self.speed += 1
                    self.bonus_on_level.remove(bonus)


class Enemy(Tank):
    def __init__(self, x, y, kind, enemies, level_map, hp=100, image=None, missile=[],
                 artillery_position=None):
        Tank.__init__(self, x, y, level_map)
        self.missile = missile
        self.angle = 0
        self.missile = []
        self.image = image
        self.hp = hp
        self.direction = 180
        self.kind = kind
        self.enemies = enemies
        self.damage = 50
        self.artillery_position = artillery_position
        self.level_map = level_map

        if kind == "casual":
            self.image = constant.CASUAL_ENEMY
            self.speed = 0.8
            self.hp = 100
        if kind == "fast":
            self.image = constant.FAST_ENEMY
            self.speed = 3
            self.hp = 50
        if kind == "hurt":
            self.image = constant.POPA_BOL_ENEMY
            self.speed = 2
            self.hp = 200
            self.damage = 100

    def make_move(self, player: Player):
        if self.direction == 0:
            if not self.tank_collision_with_wall((self.x, self.y - self.speed)) \
                    and self.y > 0 \
                    and not self.with_other_tank_collision((self.x, self.y - self.speed), player):
                self.direction = 0
                self.dy -= self.speed
                self.dx = 0
            else:
                self.direction = random.choice([180, 90, 270])
        if self.direction == 180:
            if not self.tank_collision_with_wall((self.x, self.y + self.speed)) \
                    and self.y < settings.DISPLAY_HEIGHT - 30 \
                    and not self.with_other_tank_collision((self.x, self.y + self.speed), player):
                self.direction = 180
                self.dy += self.speed
                self.dx = 0
            else:
                self.direction = random.choice([0, 90, 270])
        if self.direction == 90:
            if not self.tank_collision_with_wall((self.x - self.speed, self.y)) \
                    and self.x > 0 \
                    and not self.with_other_tank_collision((self.x - self.speed, self.y), player):

                self.direction = 90
                self.dx -= self.speed
                self.dy = 0
            else:
                self.direction = random.choice([0, 180, 270])
        if self.direction == 270:
            if not self.tank_collision_with_wall((self.x + self.speed, self.y)) \
                    and self.x < settings.GAME_DISP_WIDTH \
                    and not self.with_other_tank_collision((self.x + self.speed, self.y), player):
                self.direction = 270
                self.dx += self.speed
                self.dy = 0
            else:
                self.direction = random.choice([0, 90, 180])

    def with_other_tank_collision(self, new_position, player: Player):
        rec_l = [pygame.Rect(player.x, player.y, 26, 26)]
        enemy_rect = pygame.Rect(self.x, self.y, 26, 26)
        new_player_rect = pygame.Rect(new_position[0], new_position[1], 26, 26)
        bool_l = []
        for elem in self.enemies:
            rec_l.append(pygame.Rect(elem.x, elem.y, 26, 26))
        rec_l.remove(enemy_rect)
        for elem in rec_l:
            data = new_player_rect.colliderect(elem)
            bool_l.append(data)
        return 1 in bool_l

    def shoot(self, direction):
        traction_x = 0
        traction_y = 0
        if direction == 270:
            traction_x = 1
            traction_y = 0
        elif direction == 90:
            traction_x = -1
            traction_y = 0
        elif direction == 0:
            traction_x = 0
            traction_y = -1
        elif direction == 180:
            traction_x = 0
            traction_y = 1
        missile_e = Missile(self.x + 4, self.y + 4, direction, traction_x, traction_y, constant.OBJ_SIZE)
        if len(self.missile) < 1:
            self.missile.append(missile_e)

    def update_position(self, game_display):
        self.x += self.dx
        self.y += self.dy
        self.draw(game_display, pygame.transform.rotate(self.image, self.direction), (self.x, self.y))
        self.dx = 0
        self.dy = 0


class Artillery(Tank):
    def __init__(self, x, y, level_map):
        Tank.__init__(self, x, y, level_map)
        self.x = x
        self.y = y
        self.image = constant.ART_ENEMY
        self.damage = 400
        self.hp = 100
        self.aim_position = None
        self.count_for_shoot = 0
        self.explode_count = 0
        self.kind = "artillery"

    def make_boom(self, main_player, enemy_in_game):
        self.draw(settings.GAME_DISPLAY, constant.ART_ENEMY, (self.x, self.y))
        all_target = enemy_in_game + [main_player]
        if not self.aim_position:
            self.aim_position = (main_player.x, main_player.y)
        if self.count_for_shoot < 150:
            settings.GAME_DISPLAY.blit(constant.AIM, self.aim_position)
        else:
            self.explode_count += 1
            for tank in all_target:
                if pygame.Rect(self.aim_position[0], self.aim_position[1], 26, 26).colliderect(
                        pygame.Rect(tank.x, tank.y, 26, 26)):
                    tank.hp -= self.damage
            if self.explode_count < 20:
                settings.GAME_DISPLAY.blit(constant.EXPLODE, (self.aim_position[0] + 6, self.aim_position[1] + 6))
            elif self.explode_count < 40:
                settings.GAME_DISPLAY.blit(constant.BIG_EXPLODE, self.aim_position)
            else:
                self.aim_position = None
                self.explode_count = 0
                self.count_for_shoot = 0
        self.count_for_shoot += 1

    def artillery_rotate(self, main_player):
        if main_player.x < self.x and main_player.y > self.y:
            self.angle = 90
        elif main_player.x > self.x and not main_player.y > self.y:
            self.angle = 270
        elif main_player.y > self.y:
            self.angle = 180
        else:
            self.angle = 0
