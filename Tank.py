import settings as s
import constant as c
import random
import GameObject as go
from GameObject import Missile
from GameObject import with_player_collision as co
from collections import Counter
import pygame
import LoadLevel


class Tank:
    def __init__(self, x, y, size=c.OBJ_SIZE):
        self.x = x
        self.y = y
        self.speed = 1
        self.dx = 0
        self.dy = -1.0
        self.size = size
        self.angle = 0
        self.rect = pygame.rect.Rect(self.x, self.y, c.OBJ_SIZE, c.OBJ_SIZE)

    def draw(self, game_display, img, position):
        rotate_image = pygame.transform.rotate(img, self.angle)
        game_display.blit(rotate_image, position)

    def tank_collision_with_wall(self, some_object, rec_object):
        for elem in rec_object:
            if elem.block_type != "BUSH":
                if elem.object_rect.x <= some_object.x <= elem.object_rect.x + c.OBJ_SIZE \
                        or elem.object_rect.x <= some_object.x + 25 <= elem.object_rect.x + c.OBJ_SIZE:
                    if elem.object_rect.y <= some_object.y <= elem.object_rect.y + c.OBJ_SIZE or elem.object_rect.y <= some_object.y \
                            + 25 <= elem.object_rect.y + c.OBJ_SIZE:
                        return False
        return True


class Player(Tank):
    def __init__(self, x, y, speed, enemies, count_of_enemies):
        Tank.__init__(self, x, y, speed)
        self.angle = 0
        self.missile = []
        self.life = 3
        self.enemies = enemies
        self.count_of_enemies = count_of_enemies
        self.kill_enemy = Counter()
        self.score = 0
        self.enemies_pos = []

    def player_control(self, keys, level_map):
        my_rect = pygame.Rect(self.x, self.y + 1, 26, 26)
        my_rect_2 = pygame.Rect(my_rect.topright[0] - 22, self.y + 1, 0, 0)
        my_rect_3 = pygame.Rect(self.x + 1, my_rect.topright[1] - 1, 0, 0)
        my_rect_4 = pygame.Rect(self.x + 1, my_rect.bottomright[1] - 24, 0, 0)

        if keys[pygame.K_LEFT] \
                and self.x > 0:
            self.angle = 90
            self.dx = -1
            self.dy = 0
            if self.tank_collision_with_wall(my_rect, level_map) \
                    and not self.with_enemy_collision((self.x - self.speed, self.y)):
                self.x -= self.speed

        elif keys[pygame.K_RIGHT] \
                and self.x < s.GAME_DISP_WIDTH:
            self.angle = 270
            self.dx = 1
            self.dy = 0
            if self.tank_collision_with_wall(my_rect_2, level_map) \
                    and not self.with_enemy_collision(
                (self.x + self.speed, self.y)):
                self.x += self.speed

        elif keys[pygame.K_UP] \
                and self.y > 0:
            self.angle = 0
            self.dx = 0
            self.dy = -1
            if self.tank_collision_with_wall(my_rect_3, level_map) \
                    and not self.with_enemy_collision((self.x, self.y - self.speed)):
                self.y -= self.speed

        elif keys[pygame.K_DOWN] \
                and self.y < s.DISPLAY_HEIGHT - 30:
            self.angle = 180
            self.dx = 0
            self.dy = 1
            if self.tank_collision_with_wall(my_rect_4, level_map) \
                    and not self.with_enemy_collision((self.x, self.y + self.speed)):
                self.y += self.speed

        if keys[pygame.K_SPACE] and len(self.missile) < 1:
            self.missile.append(Missile(self.x + 4, self.y + 4, self.angle, self.dx, self.dy, c.OBJ_SIZE / 2))
            # c.FIRE_SOUND.set_volume(10)
            # c.FIRE_SOUND.play()

    def collision_missile_with_enemy(self):
        for elem in self.enemies:
            for mis in self.missile:
                if elem.x < mis.x < elem.x + c.OBJ_SIZE \
                        and elem.y < mis.y < elem.y + c.OBJ_SIZE:
                    self.missile.remove(mis)
                    self.kill_enemy[elem.kind] += 1
                    self.enemies.remove(elem)
                    self.count_of_enemies -= 1

    def with_enemy_collision(self, new_position):
        player_rect = pygame.Rect(new_position[0], new_position[1], 26, 26)
        bool_l = []
        for elem in self.enemies:
            enemy_rect = pygame.Rect(elem.x, elem.y, 26, 26)
            data = player_rect.colliderect(enemy_rect)
            bool_l.append(data)

        return 1 in bool_l


