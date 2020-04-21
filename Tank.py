import settings as s
import constant as c
from GameObject import Missile
import pygame
import LoadLevel


class Tank:
    def __init__(self, x, y, speed, size, dx=0, dy=-1.0):
        self.x = x
        self.y = y
        self.speed = speed
        self.dx = dx
        self.dy = dy
        self.size = size
        self.angle = 0

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


class Player(Tank):
    def __init__(self, x, y, speed, size):
        Tank.__init__(self, x, y, speed, size)
        self.angle = 0
        self.missile = []

    def player_control(self, keys):
        my_rect = pygame.Rect(self.x, self.y + 1, 26, 26)
        my_rect_2 = pygame.Rect(my_rect.topright[0] - 22, self.y + 1, 0, 0)
        my_rect_3 = pygame.Rect(self.x + 1, my_rect.topright[1] - 1, 0, 0)
        my_rect_4 = pygame.Rect(self.x + 1, my_rect.bottomright[1] - 24, 0, 0)

        if keys[pygame.K_LEFT] and self.x > 0:
            self.angle = 90
            if self.tank_collision_with_wall(my_rect, s.MAP):
                self.x -= self.speed
                self.dx = -1
                self.dy = 0
        elif keys[pygame.K_RIGHT] and self.x < s.DISPLAY_WIDTH - 30:
            self.angle = 270
            if self.tank_collision_with_wall(my_rect_2, s.MAP):
                self.x += self.speed
                self.dx = 1
                self.dy = 0
        elif keys[pygame.K_UP] and self.y > 0:
            self.angle = 0
            if self.tank_collision_with_wall(my_rect_3, s.MAP):
                self.y -= self.speed
                self.dx = 0
                self.dy = -1
        elif keys[pygame.K_DOWN] and self.y < s.DISPLAY_HEIGHT - 30:
            self.angle = 180
            if self.tank_collision_with_wall(my_rect_4, s.MAP):
                self.y += self.speed
                self.dx = 0
                self.dy = 1

        if keys[pygame.K_SPACE] and len(self.missile) < 1:
            self.missile.append(Missile(self.x + 4, self.y + 4, self.angle, self.dx, self.dy, c.OBJ_SIZE / 2))
            c.FIRE_SOUND.set_volume(10)
            c.FIRE_SOUND.play()

    def bullet_operation(self):
        for bullet in self.missile:
            if 0 < bullet.x < s.DISPLAY_WIDTH and 0 < bullet.y < s.DISPLAY_HEIGHT:
                bullet.x += bullet.speed_x
                bullet.y += bullet.speed_y
            else:
                self.missile.pop(self.missile.index(bullet))

    def collision_with_enemy(self):
        pass


class Enemy(Tank):
    def __init__(self, x, y, speed, size, kind, hp=100, image=None, missile=[]):
        Tank.__init__(self, x, y, speed, size)
        self.missile = missile
        self.angle = 0
        self.missile = []
        self.image = image
        self.hp = hp
        self.direction = 0
        if kind == "casual":
            self.image = c.CASUAL_ENEMY
            self.speed = 5
        if kind == "fast":
            self.image = c.FAST_ENEMY
            self.speed = 10
            self.hp = 50
        if kind == "hurt":
            self.image = c.POPA_BOL_ENEMY
            self.speed = 1
            self.hp = 200

    def make_move(self, obj):
        enemy_rect_3 = pygame.Rect(self.x, self.y + 1, 26, 26)
        enemy_rect = pygame.Rect(self.x + 1, enemy_rect_3.topright[1] - 1, 0, 0)
        enemy_rect_2 = pygame.Rect(self.x + 1, enemy_rect_3.bottomright[1] - 24, 0, 0)
        enemy_rect_4 = pygame.Rect(enemy_rect_3.topright[0] - 22, self.y + 1, 0, 0)
        if self.y > obj.y:
            if self.tank_collision_with_wall(enemy_rect, s.MAP):
                self.direction = 0
                self.dy -= self.speed
                self.dx = 0
        if self.y < obj.y:
            if self.tank_collision_with_wall(enemy_rect_2, s.MAP):
                self.direction = 180
                self.dy += self.speed
                self.dx = 0
        if self.x > obj.x:
            if self.tank_collision_with_wall(enemy_rect_3, s.MAP):
                self.direction = 90
                self.dx -= self.speed
                self.dy = 0
        if self.x < obj.x:
            if self.tank_collision_with_wall(enemy_rect_4, s.MAP):
                self.direction = 270
                self.dx += self.speed
                self.dy = 0

    def shoot(self, enemy, direction):

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
            if 0 < bullet.x < 520 and 0 < bullet.y < 416:
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
