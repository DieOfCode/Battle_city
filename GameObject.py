import settings as s
import constant as c
import pygame.locals
import LoadLevel
import Tank


class GameObject:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.object_rect = pygame.Rect(x, y, c.OBJ_SIZE, c.OBJ_SIZE)


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
                if tank.missile is not None and not collision(tank.missile[0],
                                                              block) and block.block_type is not "BUSH":
                    s.GAME_DISPLAY.blit(c.EXPLODE, (tank.missile[0].x, tank.missile[0].y))
                    if block.block_type == 'BRICK':
                        level_map.remove(block)
                    if block.block_type == 'B':
                        level_map.remove(block)
                        return True
                    tank.missile.pop(0)
                    break

    @staticmethod
    def bullet_operation(missiles):
        for bullet in missiles:
            if 0 < bullet.x < s.GAME_DISP_WIDTH and 0 < bullet.y < s.DISPLAY_HEIGHT:
                bullet.x += bullet.speed_x
                bullet.y += bullet.speed_y
            else:
                missiles.pop(missiles.index(bullet))

    @staticmethod
    def collision_with_player(missiles, my_obj):
        for mis in missiles:
            if my_obj.x < mis.x < my_obj.x + c.OBJ_SIZE \
                    and my_obj.y < mis.y < my_obj.y + c.OBJ_SIZE:
                missiles.remove(mis)
                return True
            return False


class Blocks(GameObject):
    def __init__(self, x, y, block_type, size, can_move):
        GameObject.__init__(self, x, y, size)
        self.block_type = block_type
        self.can_move = can_move

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
