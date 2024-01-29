import pygame
from math import sin


class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.direction = [0, 0]
        self.end_game = False

        # sounds
        self.sounds = []

        self.walk_sound_grass = pygame.mixer.Sound('data/Sounds/Game/walk_on_grass.mp3')
        self.walk_sound_grass.set_volume(0.7)
        self.walk_sound_stone = pygame.mixer.Sound('data/Sounds/Game/walk_on_grass.mp3')
        self.walk_sound_stone.set_volume(0.3)

        self.sounds = [self.walk_sound_grass, self.walk_sound_stone]
        self.sound_index = 0
        self.sound_playing = True

    def move(self, speed):
        if (self.direction[0] != 0 or self.direction[1] != 0) and not self.end_game and self.sprite_type == 'player':
            if self.sound_playing:
                self.sounds[self.sound_index].play(loops=-1)
                self.sound_playing = False
        else:
            self.sounds[self.sound_index].stop()
            self.sound_playing = True
        self.hitbox.x += self.direction[0] * speed
        self.colusion(self.direction, 'x')
        self.hitbox.y += self.direction[1] * speed
        self.colusion(self.direction, 'y')
        self.rect.center = self.hitbox.center

    def colusion(self, direction, space):
        if space == 'x':
            for sprite in self.obstical_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction[0] > 0:
                        self.hitbox.right = sprite.hitbox.left
                    elif direction[0] < 0:
                        self.hitbox.left = sprite.hitbox.right
        elif space == 'y':
            for sprite in self.obstical_sprites:
                if sprite.sprite_type == 'переход':
                    if sprite.hitbox.colliderect(self.hitbox):
                        self.next_level = True
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction[1] > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    elif direction[1] < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def hit_animation(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        return 0
