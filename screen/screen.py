import pygame.locals
from settings import GAME_DISPLAY, DISPLAY_HEIGHT, DISPLAY_WIDTH, TIMER, FPS
from constant import constant
from game_object.tank import Player
from game import battle_city
from game.score import load_score, get_score


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
            GAME_DISPLAY.fill(constant.BLACK)
            self.message_to_screen("High score:" + str(load_score()), constant.WHITE, DISPLAY_WIDTH, DISPLAY_HEIGHT,
                                   constant.SMALL_FONT, -150)
            self.message_to_screen("BATTLE CITY", constant.RED, DISPLAY_WIDTH, DISPLAY_HEIGHT, constant.FONT, -100)
            self.message_to_screen("It`s awful and i know it", constant.WHITE,
                                   DISPLAY_WIDTH, DISPLAY_HEIGHT, constant.SMALL_FONT, -40)
            self.message_to_screen("Start", constant.WHITE, DISPLAY_WIDTH, DISPLAY_HEIGHT, constant.BUTTON_FONT, 20)
            start_button = self.create_menu_button(DISPLAY_WIDTH - 110, DISPLAY_HEIGHT - 40)
            if self.button_click(start_button):
                constant.BUTTON_MUSIC.play()
                game = battle_city.Game(level=1, enemy_in_game=[],
                                        game_score=0)
                game.main_loop()
            pygame.display.update()
            TIMER.tick(FPS)

    def next_level_screen(self, player: Player, num_of_level, game_score):
        GAME_DISPLAY.fill(constant.BLACK)
        self.message_to_screen("Current score: " + str(game_score + get_score(player)), constant.WHITE, DISPLAY_WIDTH,
                               DISPLAY_HEIGHT, constant.SMALL_FONT, -150)
        next_level_button = self.create_menu_button(DISPLAY_WIDTH - 110, DISPLAY_HEIGHT - 40)
        exit_button = self.create_menu_button(DISPLAY_WIDTH - 110, DISPLAY_HEIGHT - 60)
        self.message_to_screen("LEVEL ", constant.RED, DISPLAY_WIDTH, DISPLAY_HEIGHT, constant.FONT, -100)
        self.message_to_screen("Next Level", constant.WHITE, DISPLAY_WIDTH, DISPLAY_HEIGHT, constant.BUTTON_FONT, 20)
        self.message_to_screen("COMPLETE ", constant.RED, DISPLAY_WIDTH, DISPLAY_HEIGHT, constant.FONT, -55)
        if self.button_click(next_level_button):
            new_level = battle_city.Game(level=num_of_level + 1, enemy_in_game=[],
                                         game_score=game_score + get_score(player))
            new_level.main_loop()
        if self.button_click(exit_button):
            return True

    def victory_screen(self):
        GAME_DISPLAY.fill(constant.BLACK)
        self.message_to_screen("VICTORY ", constant.RED, DISPLAY_WIDTH, DISPLAY_HEIGHT, constant.FONT, -100)
        self.message_to_screen("Press Esc To Exit", constant.WHITE, DISPLAY_WIDTH, DISPLAY_HEIGHT, constant.BUTTON_FONT,
                               20)
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.start_screen()

    def game_over_screen(self):
        GAME_DISPLAY.fill(constant.BLACK)
        self.message_to_screen("game", constant.RED, DISPLAY_WIDTH, DISPLAY_HEIGHT, constant.FONT, -100)
        self.message_to_screen("Over", constant.RED, DISPLAY_WIDTH, DISPLAY_HEIGHT, constant.FONT, -50)
        self.message_to_screen("Press Enter To Continue", constant.WHITE, DISPLAY_WIDTH, DISPLAY_HEIGHT,
                               constant.BUTTON_FONT, 20)
        pygame.display.flip()
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.start_screen()

    @staticmethod
    def draw_sidebar(player: Player, enemy_in_level, current_level):

        x = 416
        y = 0
        GAME_DISPLAY.fill([100, 100, 100], pygame.Rect([416, 0], [100, 416]))

        x_pos = x + 16
        y_pos = y + 16

        for n in range(enemy_in_level):
            GAME_DISPLAY.blit(constant.ENEMY_LIFE, [x_pos, y_pos])
            if n % 2 == 1:
                x_pos = x + 16
                y_pos += 17
            else:
                x_pos += 17
        GAME_DISPLAY.blit(constant.SMALL_FONT.render(str(int(player.hp / 50)), False, constant.BLACK),
                          [x + 35, y + 215])
        GAME_DISPLAY.blit(constant.PLAYER_LIFE, [x + 17, y + 215])

        GAME_DISPLAY.blit(constant.FLAG, [x + 17, y + 280])
        GAME_DISPLAY.blit(constant.BUTTON_FONT.render(str(current_level), False, constant.BLACK), [x + 64, y + 285])
