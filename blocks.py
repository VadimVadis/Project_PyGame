from main_play import *
import pygame

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32

ANIMATION_BLOCKTELEPORT = ['data\_blocks/portal2.png', 'data\_blocks/portal1.png']

ANIMATION_PRINCESS = ['data\_blocks/princess_l.png', 'data\_blocks/princess_r.png']


class Platform(pygame.sprite.Sprite):
    platform3 = pygame.image.load("data\_blocks/platform3.png")
    platform = pygame.image.load("data\_blocks/platform.png")

    def __init__(self, x, y, name_platform=None):
        super().__init__()
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        if name_platform == '=':
            self.image = Platform.platform
        elif name_platform == '-':
            self.image = Platform.platform3
        self.image.set_colorkey(pygame.Color((0, 0, 0)))
        self.rect = pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class BlockDie(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = pygame.image.load("data\_blocks/dieBlock.png")


class BlockTeleport(Platform):
    def __init__(self, x, y, goX, goY):
        Platform.__init__(self, x, y)
        self.goX = goX  # координаты назначения перемещения
        self.goY = goY  # координаты назначения перемещения
        self.num_move = 0

    def update(self):
        self.num_move += 1
        if self.num_move / 20 > 2:
            self.num_move = 0
        elif self.num_move % 20 in [1, 0]:
            self.image = pygame.image.load(ANIMATION_BLOCKTELEPORT[self.num_move // 20 - 1])


class Princess(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.num_move = 0

    def update(self):
        self.num_move += 1
        if self.num_move / 20 > 2:
            self.num_move = 0
        elif self.num_move % 20 in [1, 0]:
            self.image = pygame.image.load(ANIMATION_PRINCESS[self.num_move // 20 - 1])


class Keys_or_Money(pygame.sprite.Sprite):
    img_key = pygame.image.load("data\img\key.png")
    img_moneta = pygame.image.load("data\img\money.png")

    def __init__(self, x, y, mpney_or_key='key'):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        if mpney_or_key == 'key':
            self.image = pygame.transform.scale(Keys_or_Money.img_key, (32, 32))
        else:
            self.image = pygame.transform.scale(Keys_or_Money.img_moneta, (32, 32))
        self.rect = pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

    def update(self):
        if pygame.sprite.spritecollide(self, player_sprite, False):
            self.kill()
