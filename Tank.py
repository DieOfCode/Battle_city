import settings as s
import constant as c
import random
import GameObject as go
from GameObject import Missile
from GameObject import collision as co
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
        self.rect = pygame.Rect(self.x, self.y, 26, 26)

    def draw(self, game_display, img, position):
        t = pygame.transform.rotate(img, self.angle)
        game_display.blit(t, position)

    def tank_collision_with_wall(self, some_object, rec_object):
        for elem in rec_object:
            if elem.block_type != "BUSH":
                if elem.object_rect.x <= some_object.x <= elem.object_rect.x + c.OBJ_SIZE \
                        or elem.object_rect.x <= some_object.x + 25 <= elem.object_rect.x + c.OBJ_SIZE:
                    if elem.object_rect.y <= some_object.y <= elem.object_rect.y + c.OBJ_SIZE or elem.object_rect.y <= some_object.y \
                            + 25 <= elem.object_rect.y + c.OBJ_SIZE:
                        return False

        return True

    def inside_boundaries(self):
        """Checks if the object inside game boundaries"""
        return self.x + self.dx > 0 \
               and self.x < s.GAME_DISP_WIDTH \
               and 0 < self.y < s.DISPLAY_HEIGHT - 20


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

    def player_control(self, keys,level_map):
        my_rect = pygame.Rect(self.x, self.y + 1, 26, 26)
        my_rect_2 = pygame.Rect(my_rect.topright[0] - 22, self.y + 1, 0, 0)
        my_rect_3 = pygame.Rect(self.x + 1, my_rect.topright[1] - 1, 0, 0)
        my_rect_4 = pygame.Rect(self.x + 1, my_rect.bottomright[1] - 24, 0, 0)

        if keys[pygame.K_LEFT] and self.x > 0:
            self.angle = 90
            self.dx = -1
            self.dy = 0
            if self.tank_collision_with_wall(my_rect, level_map):
                self.x -= self.speed

        elif keys[pygame.K_RIGHT] and self.x < s.GAME_DISP_WIDTH:
            self.angle = 270
            self.dx = 1
            self.dy = 0
            if self.tank_collision_with_wall(my_rect_2, level_map):
                self.x += self.speed

        elif keys[pygame.K_UP] and self.y > 0:
            self.angle = 0
            self.dx = 0
            self.dy = -1
            if self.tank_collision_with_wall(my_rect_3,level_map):
                self.y -= self.speed

        elif keys[pygame.K_DOWN] and self.y < s.DISPLAY_HEIGHT - 30:
            self.angle = 180
            self.dx = 0
            self.dy = 1
            if self.tank_collision_with_wall(my_rect_4, level_map):
                self.y += self.speed

        if keys[pygame.K_SPACE] and len(self.missile) < 1:
            self.missile.append(Missile(self.x + 4, self.y + 4, self.angle, self.dx, self.dy, c.OBJ_SIZE / 2))
            c.FIRE_SOUND.set_volume(10)
            c.FIRE_SOUND.play()

    def collision_missile_with_enemy(self):
        for elem in self.enemies:
            for mis in self.missile:
                if elem.x < mis.x < elem.x + c.OBJ_SIZE \
                        and elem.y < mis.y < elem.y + c.OBJ_SIZE:
                    self.missile.remove(mis)
                    self.kill_enemy[elem.kind] += 1
                    self.enemies.remove(elem)
                    self.count_of_enemies -= 1

    def my_collision(self, rec_object):
        pass


class Enemy(Tank):
    def __init__(self, x, y, speed, kind, hp=100, image=None, missile=[]):
        Tank.__init__(self, x, y, speed)
        self.missile = missile
        self.angle = 0
        self.missile = []
        self.image = image
        self.hp = hp
        self.direction = 180
        self.kind = kind

        if kind == "casual":
            self.image = c.CASUAL_ENEMY
            self.speed = 0.1
        if kind == "fast":
            self.image = c.FAST_ENEMY
            self.speed = 3
            self.hp = 50
        if kind == "hurt":
            self.image = c.POPA_BOL_ENEMY
            self.speed = 2
            self.hp = 200

    def make_move(self, obj,level_map):
        enemy_rect_3 = pygame.Rect(self.x, self.y + 1, 26, 26)
        enemy_rect = pygame.Rect(self.x + 1, enemy_rect_3.topright[1] - 1, 0, 0)
        enemy_rect_2 = pygame.Rect(self.x + 1, enemy_rect_3.bottomright[1] - 24, 0, 0)
        enemy_rect_4 = pygame.Rect(enemy_rect_3.topright[0] - 22, self.y + 1, 0, 0)
        if self.direction == 0 and co(enemy_rect, pygame.Rect(obj.x, obj.y, 26, 26)):
            if self.tank_collision_with_wall(enemy_rect, level_map) and self.y > 0:
                self.direction = 0
                self.dy -= self.speed
                self.dx = 0
            else:
                self.direction = random.choice([180, 90, 270])
        if self.direction == 180 and co(enemy_rect_2, pygame.Rect(obj.x, obj.y, 26, 26)):
            if self.tank_collision_with_wall(enemy_rect_2, level_map) and self.y < s.DISPLAY_HEIGHT - 30:
                self.direction = 180
                self.dy += self.speed
                self.dx = 0
            else:
                self.direction = random.choice([0, 90, 270])
        if self.direction == 90 and co(enemy_rect_3, pygame.Rect(obj.x, obj.y, 26, 26)):
            if self.tank_collision_with_wall(enemy_rect_3, level_map) and self.x > 0:
                self.direction = 90
                self.dx -= self.speed
                self.dy = 0
            else:
                self.direction = random.choice([0, 180, 270])
        if self.direction == 270 and co(enemy_rect_4, pygame.Rect(obj.x, obj.y, 26, 26)):
            if self.tank_collision_with_wall(enemy_rect_4, level_map) and self.x < s.GAME_DISP_WIDTH:
                self.direction = 270
                self.dx += self.speed
                self.dy = 0
            else:
                self.direction = random.choice([0, 90, 180])

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
