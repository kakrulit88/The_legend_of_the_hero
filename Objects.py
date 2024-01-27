import pygame
from Particles import *


class Object(pygame.sprite.Sprite):
    def __init__(self, pos, group, sprite_type, image=None):
        super().__init__(group)
        self.sprite_type = sprite_type
        if image:
            self.image = pygame.image.load(image).convert_alpha()
        else:
            self.image = pygame.Surface((64, 64))
        self.mask = pygame.mask.from_surface(self.image).outline()
        self.pos = pos
        self.rect = self.image.get_rect(topleft=(pos))
        self.hitbox = self.rect.inflate(-8, -8)
