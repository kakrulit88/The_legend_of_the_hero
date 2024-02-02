import pygame
import sys
from Level_and_camera import *
from Menu import *
from Hud import *


class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption('The legend of the hero')
        self.clock = pygame.time.Clock()

        self.level = Level()

        self.menu = Menu(self.level.player)

        self.menu.main_menu()
        self.menu.prestory()
        self.menu.transition()
        self.run()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game_start = Game()
