import pygame
from constant_and_setting.constant import PLAYER_SPRITE

pygame.init()

LEVEL = 1
ENEMY_TYPES = ['regular', 'heavy', 'fast']

DISPLAY_WIDTH = 500
GAME_DISP_WIDTH = 388
DISPLAY_HEIGHT = 416
FPS = 60

TIMER = pygame.time.Clock()

GAME_DISPLAY = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT),
                                       pygame.RESIZABLE | pygame.DOUBLEBUF)
pygame.display.set_caption('Battle city')
pygame.display.set_icon(PLAYER_SPRITE)

# BULLETS = []

LEVELS_ENEM = {
    1: ["casual"],
    1.5: ["casual"],
    2: ["hurt"],
    3: ["hurt"]
}
ENEMY_IN_LEVEL = len(LEVELS_ENEM[1])

#
#     (
#     (18, 2, 0, 0), (14, 4, 0, 2), (14, 4, 0, 2), (2, 5, 10, 3), (8, 5, 5, 2),
#     (9, 2, 7, 2), (7, 4, 6, 3), (7, 4, 7, 2), (6, 4, 7, 3), (12, 2, 4, 2),
#     (5, 5, 4, 6), (0, 6, 8, 6), (0, 8, 8, 4), (0, 4, 10, 6), (0, 2, 10, 8),
#     (16, 2, 0, 2), (8, 2, 8, 2), (2, 8, 6, 4), (4, 4, 4, 8), (2, 8, 2, 8),
#     (6, 2, 8, 4), (6, 8, 2, 4), (0, 10, 4, 6), (10, 4, 4, 2), (0, 8, 2, 10),
#     (4, 6, 4, 6), (2, 8, 2, 8), (15, 2, 2, 1), (0, 4, 10, 6), (4, 8, 4, 4),
#     (3, 8, 3, 6), (6, 4, 2, 8), (4, 4, 4, 8), (0, 10, 4, 6), (0, 6, 4, 10)
# )
