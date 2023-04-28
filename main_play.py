from blocks import Platform, Princess, BlockTeleport, BlockDie, Keys_or_Money, PLATFORM_WIDTH, PLATFORM_HEIGHT
from characters import Character
import player
import pygame
from victory_window import victory_final
import sqlite3

size = WIDTH, HEIGHT = 800, 600
FPS = 60
player_sprite = pygame.sprite.GroupSingle()
all_sprites = pygame.sprite.Group()  # Все объекты
animatedEntities = pygame.sprite.Group()  # все анимированные объекты, за исключением героя
characters = pygame.sprite.Group()  # Все передвигающиеся объекты
bullets = pygame.sprite.Group()
oppon_sprites = pygame.sprite.Group()
bullets_player = pygame.sprite.Group()
keys = pygame.sprite.Group()
money = pygame.sprite.Group()

platforms = []  # опоры
opponents = []


class Opponent(pygame.sprite.Sprite):
    opponent_img = pygame.image.load("data\img\witch.png")

    def __init__(self, x, y, numside):
        pygame.sprite.Sprite.__init__(self)
        if numside == 'right':
            self.image = pygame.transform.flip(Opponent.opponent_img, True, False)
        self.image = pygame.transform.scale(Opponent.opponent_img, (42, 30))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = 0

    def update(self):
        if pygame.sprite.spritecollide(self, bullets_player, False):
            self.kill()

    def retern_data(self):
        return self.rect.centerx - 40, self.rect.top + 25


class Bullet(pygame.sprite.Sprite):
    bullet_img = pygame.image.load("data\img\molnia.png")
    bullet_player_img = pygame.image.load("data\img\laserRed16.png")

    def __init__(self, x, y, num_side, player=False):
        pygame.sprite.Sprite.__init__(self)
        if not player:
            self.image = pygame.transform.scale(Bullet.bullet_img, (26, 6))
            self.image.set_colorkey((0, 0, 0))
            speed = 26
        else:
            self.image = pygame.transform.scale(Bullet.bullet_player_img, (24, 6))
            self.image.set_colorkey((255, 255, 255))
            speed = 9
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        if num_side == 'right':
            self.speedx = speed
        else:
            self.speedx = -speed

    def update(self):
        self.rect.x += self.speedx
        # убить, если он тронулся стенки
        if self.collide(platforms):
            self.kill()

    def collide(self, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p) and self != p:  # если с чем-то или кем-то столкнулись
                return True
        return False


class Camera:
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIDTH / 2, -t + HEIGHT / 2

    l = min(0, l)  # запрет передвижения слева граница
    l = max(-(camera.width - WIDTH), l)  # запрет передвижения справа граница
    t = max(-(camera.height - HEIGHT), t)  # запрет передвижения снизу граница
    t = min(0, t)  # запрет передвижения вверху граница

    return pygame.Rect(l, t, w, h)


def loadLevel(card):
    global playerX, playerY  # объявляем глобальные переменные, это координаты героя
    lvl = []
    levelFile = open(card)
    line = " "
    commands = []
    while line[0] != "/":
        line = levelFile.readline()
        if line[0] == "[":  # знак открытия уровня
            while line[0] != "]":  # знак закрытия уровня
                line = levelFile.readline()
                if line[0] != "]":
                    endLine = line.find("|")  # знак конца строки
                    lvl.append(line[0: endLine])

        if line[0] != "":
            commands = line.split()
            if len(commands) > 1:  # работа с коммандами
                if commands[0] == "player":
                    playerX = int(commands[1])
                    playerY = int(commands[2])
                elif commands[0] == "monster":
                    mn = Character(int(commands[1]), int(commands[2]), int(commands[3]), int(commands[4]),
                                   int(commands[5]), int(commands[6]))
                    all_sprites.add(mn)
                    platforms.append(mn)
                    characters.add(mn)
                elif commands[0] == 'witch':
                    wt = Opponent(int(commands[1]), int(commands[2]), commands[3])
                    all_sprites.add(wt)
                    oppon_sprites.add(wt)
                    opponents.append(tuple([wt, commands[3]]))
                elif commands[0] == "portal":  # если первая команда portal, то создаем портал
                    tp = BlockTeleport(int(commands[1]), int(commands[2]), int(commands[3]), int(commands[4]))
                    all_sprites.add(tp)
                    platforms.append(tp)
                    animatedEntities.add(tp)
    return lvl


def start_screen(var):
    screen = pygame.display.set_mode((800, 640), 0, 32)
    if var == 'start':
        fon = pygame.transform.scale(pygame.image.load('data\display\_reg1.jpg'), (800, 640))
    elif var == 'time':
        fon = pygame.transform.scale(pygame.image.load('data\display\_reg2.jpg'), (800, 640))
    while True:
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                all_sprites.empty()
                player_sprite.empty()
                animatedEntities.empty()
                characters.empty()
                bullets.empty()
                oppon_sprites.empty()
                bullets_player.empty()
                platforms.clear()
                opponents.clear()
                keys.empty()
                return
        pygame.display.flip()


def generate_level(level):
    x = 0
    y = 0
    for row in level:
        for col in row:
            if col == "=":
                pf_up = Platform(x, y, '=')
                all_sprites.add(pf_up)
                platforms.append(pf_up)
            elif col == "-":
                pf = Platform(x, y, '-')
                all_sprites.add(pf)
                platforms.append(pf)
            elif col == "*":
                bd = BlockDie(x, y)
                all_sprites.add(bd)
                platforms.append(bd)
            elif col == "P":
                pr = Princess(x, y)
                all_sprites.add(pr)
                platforms.append(pr)
                animatedEntities.add(pr)
            elif col == '+':
                key = Keys_or_Money(x, y)
                all_sprites.add(key)
                keys.add(key)
            elif col == '$':
                moneta = Keys_or_Money(x, y, 'money')
                all_sprites.add(moneta)
                money.add(moneta)
            x += PLATFORM_WIDTH
        y += PLATFORM_HEIGHT
        x = 0