class Enemy(Tank):
    def __init__(self, x, y, speed, kind, enemies, hp=100, image=None, missile=[]):
        Tank.__init__(self, x, y, speed)
        self.missile = missile
        self.angle = 0
        self.missile = []
        self.image = image
        self.hp = hp
        self.direction = 180
        self.kind = kind
        self.enemies = enemies

        if kind == "casual":
            self.image = c.CASUAL_ENEMY
            self.speed = 0.8
        if kind == "fast":
            self.image = c.FAST_ENEMY
            self.speed = 3
            self.hp = 50
        if kind == "hurt":
            self.image = c.POPA_BOL_ENEMY
            self.speed = 2
            self.hp = 200

    def make_move(self, player: Player, level_map):
        enemy_rect_3 = pygame.Rect(self.x, self.y + 1, 26, 26)
        enemy_rect = pygame.Rect(self.x + 1, enemy_rect_3.topright[1] - 1, 0, 0)
        enemy_rect_2 = pygame.Rect(self.x + 1, enemy_rect_3.bottomright[1] - 24, 0, 0)
        enemy_rect_4 = pygame.Rect(enemy_rect_3.topright[0] - 22, self.y + 1, 0, 0)
        if self.direction == 0:
            if self.tank_collision_with_wall(enemy_rect, level_map) \
                    and self.y > 0 \
                    and not self.with_other_enemy_collision((self.x, self.y - self.speed)) \
                    and co((self.x, self.y - self.speed), player):
                self.direction = 0
                self.dy -= self.speed
                self.dx = 0
            else:
                self.direction = random.choice([180, 90, 270])
        if self.direction == 180:
            if self.tank_collision_with_wall(enemy_rect_2, level_map) \
                    and self.y < s.DISPLAY_HEIGHT - 30 \
                    and co((self.x, self.y + self.speed), player) \
                    and not self.with_other_enemy_collision((self.x, self.y + self.speed)):
                self.direction = 180
                self.dy += self.speed
                self.dx = 0
            else:
                self.direction = random.choice([0, 90, 270])
        if self.direction == 90:
            if self.tank_collision_with_wall(enemy_rect_3, level_map) \
                    and self.x > 0 \
                    and not self.with_other_enemy_collision((self.x - self.speed, self.y)) \
                    and co((self.x - self.speed, self.y), player):
                self.direction = 90
                self.dx -= self.speed
                self.dy = 0
            else:
                self.direction = random.choice([0, 180, 270])
        if self.direction == 270:
            if self.tank_collision_with_wall(enemy_rect_4, level_map) \
                    and self.x < s.GAME_DISP_WIDTH \
                    and not self.with_other_enemy_collision((self.x + self.speed, self.y)) \
                    and co((self.x + self.speed, self.y), player):
                self.direction = 270
                self.dx += self.speed
                self.dy = 0
            else:
                self.direction = random.choice([0, 90, 180])

    def with_other_enemy_collision(self, new_position):
        rec_l = []
        player_rect = pygame.Rect(self.x, self.y, 26, 26)
        new_player_rect = pygame.Rect(new_position[0], new_position[1], 26, 26)
        bool_l = []
        for elem in self.enemies:
            rec_l.append(pygame.Rect(elem.x, elem.y, 26, 26))
        rec_l.remove(player_rect)
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
        missile_e = Missile(self.x + 4, self.y + 4, direction, traction_x, traction_y, c.OBJ_SIZE / 2)
        if len(self.missile) < 1:
            self.missile.append(missile_e)

    def bullet_operation(self):
        for bullet in self.missile:
            if 0 < bullet.x < s.GAME_DISP_WIDTH and 0 < bullet.y < 416:
                bullet.x += bullet.speed_x
                bullet.y += bullet.speed_y
            else:
                self.missile.pop(self.missile.index(bullet))

    def update_position(self, game_display):
        self.x += self.dx
        self.y += self.dy
        self.draw(game_display, pygame.transform.rotate(self.image, self.direction), (self.x, self.y))
        self.dx = 0
        self.dy = 0
