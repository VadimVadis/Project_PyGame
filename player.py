import pygame
import blocks
import characters

MOVE_SPEED = 5
JUMP_POWER = 7
GRAVITY = 0.35  # Сила, которая будет тянуть нас вниз


class Animate:
    def __init__(self, name_person):
        self.ANIMATION_RIGHT = [pygame.image.load(f'data\platformers/{name_person}/r1.png'),
                                pygame.image.load(f'data\platformers/{name_person}/r2.png'),
                                pygame.image.load(f'data\platformers/{name_person}/r3.png')]
        self.ANIMATION_LEFT = [pygame.image.load(f'data\platformers/{name_person}/l1.png'),
                               pygame.image.load(f'data\platformers/{name_person}/l2.png'),
                               pygame.image.load(f'data\platformers/{name_person}/l3.png')]

        self.ANIMATION_JUMP_LEFT = pygame.image.load(f'data\platformers/{name_person}/jl.png')
        self.ANIMATION_JUMP_RIGHT = pygame.image.load(f'data\platformers/{name_person}/jr.png')
        self.ANIMATION_JUMP = pygame.image.load(f'data\platformers/{name_person}/j.png')
        self.ANIMATION_STAY = pygame.image.load(f'data\platformers/{name_person}/0.png')


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, name_use_plarformer):
        self.amimation = Animate(name_use_plarformer)
        pygame.sprite.Sprite.__init__(self)
        self.xvel = 0  # скорость перемещения. 0 - стоять на месте
        self.startX = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.yvel = 0  # скорость вертикального перемещения
        self.onGround = False  # На земле ли я?
        self.image = self.amimation.ANIMATION_STAY
        self.rect = pygame.Rect(x, y, 21, 29)
        self.image.set_colorkey(pygame.Color((255, 255, 255)))
        self.num_move = 0
        self.num_move_every_other = 0
        self.win = False

    def update(self, left, right, up, running, platforms, keys_kolvo):
        if up:
            if self.onGround:  # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -JUMP_POWER
                self.image = self.amimation.ANIMATION_JUMP

        if left:
            self.xvel = -MOVE_SPEED  # Лево = x- n
            if not up:  # и не прыгаем
                self.num_move += 1
                if self.num_move / 5 > len(self.amimation.ANIMATION_LEFT) - 1:
                    self.num_move = 0
                if self.num_move % 5 == 0:
                    self.image = self.amimation.ANIMATION_LEFT[self.num_move // 5]
            if up:  # если же прыгаем
                self.image = self.amimation.ANIMATION_JUMP_LEFT

        elif right:
            self.xvel = MOVE_SPEED  # Право = x + n
            if not up:
                self.num_move += 1
                if self.num_move / 5 > len(self.amimation.ANIMATION_RIGHT) - 1:
                    self.num_move = 0
                if self.num_move % 5 == 0:
                    self.image = self.amimation.ANIMATION_RIGHT[self.num_move // 5]
            if up:
                self.image = self.amimation.ANIMATION_JUMP_RIGHT

        elif not (left or right):  # стоим, когда нет указаний идти
            self.xvel = 0
            if not up:
                self.image = self.amimation.ANIMATION_STAY

        if not self.onGround:
            self.yvel += GRAVITY

        self.onGround = False  # Мы не знаем, когда мы на земле((
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms, keys_kolvo)

        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms, keys_kolvo)

        self.image.set_colorkey(pygame.Color((255, 255, 255)))

    def collide(self, xvel, yvel, platforms, keys_kolvo):
        for platform in platforms:
            if pygame.sprite.collide_rect(self, platform):  # если есть пересечение платформы с игроком
                if isinstance(platform, blocks.BlockDie) or isinstance(platform,
                                                                       characters.Character):  # если пересакаемый блок - blocks.BlockDie или Monster
                    self.die()  # умираем
                elif isinstance(platform, blocks.BlockTeleport) and keys_kolvo == 3:
                    self.teleporting(platform.goX, platform.goY)
                elif isinstance(platform, blocks.Princess):  # если коснулись принцессы
                    self.win = True  # победили!!!
                else:
                    if xvel > 0:  # если движется вправо
                        self.rect.right = platform.rect.left  # то не движется вправо

                    if xvel < 0:  # если движется влево
                        self.rect.left = platform.rect.right  # то не движется влево

                    if yvel > 0:  # если падает вниз
                        self.rect.bottom = platform.rect.top  # то не падает вниз
                        self.onGround = True  # и становится на что-то твердое
                        self.yvel = 0  # и энергия падения пропадает

                    if yvel < 0:  # если движется вверх
                        self.rect.top = platform.rect.bottom  # то не движется вверх
                        self.yvel = 0  # и энергия прыжка пропадает

    def die(self):
        pygame.time.wait(300)
        self.teleporting(self.startX, self.startY)  # перемещаемся в начальные координаты

    def teleporting(self, goX, goY):
        self.rect.x = goX
        self.rect.y = goY
