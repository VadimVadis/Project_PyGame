import pygame
import pygame_gui


class Rule:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Prince Of Voronezh')
        self.window_surface = pygame.display.set_mode((800, 600))
        self.background = pygame.image.load('images/rules.jpg')
        self.manager = pygame_gui.UIManager((800, 600))

        self.return_back = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((20, 500), (150, 50)),
            text='Вернуться назад',
            manager=self.manager
        )
        self.clock = pygame.time.Clock()
        self.rul()

    def rul(self):
        running = True
        time_delta = self.clock.tick(60) / 1000.0
        while running:
            self.window_surface.blit(self.background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.USEREVENT:
                    self.window_surface.blit(self.background, (0, 0))
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.return_back:
                            running = False
                self.manager.process_events(event)
            self.manager.update(time_delta)
            self.manager.draw_ui(self.window_surface)
            pygame.display.update()
