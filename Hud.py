import pygame
from Settings import *


class HUD():
    def __init__(self, player):
        self.surface = pygame.display.get_surface()
        self.font = pygame.font.Font(font, font_size)
        self.player = player

        self.bg_rect_health = None
        self.bg_rect_energy = None

    def update(self):
        # health and energy
        self.bg_rect_health = pygame.Rect(8, 8, health_bar_height + 4, health_bar_width + 4)
        self.bg_rect_energy = pygame.Rect(8, 43, energy_bar_height + 4, energy_bar_width + 4)

        self.current_heath_len = health_bar_height * (self.player.health * 2 / health_bar_height)
        self.current_energy_len = energy_bar_height * (self.player.energy * 2 / energy_bar_height)

        self.health_bar_rect = pygame.Rect(10, 10, self.current_heath_len, health_bar_width)
        self.energy_bar_rect = pygame.Rect(10, 45, self.current_energy_len, energy_bar_width)

        pygame.draw.rect(self.surface, (165, 165, 165), self.bg_rect_health)
        pygame.draw.rect(self.surface, (165, 165, 165), self.bg_rect_energy)

        pygame.draw.rect(self.surface, 'black', self.bg_rect_health, 2)
        pygame.draw.rect(self.surface, 'black', self.bg_rect_energy, 2)

        pygame.draw.rect(self.surface, (248, 23, 62), self.health_bar_rect)
        pygame.draw.rect(self.surface, (21, 96, 189), self.energy_bar_rect)

        # exp
        exp_text = self.font.render(f'Score:   {self.player.exp}', True, 'white')

        self.x = self.surface.get_size()[0] - 130
        self.y = 30

        exp_text_rect = exp_text.get_rect(center=(self.x, self.y))
        self.surface.blit(exp_text, exp_text_rect)