def working_with_database(id_player, card, money_kolvo):
    con = sqlite3.connect('users.db')
    cur = con.cursor()
    value = cur.execute(
        f"""SELECT kolvo_money, lvl FROM users WHERE id='{id_player}'""").fetchone()
    lvl = 1
    if int(value[1]) < 3 and int(value[1]) == int(card[-5]):
        lvl = int(card[-5]) + 1
    elif int(value[1]) > int(card[-5]):
        lvl = (value[1])
    cur.execute(
        f"""UPDATE users SET kolvo_money = {int(value[0]) + money_kolvo},
               lvl = '{lvl}'
               WHERE id = '{id_player}'""")
    con.commit()
    con.close()


def play(play_time, card, name_use_plarformer, id_player):
    start_screen('start')
    clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Prince Of Voronezh")
    bg = pygame.Surface((WIDTH, HEIGHT))
    # будем использовать как фон
    bg.fill(pygame.Color((255, 255, 255)))
    # Игровое время
    font = pygame.font.SysFont(None, 50)
    text_time = font.render(str(play_time), True, (255, 255, 255))
    timer_event = play_time
    pygame.time.set_timer(timer_event, 1000)

    keys_kolvo = 0
    text_kolvo_keys = font.render(str(keys_kolvo), True, (237, 60, 202))

    money_kolvo = 0
    text_kolvo_money = font.render(str(money_kolvo), True, (24, 100, 234))

    level = loadLevel(card)
    generate_level(level)

    left = False
    right = False  # по умолчанию - стоим
    up = False
    running = False
    num_side_player = 'right'
    play = player.Player(playerX, playerY, name_use_plarformer)  # создаем героя по (x,y) координатам
    all_sprites.add(play)
    player_sprite.add(play)

    total_level_width = len(level[0]) * PLATFORM_WIDTH
    total_level_height = len(level) * PLATFORM_HEIGHT

    run = True
    camera = Camera(camera_configure, total_level_width, total_level_height)
    while not play.win and run:
        clock.tick(FPS)
        if play_time == 0:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            elif event.type == timer_event:
                play_time -= 1
                text_time = font.render(str(play_time), True, (255, 255, 255))

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                up = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                left = True
                player.num_move = 0
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                right = True
                player.num_move = 0
            elif event.type == pygame.KEYUP and event.key == pygame.K_UP:
                up = False
            elif event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                right = False
            elif event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                left = False
            # Функция стрельбы игрока при нажатии на пробел
            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                x, y = play.rect.x, play.rect.y + 15
                if num_side_player == 'right':
                    bullet = Bullet(x, y, 'right', True)
                else:
                    bullet = Bullet(x, y, 'left', True)
                all_sprites.add(bullet)
                bullets_player.add(bullet)
        if right:
            num_side_player = 'right'
        elif left:
            num_side_player = 'left'

        if play_time % 3 == 0:
            for opponent in opponents:
                if opponent[0] not in oppon_sprites:
                    del opponents[opponents.index(opponent)]
                else:
                    x, y = opponent[0].rect.x, opponent[0].rect.y + 20
                    if opponent[1] == 'right':
                        x += 35
                    bullet = Bullet(x, y, opponent[1])
                    all_sprites.add(bullet)
                    bullets.add(bullet)

        screen.blit(bg, (0, 0))  # отрисовка
        animatedEntities.update()  # показываем анимацию

        characters.update(platforms)  # передвигаем всех монстров
        oppon_sprites.update()
        bullets.update()
        bullets_player.update()
        camera.update(play)  # наводим камеру на игрока
        play.update(left, right, up, running, platforms, keys_kolvo)  # передвижение
        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite))

        text_x = WIDTH // 2 - text_time.get_width() // 2
        text_y = HEIGHT // 2 - text_time.get_height() // 2
        text_w = text_time.get_width()
        text_h = text_time.get_height()
        pygame.draw.rect(screen, (0, 0, 0), (text_x - 353, text_y + 243,
                                             text_w + 20, text_h + 20))
        screen.blit(text_time, (30, 540))  # Выставление часов

        if pygame.sprite.spritecollide(play, bullets, False):
            play.die()

        for key in keys:
            if pygame.sprite.collide_mask(key, play):
                key.kill()
                keys_kolvo += 1
                text_kolvo_keys = font.render(str(keys_kolvo), True, (234, 127, 234))
        for moneta in money:
            if pygame.sprite.collide_mask(moneta, play):
                moneta.kill()
                money_kolvo += 1
                text_kolvo_money = font.render(str(money_kolvo), True, (24, 100, 234))

        pygame.draw.rect(screen, (0, 0, 0), (0, 0, 100, 60))
        screen.blit(text_kolvo_keys, (20, 20))
        screen.blit(pygame.transform.scale(Keys_or_Money.img_key, (30, 30)), (50, 20))

        pygame.draw.rect(screen, (0, 0, 0), (700, 0, 100, 60))
        screen.blit(text_kolvo_money, (720, 20))
        screen.blit(pygame.transform.scale(Keys_or_Money.img_moneta, (30, 30)), (750, 20))
        pygame.display.update()

    if run:
        if not play.win:
            start_screen('time')
            return 'Проигрыш'
        else:
            working_with_database(id_player, card, money_kolvo)
            victory_final(screen, clock)
            return 'Победа'
