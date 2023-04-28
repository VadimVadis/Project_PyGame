import pygame
import pygame_gui
import sqlite3
import hashlib


def signal_notification(value, manager):
    conf_dealog = pygame_gui.windows.ui_message_window.UIMessageWindow(
        rect=pygame.Rect((250, 200), (300, 200)),
        html_message=value,
        manager=manager,
        window_title="Оповещение")


class Authorization:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Prince Of Voronezh')
        self.window_surface = pygame.display.set_mode((800, 600))
        self.background = pygame.image.load('images/reg1.jpg')
        self.manager = pygame_gui.UIManager((800, 600))
        self.name_use_person = -1
        self.lvl = -1
        self.id_player = -1
        self.name_player = ''
        self.entrance = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((30, 280), (340, 40)),
            text='Войти',
            manager=self.manager)
        self.return_back = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((20, 450), (150, 50)),
            text='Вернуться назад',
            manager=self.manager)
        self.registration = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((440, 250), (110, 40)),
            text='Регистрация',
            manager=self.manager)
        self.return_password = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((440, 200), (180, 40)),
            text='Восстановить пароль',
            manager=self.manager)
        self.name = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((118, 171), (250, 30)),
            manager=self.manager)
        self.psw = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((118, 221), (250, 30)),
            manager=self.manager)
        self.clock = pygame.time.Clock()
        self.authorization_func()

    def login(self):
        name = self.name.get_text()
        passw = self.psw.get_text()

        con = sqlite3.connect('users.db')
        cur = con.cursor()
        # Проверяем есть ли такой пользователь
        value = cur.execute(f"""SELECT id, name, hesh_psw, use_person, lvl FROM users WHERE name='{name}'""").fetchall()
        # Переводим пароль в хэш
        password_bytes = passw.encode('utf-8')
        hesh_psw = hashlib.sha1(password_bytes).hexdigest()
        if value != [] and value[0][2] == hesh_psw:
            signal_notification('Здравствуйте, ' + name + '!', self.manager)
            self.id_player = value[0][0]
            self.name_use_person = value[0][3]
            self.name_player = value[0][1]
            self.lvl = value[0][4]
        else:
            signal_notification('Неверные данные', self.manager)
        con.close()

    def authorization_func(self):
        running = True
        while running:
            time_delta = self.clock.tick(60) / 1000.0
            self.window_surface.blit(self.background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.entrance:
                            self.login()
                        elif event.ui_element == self.registration:
                            Register()
                        elif event.ui_element == self.return_password:
                            Return_PSW()
                        elif event.ui_element == self.return_back:
                            running = False
                self.manager.process_events(event)
            self.manager.update(time_delta)
            self.manager.draw_ui(self.window_surface)
            pygame.display.update()


class Register:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Prince Of Voronezh')
        self.window_surface = pygame.display.set_mode((800, 600))
        self.background = pygame.image.load('images/reg3.jpg')
        self.manager = pygame_gui.UIManager((800, 600))

        self.reg_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((235, 350), (300, 40)),
            text='Завершить регистрацию',
            manager=self.manager)
        self.return_menu_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((20, 450), (150, 50)),
            text='Вернуться назад',
            manager=self.manager)
        self.name = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((235, 123), (300, 30)),
            manager=self.manager)
        self.key_word = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((235, 181), (300, 30)),
            manager=self.manager)
        self.psw1 = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((235, 236), (300, 30)),
            manager=self.manager)
        self.psw2 = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((235, 292), (300, 30)),
            manager=self.manager)
        self.clock = pygame.time.Clock()
        self.authorization_func()

    def reg(self):
        self.register(str(self.name.get_text()), str(self.psw1.get_text()),
                      str(self.psw2.get_text()), str(self.key_word.get_text()))

    def register(self, name, passw1, passw2, key_word):
        con = sqlite3.connect('users.db')
        cur = con.cursor()
        # Проверяем используется ли такой логин
        value = cur.execute(f'SELECT * FROM users WHERE name="{name}";').fetchall()
        if len(passw1) == 0 and len(name) == 0:
            signal_notification('Некорректный ввод', self.manager)
        elif len(key_word) == 0:
            signal_notification('Некорректное кодовое слово', self.manager)
        elif len(passw1) == 0:
            signal_notification('Некорректный пароль', self.manager)
        elif passw1 != passw2:
            signal_notification('Пароли не совпадают', self.manager)
        elif len(name) == 0:
            signal_notification('Некорректное имя пользователя', self.manager)
        elif not value:
            password_bytes = passw1.encode('utf-8')
            hesh_psw = hashlib.sha1(password_bytes).hexdigest()
            cur.execute(f"INSERT INTO users (name, hesh_psw, key_word, lvl, "
                        f"buy_person, use_person, kolvo_money) VALUES ('{name}', '{hesh_psw}', '{key_word}', 1, '1;', 1, 0)")
            con.commit()
            signal_notification('Всё прошло успешно!', self.manager)
        else:
            signal_notification('Такой ник уже используется!', self.manager)

    def authorization_func(self):
        running = True
        while running:
            time_delta = self.clock.tick(60) / 1000.0
            self.window_surface.blit(self.background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.USEREVENT:
                    self.window_surface.blit(self.background, (0, 0))
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.reg_btn:
                            self.reg()
                        elif event.ui_element == self.return_menu_btn:
                            running = False
                self.manager.process_events(event)
            self.manager.update(time_delta)
            self.manager.draw_ui(self.window_surface)
            pygame.display.update()


class Return_PSW:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Prince Of Voronezh')
        self.window_surface = pygame.display.set_mode((800, 600))
        self.background = pygame.image.load('images/reg2.jpg')
        self.manager = pygame_gui.UIManager((800, 600))

        self.update_psw = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((235, 350), (300, 40)),
            text='Завершить регистрацию',
            manager=self.manager)
        self.return_menu_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((20, 450), (150, 50)),
            text='Вернуться назад',
            manager=self.manager)
        self.name = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((235, 123), (300, 30)),
            manager=self.manager)
        self.key_word = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((235, 181), (300, 30)),
            manager=self.manager)
        self.psw1 = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((235, 236), (300, 30)),
            manager=self.manager)
        self.psw2 = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((235, 292), (300, 30)),
            manager=self.manager)
        self.clock = pygame.time.Clock()
        self.update_psw_func()

    def check_data_func(self):
        self.change_data(str(self.name.get_text()), str(self.psw1.get_text()),
                         str(self.psw2.get_text()), str(self.key_word))

    def change_data(self, name, passw1, passw2, key_word):
        con = sqlite3.connect('users.db')
        cur = con.cursor()
        # Проверяем используется ли такой логин
        value = cur.execute(f'SELECT * FROM users WHERE name="{name}";').fetchall()
        if value != [] and key_word != value[0][3]:
            if passw1 == passw2:
                password_bytes = passw1.encode('utf-8')
                hesh_psw = hashlib.sha1(password_bytes).hexdigest()
                cur.execute(f"UPDATE users SET hesh_psw = '{hesh_psw}'"
                            f"WHERE name = '{name}'")
                signal_notification('Вы успешно поменяли пароль', self.manager)
                con.commit()
            else:
                signal_notification('Пароли не совпадают', self.manager)
        else:
            signal_notification('Не верные данные!', self.manager)

    def update_psw_func(self):
        running = True
        while running:
            time_delta = self.clock.tick(60) / 1000.0
            self.window_surface.blit(self.background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.USEREVENT:
                    self.window_surface.blit(self.background, (0, 0))
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.update_psw:
                            self.check_data_func()
                        elif event.ui_element == self.return_menu_btn:
                            running = False
                self.manager.process_events(event)
            self.manager.update(time_delta)
            self.manager.draw_ui(self.window_surface)
            pygame.display.update()
