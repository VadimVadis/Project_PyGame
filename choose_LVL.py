import pygame
import pygame_gui
from main_play import play
import sqlite3


class LVLs:
    def __init__(self, id_player, name_use_person, lvl1):
        pygame.init()
        pygame.display.set_caption('Prince Of Voronezh')
        self.window_surface = pygame.display.set_mode((800, 600))
        self.background = pygame.image.load('images/background2.jpg')
        self.manager = pygame_gui.UIManager((800, 600))
        self.id_player = id_player
        self.lvl = int(lvl1)
        if int(name_use_person) == 1:
            self.name_use_person = 'robot'
        elif int(name_use_person) == 2:
            self.name_use_person = 'girl'
        elif int(name_use_person) == 3:
            self.name_use_person = 'marr'
        self.return_back = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((20, 500), (150, 50)),
            text='Вернуться назад',
            manager=self.manager
        )
        self.lvl1 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((50, 80), (100, 100)),
            text='Уровень -1-',
            manager=self.manager
        )
        self.lvl2 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((180, 80), (100, 100)),
            text='Уровень -2-',
            manager=self.manager
        )
        self.lvl3 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((310, 80), (100, 100)),
            text='Уровень -3-',
            manager=self.manager
        )
        self.a = ''
        self.clock = pygame.time.Clock()
        self.choose_lvl()

    def choose_lvl(self):
        running = True
        while running:
            self.a = ''
            time_delta = self.clock.tick(60) / 1000.0
            self.window_surface.blit(self.background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.USEREVENT:
                    self.window_surface.blit(self.background, (0, 0))
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.lvl1 and self.lvl >= 1:
                            self.a = play(60, 'data\levels/lvl_1.txt', self.name_use_person, self.id_player)
                        elif event.ui_element == self.lvl2 and self.lvl >= 2:
                            self.a = play(120, 'data\levels/lvl_2.txt', self.name_use_person, self.id_player)
                        elif event.ui_element == self.lvl3 and self.lvl == 3:
                            self.a = play(1000, 'data\levels/lvl_3.txt', self.name_use_person, self.id_player)
                        elif event.ui_element == self.return_back:
                            running = False
                self.manager.process_events(event)
            if self.a == 'Победа':
                con = sqlite3.connect('users.db')
                cur = con.cursor()
                self.lvl = cur.execute(
                    f"""SELECT lvl FROM users WHERE id='{self.id_player}'""").fetchone()[0]
                con.commit()
                con.close()
            self.manager.update(time_delta)
            self.manager.draw_ui(self.window_surface)
            pygame.display.update()