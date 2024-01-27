import pygame
from Settings import *
from Weapon import *
from Level_and_camera import *
from Entity import *
from Particles import *
from Level_and_camera import *
from random import randrange


class Player(Entity):
    def __init__(self, pos, group, obstical_sprites, all_visible_sprites, attack_sprites, attackable_sprites):
        super().__init__(group)
        self.sprite_type = 'player'

        self.image = pygame.image.load(player_animation['down_idle']).convert_alpha()
        self.rect = self.image.get_rect(topleft=(pos))
        self.mask = pygame.mask.from_surface(self.image)
        self.hitbox = self.rect.inflate(-10, 0)

        self.obstical_sprites = obstical_sprites
        self.all_visible_sprites = all_visible_sprites
        self.attack_sprites = attack_sprites
        self.attackable_sprites = attackable_sprites

        self.direction = [0, 0]

        # stats
        self.alive = True
        self.health = player_stats['health']
        self.energy = player_stats['energy']
        self.speed = player_stats['speed']
        self.exp = player_stats['exp']

        # energy
        self.energycooldown = 1500
        self.not_energy_time = 0
        self.energy_heal = False

        # attack
        self.attacked = False
        self.attacking = False
        self.attack_cooldown_time = 300
        self.attacked_cooldown_time = 500
        self.attack_time = pygame.time.get_ticks()
        self.weapon = None

        # timer
        self.istimer = False
        self.delay = 700
        self.timer_start = 0

        # animation
        self.animation_speed = 0.15
        self.frame_time = 0
        self.animation_direction = player_animation['down_idle']
        self.last_direction = 'down'

        # sounds
        self.weapon_sound = pygame.mixer.Sound('data/Sounds/Game/sword2.wav')
        self.weapon_sound.set_volume(0.008)
        self.hit_sound = pygame.mixer.Sound('data/Sounds/Game/hit7.wav')
        self.hit_sound.set_volume(0.008)

        # particles
        self.particles = Particles_settings()

        self.dialog = False

        self.next_level = False

    def new_direction(self):
        keys = pygame.key.get_pressed()
        if not self.attacking:
            if keys[pygame.K_w]:
                self.direction[1] = -1
                self.animation_direction = player_animation['up']
                self.last_direction = 'up'
            elif keys[pygame.K_s]:
                self.direction[1] = 1
                self.animation_direction = player_animation['down']
                self.last_direction = 'down'
            else:
                self.direction[1] = 0
                self.animation_direction = player_animation['down_idle']

            if keys[pygame.K_d]:
                self.direction[0] = 1
                self.animation_direction = player_animation['right']
                self.last_direction = 'right'
            elif keys[pygame.K_a]:
                self.direction[0] = -1
                self.animation_direction = player_animation['left']
                self.last_direction = 'left'
            else:
                self.direction[0] = 0

            if (self.direction == [-1, -1] or self.direction == [1, -1]
                    or self.direction == [1, 1] or self.direction == [-1, 1]):
                self.direction = [self.direction[0] * 0.707, self.direction[1] * 0.707]

            if keys[pygame.K_TAB]:
                self.health += 20

            self.move(self.speed)

    def animation(self):
        self.frame_time += self.animation_speed
        if self.frame_time > len(self.animation_direction):
            self.frame_time = 0
        # shadow
        self.particles.create_shadow_particles([self.all_visible_sprites] , (self.rect.midbottom[0], self.rect.midbottom[1] - 5))
        # move animation
        if not self.attacking:
            if self.animation_direction != player_animation['down_idle']:
                self.image = pygame.image.load(self.animation_direction[int(self.frame_time)]).convert_alpha()
                self.mask = pygame.mask.from_surface(self.image).outline()
            else:
                self.image = pygame.image.load(player_animation[self.last_direction + '_idle']).convert_alpha()
                self.mask = pygame.mask.from_surface(self.image).outline()
            self.rect = self.image.get_rect(center=(self.hitbox.center))
        # attack animation
        else:
            self.image = pygame.image.load(player_animation['attack'][self.last_direction + '_attack']).convert_alpha()
            self.mask = pygame.mask.from_surface(self.image).outline()

        # player attacked effects
        if self.attacked:
            self.attacked_time = pygame.time.get_ticks()
            self.attacked_cooldown()
        else:
            self.image.set_alpha(255)

    def create_attack(self, keys):
        if keys[pygame.K_SPACE] and not self.attacking and not self.istimer:
            self.istimer = True
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.timer_start = pygame.time.get_ticks()
            self.weapon_sound.play()
            self.weapon = Weapon(self.last_direction, [self.all_visible_sprites, self.attack_sprites], self, 'lance')

        self.attack_cooldown()
        self.timer()

    def attack_cooldown(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            self.image.set_alpha(self.hit_animation())
            if current_time - self.attack_time >= self.attack_cooldown_time:
                self.attacking = False
                if self.weapon:
                    self.weapon.kill()
                    self.weapon = None


    def timer(self):
        current_time = pygame.time.get_ticks()
        if self.istimer and not self.attacking:
            if current_time - self.timer_start >= self.delay:
                self.istimer = False




    def attacked_cooldown(self):
        current_time = pygame.time.get_ticks()
        if self.attacked:
            self.image.set_alpha(self.hit_animation())
            if current_time - self.attack_time >= self.attacked_cooldown_time:
                self.attacked = False

    def energy_cooldown(self):
        current_time = pygame.time.get_ticks()
        if self.energy_heal:
            if current_time - self.not_energy_time >= self.energycooldown:
                self.energy += 0.15
            if self.energy >= player_stats['energy']:
                self.energy_heal = False

    def energy_consumption(self, keys):
        if keys[pygame.K_LSHIFT]:
            if self.energy > 0:
                self.energy -= 0.45
                self.speed = player_stats['speed'] + 1.5
                self.not_energy_time = pygame.time.get_ticks()
            else:
                self.speed = player_stats['speed']
        elif not keys[pygame.K_LSHIFT]:
            self.speed = player_stats['speed']

        if not keys[pygame.K_LSHIFT] and not self.energy_heal:
            self.energy_heal = True
            self.not_energy_time = pygame.time.get_ticks()

        self.energy_cooldown()

    def sprites_attack_interaction(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                spisok_collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if spisok_collision_sprites:
                    for sprite in spisok_collision_sprites:
                        if sprite.sprite_type == 'трава':
                            pos = (sprite.rect.centerx, sprite.rect.centery - 30)
                            for i in range(randrange(3, 7)):
                                self.particles.create_grass_particles([self.all_visible_sprites], pos)
                            sprite.kill()
                        else:
                            sprite.get_damage(self)

    def get_damage(self, damage, attack_type):
        self.health -= damage
        self.particles.create_attack_particles([self.all_visible_sprites], self.rect.center, attack_type)
        self.attacked = True

    def check_death(self):
        if self.health <= 0:
            self.alive = False
            self.image = pygame.image.load(player_animation['dead']).convert_alpha()

    def update(self):
        self.check_death()
        if not self.dialog and self.alive:
            self.new_direction()
            self.create_attack(pygame.key.get_pressed())
            self.sprites_attack_interaction()
            self.energy_consumption(pygame.key.get_pressed())
            self.animation()
