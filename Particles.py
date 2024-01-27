import pygame
from Settings import *
from random import choice


class Particles_settings():
    def __init__(self):
        self.particles_type = None
        self.particles_frames = particles
        self.flip_particles()

    def flip_particles(self):
        for leafs in range(len(self.particles_frames['leafs'])):
            flipped_particles = []
            for particle in self.particles_frames['leafs'][leafs]:
                particle_image = pygame.transform.flip(particle, True, False)
                flipped_particles.append(particle_image)
            self.particles_frames['leafs'].append(flipped_particles)

    def create_grass_particles(self, group, pos):
        leaf_particles = choice(self.particles_frames['leafs'])
        Particle(group, pos, leaf_particles, 'dynamic')

    def create_attack_particles(self, group, pos, attack_type):
        attack_particles = self.particles_frames[attack_type]
        Particle(group, pos, attack_particles, 'dynamic')

    def create_death_particles(self, group, pos, death_type):
        death_particles = self.particles_frames[death_type]
        Particle(group, pos, death_particles, 'dynamic')

    def create_shadow_particles(self, group, pos):
        shadow_particles = [pygame.image.load('data/animations/Shadow.png')]
        Particle(group, pos, shadow_particles, 'static')



class Particle(pygame.sprite.Sprite):
    def __init__(self, group, pos, animations, particle_type):
        super().__init__(group)
        self.particle_type = particle_type
        self.sprite_type = 'particle'
        self.animations_index = 0
        self.animations_speed = 0.15
        self.particles_animations = animations

        self.image = self.particles_animations[self.animations_index]
        self.rect = self.image.get_rect(center=(pos))

    def animate(self):
        if self.particle_type == 'dynamic':
            self.animations_index += self.animations_speed
            if self.animations_index >= len(self.particles_animations):
                self.kill()
            else:
                self.image = self.particles_animations[int(self.animations_index)]
        else:
            self.image = self.particles_animations[int(self.animations_index)]

    def update(self):
        self.animate()
