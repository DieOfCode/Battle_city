import pygame
from constant.constant import PLAYER_SPRITE

pygame.init()

LEVEL = 1

DISPLAY_WIDTH = 500
GAME_DISP_WIDTH = 388
DISPLAY_HEIGHT = 416
FPS = 60

TIMER = pygame.time.Clock()

GAME_DISPLAY = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT),
                                       pygame.RESIZABLE | pygame.DOUBLEBUF)
pygame.display.set_caption('Battle city')
pygame.display.set_icon(PLAYER_SPRITE)

LEVELS_ENEM = {
    1: ["casual", "casual", "casual", "casual", "casual", "casual", "casual", "casual", "casual", "casual", "casual"],
    1.5: ["casual"],
    2: ["casual", "casual", "casual", "casual", "casual", "casual", "fast", "fast", "fast", "hurt", "hurt"],
    3: ["fast", "fast", "fast", "fast", "fast", "fast", "hurt", "hurt", "hurt", "hurt", "hurt", "hurt", "hurt"],
    4: ["fast", "fast", "fast", "fast", "fast", "fast", "hurt", "hurt", "hurt", "hurt", "hurt", "hurt", "hurt",
        "casual", "casual", "casual"]
}
ENEMY_IN_LEVEL = len(LEVELS_ENEM[1])

LEVEL_BONUS = {
    1: ["LIFE", "SPEED", "DAMAGE"],
    1.5: [],
    2: ["LIFE", "LIFE", "DAMAGE", "SPEED"],
    3: ["LIFE", "LIFE", "DAMAGE", "SPEED"],
    4: ["LIFE", "LIFE", "DAMAGE", "SPEED"]
}
