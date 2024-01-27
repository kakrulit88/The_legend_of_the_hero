import pygame
from Settings import *


class Weapon(pygame.sprite.Sprite):
    def __init__(self, direction, group, player, weapon_name):
        super().__init__(group)
        self.image = pygame.Surface((40, 40))
        self.mask = pygame.mask.from_surface(self.image)
        self.player = player
        self.direction = direction
        self.weapon_name = weapon_name
        self.damage = weapons[self.weapon_name]['damage']

        self.sprite_type = 'weapon'

        if self.direction == 'right':
            self.image = pygame.image.load(weapons[self.weapon_name]['image'][2]).convert_alpha()
            self.rect = self.image.get_rect(midleft=(player.rect.midright[0] - 20, player.rect.midright[1] + 15))
        elif self.direction == 'left':
            self.image = pygame.image.load(weapons[self.weapon_name]['image'][3]).convert_alpha()
            self.rect = self.image.get_rect(midright=(player.rect.midleft[0] + 20, player.rect.midleft[1] + 15))

        elif self.direction == 'up':
            self.image = pygame.image.load(weapons[self.weapon_name]['image'][0]).convert_alpha()
            self.rect = self.image.get_rect(midbottom=(player.rect.midtop[0] - 16, player.rect.midtop[1] + 20))
        elif self.direction == 'down':
            self.image = pygame.image.load(weapons[self.weapon_name]['image'][1]).convert_alpha()
            self.rect = self.image.get_rect(midtop=(player.rect.midbottom[0] - 8, player.rect.midbottom[1] - 20))
