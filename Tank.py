from settings import *
from constant import *
from GameObject import Missile
import pygame.locals
import LoadLevel


class Tank:
    def __init__(self, x, y, speed, size, dx=0, dy=-1.0):
        self.x = x
        self.y = y
        self.speed = speed
        self.dx = dx
        self.dy = dy
        self.map_game = LoadLevel.load_level()
        self.size = size
        self.angle = 0

    def draw(self, game_display, img, position):
        t = pygame.transform.rotate(img, self.angle)
        game_display.blit(t, position)

    def tank_collision(self, some_object, rec_object):
        for elem in rec_object:
            if elem.block_type != "BUSH":
                if elem.object_rect.x <= some_object.x <= elem.object_rect.x + OBJ_SIZE \
                        or elem.object_rect.x <= some_object.x + OBJ_SIZE <= elem.object_rect.x + OBJ_SIZE:
                    if elem.object_rect.y <= some_object.y <= elem.object_rect.y + OBJ_SIZE or elem.object_rect.y <= some_object.y \
                            + OBJ_SIZE <= elem.object_rect.y + OBJ_SIZE:
                        return False

        return True


class Player(Tank):
    def __init__(self, x, y, speed, size):
        Tank.__init__(self, x, y, speed, size)
        self.angle = 0
        self.missile = []

    def player_control(self, keys):
        my_rect = pygame.Rect(self.x - 3, self.y + 11, 1, 26)
        my_rect_2 = pygame.Rect(self.x + 13, self.y + 11, 1, 26)
        my_rect_3 = pygame.Rect(self.x, self.y - 3, 26, 1)
        my_rect_4 = pygame.Rect(self.x, self.y + 13, 26, 1)
        if keys[pygame.K_LEFT] and self.x > 0 and self.tank_collision(my_rect, self.map_game):
            self.x -= self.speed
            self.angle = 90
            self.dx = -1
            self.dy = 0
        elif keys[pygame.K_RIGHT] and self.x < DISPLAY_WIDTH - 30 and self.tank_collision(my_rect_2, self.map_game):
            self.x += self.speed
            self.angle = 270
            self.dx = 1
            self.dy = 0
        elif keys[pygame.K_UP] and self.y > 0 and self.tank_collision(my_rect_3, self.map_game):
            self.y -= self.speed
            self.angle = 0
            self.dx = 0
            self.dy = -1
        elif keys[pygame.K_DOWN] and self.y < DISPLAY_HEIGHT - 30 and self.tank_collision(my_rect_4, self.map_game):
            self.y += self.speed
            self.angle = 180
            self.dx = 0
            self.dy = 1

        if keys[pygame.K_SPACE] and len(self.missile) <= 1:
            self.missile.append(Missile(self.x + 4, self.y + 4, self.angle, self.dx, self.dy, OBJ_SIZE))
            FIRE_SOUND.set_volume(10)
            FIRE_SOUND.play()

    def bullet_operation(self):
        for bullet in self.missile:
            if 0 < bullet.x < DISPLAY_WIDTH and 0 < bullet.y < DISPLAY_HEIGHT:
                bullet.x += bullet.speed_x
                bullet.y += bullet.speed_y
            else:
                self.missile.pop(self.missile.index(bullet))


class Enemy(Tank):
    def __init__(self, x, y, speed, size, kind, hp=100, image=None, missile=[]):
        Tank.__init__(self, x, y, speed, size)
        self.missiles = missile
        self.missile = missile
        self.angle = 0
        self.missile = []
        self.image = image
        self.hp = hp
        self.direction = None
        if kind == "casual":
            self.image = CASUAL_ENEMY
            self.speed = 5
        if kind == "fast":
            self.image = FAST_ENEMY
            self.speed = 10
            self.hp = 50
        if kind == "hurt":
            self.image = POPA_BOL_ENEMY
            self.speed = 1
            self.hp = 200

    def make_move(self, obj):
        enemy_rect = pygame.Rect(self.x, self.y - 3, 26, 26)
        enemy_rect_2 = pygame.Rect(self.x + 13, self.y + 13, 26, 26)
        enemy_rect_3 = pygame.Rect(self.x, self.y + 13, 26, 26)
        enemy_rect_4 = pygame.Rect(self.x + 13, self.y + 11, 26, 26)
        if self.y > obj.y and self.tank_collision(enemy_rect, self.map_game):
            self.dy -= self.speed
            self.dx = 0
            self.direction = 0
        elif self.y < obj.y and self.tank_collision(enemy_rect_2, self.map_game):
            self.dy += self.speed
            self.dx = 0
            self.direction = 180
        if self.x > obj.x and self.tank_collision(enemy_rect_3, self.map_game):
            self.dx -= self.speed
            self.dy = 0
            self.direction = 90
        elif self.x < obj.x and self.tank_collision(enemy_rect_4, self.map_game):
            self.dx += self.speed
            self.dy = 0
            self.direction = 270

    def update_position(self, game_display):
        self.x += self.dx
        self.y += self.dy
        self.draw(game_display, pygame.transform.rotate(self.image, self.direction), (self.x, self.y))
        self.dx = 0
        self.dy = 0
