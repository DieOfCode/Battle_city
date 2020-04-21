import settings as s
import constant as c
import pygame.locals


class GameObject:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.object_rect = pygame.Rect(x, y, c.OBJ_SIZE, c.OBJ_SIZE)


class Missile(GameObject):
    def __init__(self, x, y, angle, direction_x, direction_y, size, damage=50):
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
    def missile_collision(tank):
        if tank.missile:
            for block in s.MAP:
                if tank.missile is not None and not collision(tank.missile[0], block) and block.block_type is not "BUSH":
                    s.GAME_DISPLAY.blit(c.EXPLODE, (tank.missile[0].x, tank.missile[0].y))
                    if block.block_type == 'BRICK':
                        s.MAP.remove(block)
                    tank.missile.pop(0)
                    break


class Base(GameObject):
    def __init__(self, x, y, size, state, hp=100):
        GameObject.__init__(self, x, y, size)
        self.state = state
        self.kind = 'castle'
        self.hp = hp

    def draw(self, game_display):

        if self.state == 'alive':
            game_display.blit(c.CASTLE_IMG, (self.x, self.y))
        if self.state == 'destroyed':
            game_display.blit(c.DESTR_CASTLE, (self.x, self.y))


class Blocks(GameObject):
    def __init__(self, x, y, block_type, size):
        GameObject.__init__(self, x, y, size)
        self.block_type = block_type

    def draw(self, game_display, ):

        if self.block_type == 'IRON':
            game_display.blit(c.IRON_BRICK, (self.x, self.y))
        elif self.block_type == 'BUSH':
            game_display.blit(c.BUSH, (self.x, self.y))
        elif self.block_type == 'BRICK':
            game_display.blit(c.BRICK, (self.x, self.y))
        elif self.block_type == 'IRON_FLOOR':
            game_display.blit(c.IRON_FLOOR, (self.x, self.y))
        elif self.block_type == 'WATER':
            game_display.blit(c.WATER, (self.x, self.y))
        elif self.block_type == "B":
            game_display.blit(c.CASTLE_IMG, (self.x, self.y))


def collision(some_object, rec_object):
    if rec_object.x <= some_object.x <= rec_object.x + c.OBJ_SIZE \
            or rec_object.x <= some_object.x + c.OBJ_SIZE <= rec_object.x + c.OBJ_SIZE:
        if rec_object.y <= some_object.y <= rec_object.y + c.OBJ_SIZE or rec_object.y <= some_object.y + c.OBJ_SIZE <= \
                rec_object.y + c.OBJ_SIZE:
            return False

    return True
