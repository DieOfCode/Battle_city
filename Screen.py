import pygame.locals
from settings import *
from constant import *
from Tank import *
from GameObject import *
import BattleCity
from Score import *


class Screen:

    def __init__(self):
        self.running = False

    def message_to_screen(self, msg, color, width, height, font_type, y_displace=0, x_displace=0):
        text_surface, text_rect = self.text_objects(msg, color, font_type)
        text_rect.center = (width / 2) + x_displace, (height / 2) + y_displace
        GAME_DISPLAY.blit(text_surface, text_rect)

    def create_menu_button(self, width, height):
        return pygame.Rect((width / 2), (height / 2), 120, 50)

    def text_objects(self, text, color, font_type):
        text_surface = font_type.render(text, True, color)
        return text_surface, text_surface.get_rect()

    def button_click(self, button):
        click = pygame.mouse.get_pressed()
        cur = pygame.mouse.get_pos()
        if button.x + button.width > cur[0] > button.x:
            if button.y + button.height > cur[1] > button.y:
                if click[0] == 1:
                    return True
        return False

    def start_screen(self):
        beginning = True
        while beginning:
            # START_SCREEN.play()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        beginning = False
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            GAME_DISPLAY.fill(BLACK)
            self.message_to_screen("High score:" + str(load_score()), WHITE, DISPLAY_WIDTH, DISPLAY_HEIGHT,
                                   SMALL_FONT, -150)
            self.message_to_screen("BATTLE CITY", RED, DISPLAY_WIDTH, DISPLAY_HEIGHT, FONT, -100)
            self.message_to_screen("It`s awful and i know it", WHITE,
                                   DISPLAY_WIDTH, DISPLAY_HEIGHT, SMALL_FONT, -40)
            self.message_to_screen("Start", WHITE, DISPLAY_WIDTH, DISPLAY_HEIGHT, BUTTON_FONT, 20)
            start_button = self.create_menu_button(DISPLAY_WIDTH - 110, DISPLAY_HEIGHT - 40)
            if self.button_click(start_button):
                BUTTON_MUSIC.play()
                game = BattleCity.MainFunc(level=1, level_map=LoadLevel.load_level(1), enemy_in_game=[])
                game.main_loop()
            pygame.display.update()
            TIMER.tick(FPS)

    def next_level_screen(self, player: Player, num_of_level, game_score):
        GAME_DISPLAY.fill(BLACK)
        next_level_button = self.create_menu_button(DISPLAY_WIDTH - 110, DISPLAY_HEIGHT - 40)
        exit_button = self.create_menu_button(DISPLAY_WIDTH - 110, DISPLAY_HEIGHT - 60)
        self.message_to_screen("Curret score:" + str(get_score(player)), WHITE, DISPLAY_WIDTH, DISPLAY_HEIGHT,
                               SMALL_FONT, -150)
        self.message_to_screen("LEVEL ", RED, DISPLAY_WIDTH, DISPLAY_HEIGHT, FONT, -100)
        self.message_to_screen("Next Level", WHITE, DISPLAY_WIDTH, DISPLAY_HEIGHT, BUTTON_FONT, 20)
        self.message_to_screen("COMPLETE ", RED, DISPLAY_WIDTH, DISPLAY_HEIGHT, FONT, -55)
        if self.button_click(next_level_button):
            new_level = BattleCity.MainFunc(level=num_of_level + 1, enemy_in_game=[], game_score=game_score+get_score(player),
                                            level_map=LoadLevel.load_level(num_of_level + 1))
            new_level.main_loop()
        if self.button_click(exit_button):
            return True

    def game_over_screen(self):

        GAME_DISPLAY.fill([0, 0, 0])

        self.message_to_screen("game", RED, DISPLAY_WIDTH, DISPLAY_HEIGHT, FONT, -100)
        self.message_to_screen("over", RED, DISPLAY_WIDTH, DISPLAY_HEIGHT, FONT, -50)

        self.message_to_screen("Press Enter To Continue", WHITE, DISPLAY_WIDTH, DISPLAY_HEIGHT, BUTTON_FONT, 20)
        pygame.display.flip()

        while 1:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.start_screen()

    @staticmethod
    def draw_sidebar(player: Player, enemy_in_level):

        x = 416
        y = 0
        GAME_DISPLAY.fill([100, 100, 100], pygame.Rect([416, 0], [100, 416]))

        x_pos = x + 16
        y_pos = y + 16

        for n in range(enemy_in_level):
            GAME_DISPLAY.blit(ENEMY_LIFE, [x_pos, y_pos])
            if n % 2 == 1:
                x_pos = x + 16
                y_pos += 17
            else:
                x_pos += 17

        GAME_DISPLAY.blit(SMALL_FONT.render(str(player.life), False, BLACK), [x + 35, y + 215])
        GAME_DISPLAY.blit(PLAYER_LIFE, [x + 17, y + 215])

        GAME_DISPLAY.blit(FLAG, [x + 17, y + 280])
        GAME_DISPLAY.blit(BUTTON_FONT.render(str(LEVEL), False, BLACK), [x + 64, y + 285])
