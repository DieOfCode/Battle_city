from constant import constant
import settings
import pygame.locals
from sys import maxsize


class GameObject:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size


class Missile(GameObject):
    def __init__(self, x, y, angle, direction_x, direction_y, size, damage=1):
        GameObject.__init__(self, x, y, size)
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.y = y
        self.speed_x = 3 * direction_x
        self.speed_y = 3 * direction_y
        self.angle = angle
        self.damage = damage

    def draw(self, game_display, img):
        missile = pygame.transform.rotate(img, self.angle)
        game_display.blit(missile, (self.x, self.y))

    @staticmethod
    def missile_collision(tank, level_map):

        if tank.missile:
            for block in level_map:
                if tank.missile is not None \
                        and not collision(tank.missile[0], block) \
                        and block.block_type not in ["BUSH", "WATER", "BOMB"]:
                    settings.GAME_DISPLAY.blit(constant.EXPLODE, (tank.missile[0].x, tank.missile[0].y))
                    block.hp -= tank.damage
                    if block.hp <= 0:
                        level_map.remove(block)
                    if block.block_type == 'B':
                        level_map.remove(block)
                        return True
                    tank.missile.pop(0)
                    break

    @staticmethod
    def bullet_operation(missiles):
        for bullet in missiles:
            if 0 < bullet.x < 400 and 0 < bullet.y < settings.DISPLAY_HEIGHT:
                bullet.x += bullet.speed_x
                bullet.y += bullet.speed_y
            else:
                missiles.pop(missiles.index(bullet))

    @staticmethod
    def collision_with_player(missiles, my_obj):
        for mis in missiles:
            if my_obj.x < mis.x < my_obj.x + constant.OBJ_SIZE \
                    and my_obj.y < mis.y < my_obj.y + constant.OBJ_SIZE:
                missiles.remove(mis)
                return True
            return False


class Blocks(GameObject):
    def __init__(self, x, y, block_type, size, hp=100):
        GameObject.__init__(self, x, y, size)
        self.block_type = block_type
        self.hp = hp
        if self.block_type == "IRON":
            self.hp = 500
        if self.block_type == "BRICK":
            self.hp = 50
        if self.block_type == "IRON_FLOOR":
            self.hp = maxsize

    def draw(self, game_display):
        if self.block_type == 'IRON':
            game_display.blit(constant.IRON_BRICK, (self.x, self.y))
        elif self.block_type == 'BUSH':
            game_display.blit(constant.BUSH, (self.x, self.y))
        elif self.block_type == 'BRICK':
            game_display.blit(constant.BRICK, (self.x, self.y))
        elif self.block_type == 'IRON_FLOOR':
            game_display.blit(constant.IRON_FLOOR, (self.x, self.y))
        elif self.block_type == 'WATER':
            game_display.blit(constant.WATER, (self.x, self.y))
        elif self.block_type == "BOMB":
            game_display.blit(constant.BOMB, (self.x, self.y))
        elif self.block_type == "B":
            game_display.blit(constant.CASTLE_IMG, (self.x, self.y))


class Bomb(Blocks):
    def __init__(self, x, y):
        Blocks.__init__(self, x, y, block_type="BOMB", hp=100, size=26)
        self.tick_life = 0

    @staticmethod
    def collision_with_other_bomb(list_bomb: list, bomb):
        bomb_rect = pygame.Rect(bomb.x, bomb.y, 26, 26)
        bool_l = []
        for elem in list_bomb:
            enemy_rect = pygame.Rect(elem.x, elem.y, 26, 26)
            data = bomb_rect.colliderect(enemy_rect)
            bool_l.append(data)
        return 1 in bool_l

    def draw_explosion(self):
        settings.GAME_DISPLAY.blit(constant.BIG_EXPLODE, (self.x, self.y))


class Bonus(GameObject):
    def __init__(self, x, y, bonus_type):
        GameObject.__init__(self, x, y, size=26)
        self.bonus_type = bonus_type
        self.image = None
        self.life_tick = 300
        if self.bonus_type == "LIFE":
            self.image = constant.BONUS_LIFE
        if self.bonus_type == "DAMAGE":
            self.image = constant.BONUS_DAMAGE
        if self.bonus_type == "SPEED":
            self.image = constant.BONUS_SPEED

    def draw_bonus(self):
        settings.GAME_DISPLAY.blit(self.image, (self.x, self.y))


def collision(some_object, rec_object):
    return not pygame.Rect(some_object.x, some_object.y, some_object.size, some_object.size).colliderect(
        pygame.Rect(rec_object.x, rec_object.y, rec_object.size, rec_object.size))



