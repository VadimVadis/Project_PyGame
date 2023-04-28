import pygame
import pygame_gui
from registration import Authorization, signal_notification
from rules import Rule
from choose_LVL import LVLs
from shop import Shop


class Main_menu:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Prince Of Voronezh')
        self.window_surface = pygame.display.set_mode((800, 600))
        self.background = pygame.image.load('images/background.jpg')
        self.manager = pygame_gui.UIManager((800, 600))
        self.id_player = -1
        self.name_use_person = -1
        self.lvl = -1
        self.name_player = ''
        self.text_information = f'Неизвестный пользователь'
        self.font = pygame.font.SysFont(None, 29)
        self.text = self.font.render(str(self.text_information), True, (230, 9, 89))

        self.game_bt = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((30, 200), (250, 50)),
            text='Играть',
            manager=self.manager)

        self.reg_bt = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((30, 300), (250, 50)),
            text='Авторизация',
            manager=self.manager)

        self.shop_bt = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((30, 360), (250, 50)),
            text='Магазин',
            manager=self.manager)
        self.rules_bt = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((30, 420), (250, 50)),
            text='Правила',
            manager=self.manager)
        self.triangle_left = pygame.image.load('images\_treyg_left.png')
        self.triangle_right = pygame.image.load('images\_treyg_right.png')
        self.triangle_left = pygame.transform.scale(self.triangle_left, (25, 25))
        self.triangle_right = pygame.transform.scale(self.triangle_right, (25, 25))
        self.num_btn = ''
        self.clock = pygame.time.Clock()
        self.menu()
        ## Данные игрока

    def what_btn(self):
        if self.num_btn == 'game_bt':
            self.window_surface.blit(self.triangle_left, (5, 210))
            self.window_surface.blit(self.triangle_right, (280, 208))
        elif self.num_btn == 'reg_bt':
            self.window_surface.blit(self.triangle_left, (5, 310))
            self.window_surface.blit(self.triangle_right, (280, 308))
        elif self.num_btn == 'shop_bt':
            self.window_surface.blit(self.triangle_left, (5, 370))
            self.window_surface.blit(self.triangle_right, (280, 368))
        elif self.num_btn == 'rules_bt':
            self.window_surface.blit(self.triangle_left, (5, 430))
            self.window_surface.blit(self.triangle_right, (280, 428))

    def menu(self):
        running = True
        while running:
            time_delta = self.clock.tick(60) / 1000.0
            self.window_surface.blit(self.background, (0, 0))
            self.window_surface.blit(self.text, (20, 30))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_ON_HOVERED:
                        # ОБРАБОТКА НАВЕДЕНИЯ НА КНОПКУ И ОТРИСОВКА ТРЕУГОЛЬНИКА
                        if event.ui_element == self.game_bt:
                            self.num_btn = 'game_bt'
                        elif event.ui_element == self.reg_bt:
                            self.num_btn = 'reg_bt'
                        elif event.ui_element == self.shop_bt:
                            self.num_btn = 'shop_bt'
                        elif event.ui_element == self.rules_bt:
                            self.num_btn = 'rules_bt'
                    else:
                        self.num_btn = ''
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.game_bt:
                            if self.id_player != -1:
                                f = LVLs(self.id_player, self.name_use_person, self.lvl)
                                self.lvl = f.lvl
                            else:
                                signal_notification('Для начала авторизуйтесь', self.manager)
                        elif event.ui_element == self.reg_bt:
                            f = Authorization()
                            self.id_player = f.id_player
                            self.name_use_person = f.name_use_person
                            self.lvl = f.lvl
                            self.name_player = f.name_player
                        elif event.ui_element == self.shop_bt:
                            if self.id_player != -1:
                                f = Shop(self.id_player)
                                self.name_use_person = f.name_use_person
                            else:
                                signal_notification('Для начала авторизуйтесь', self.manager)
                        elif event.ui_element == self.rules_bt:
                            Rule()

                self.manager.process_events(event)
            self.manager.update(time_delta)
            self.manager.draw_ui(self.window_surface)
            self.what_btn()
            if self.name_player != '':
                self.text_information = f'Пользователь: {self.name_player}    {self.lvl} lvl '
                self.text = self.font.render(str(self.text_information), True, (230, 9, 89))
            pygame.display.update()


if __name__ == '__main__':
    a = Main_menu()
    pygame.quit()
