import pygame
from Settings import *
from Game_init import *
from Entity import *
from Particles import *


class Enemy(Entity):
    def __init__(self, pos, groups, monster_name, obstical_sprites, all_visible_sprites):
        super().__init__(groups)
        self.monster_name = monster_name
        self.sprite_type = 'enemy'
        self.alive = True

        self.image = pygame.image.load(monsters[self.monster_name]['idle'][0]).convert_alpha()
        self.rect = self.image.get_rect(topleft=(pos))
        self.mask = pygame.mask.from_surface(self.image)
        self.hitbox = self.rect.inflate(-20, -20)

        self.obstical_sprites = obstical_sprites
        self.all_visible_sprites = all_visible_sprites

        self.player = None

        # stats
        self.health = monsters[self.monster_name]['health']
        self.damage = monsters[self.monster_name]['damage']
        self.speed = monsters[self.monster_name]['speed']
        self.resistance = monsters[self.monster_name]['resistance']
        self.type_attack = monsters[self.monster_name]['type_attack']
        self.attack_radius = monsters[self.monster_name]['attack_radius']
        self.notice_radius = monsters[self.monster_name]['notice_radius']
        self.enemy_attack_cooldown = monsters[self.monster_name]['attack_cooldown']
        self.exp = monsters[self.monster_name]['exp']

        # collision with player
        self.collision_timer = True
        self.collision_timer_cooldown = 300
        self.hit_time = 0

        # animation
        self.frame_time = 0
        self.frame_time_hit = 0
        self.animation_speed = 0.10

        # attack
        self.attack_possible = True
        self.attack_time = None
        self.direction = None
        self.distance = None

        # particles
        self.particles = Particles_settings()

        # sounds
        self.getting_exp = pygame.mixer.Sound('data/Sounds/Game/exp.wav')
        self.getting_exp.set_volume(0.1)
        self.death_sound = pygame.mixer.Sound('data/Sounds/Game/death.wav')
        self.death_sound.set_volume(0.1)
        self.hit_sound = pygame.mixer.Sound('data/Sounds/Game/hit7.wav')
        self.hit_sound.set_volume(0.008)
        self.end_theme = pygame.mixer.Sound('data/Sounds/Game/End.ogg')
        self.end_theme.set_volume(0.05)
        self.hited_sound = pygame.mixer.Sound('data/Sounds/Game/hit4.wav')
        self.hited_sound.set_volume(0.08)
        self.walk_sound_grass = pygame.mixer.Sound('data/Sounds/Game/walk_on_grass.mp3')
        self.walk_sound_grass.set_volume(0.7)

        self.end_game = False


    def enemy_update(self, player):
        if self.alive:
            self.player = player
            enemy_vect = pygame.math.Vector2(self.rect.center)
            player_vect = pygame.math.Vector2(player.rect.center)
            self.distance = (player_vect - enemy_vect).magnitude()

            if self.distance > 0:
                self.direction = (player_vect - enemy_vect).normalize()
            else:
                self.direction = pygame.math.Vector2()

            if self.distance <= self.attack_radius and self.attack_possible:
                self.action = 'attack'
                self.attack_possible = False
                player.get_damage(self.damage, self.type_attack)
                self.hit_sound.play()
                self.attack_time = pygame.time.get_ticks()

            elif self.distance <= self.notice_radius:
                self.action = 'move_to_player'
            else:
                self.action = 'idle'
                self.direction = pygame.math.Vector2()

    def animate(self):
        self.frame_time += self.animation_speed
        if self.frame_time >= len(monsters[self.monster_name]['idle']):
            self.frame_time = 0

        # shadows
        if self.monster_name == 'slime' or self.monster_name == 'GiantSpirit':
            pass
        else:
            self.particles.create_shadow_particles([self.all_visible_sprites], (self.rect.midbottom[0], self.rect.midbottom[1] - 5))

        self.image = pygame.image.load(monsters[self.monster_name]['idle'][int(self.frame_time)]).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image).outline()
        self.rect = self.image.get_rect(center=(self.hitbox.center))

        if not self.collision_timer:
            if self.monster_name == 'GiantSpirit':
                self.frame_time_hit += self.animation_speed
                if self.frame_time_hit >= len(monsters[self.monster_name]['hit']):
                    self.frame_time_hit = 0
                self.image = pygame.image.load(monsters[self.monster_name]['hit'][int(self.frame_time_hit)]).convert_alpha()
            else:
                self.image.set_alpha(self.hit_animation())
        else:
            self.image.set_alpha(255)

    def attack_cooldown(self):
        if not self.attack_possible:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_time >= self.enemy_attack_cooldown:
                self.attack_possible = True

    def colusion_cooldown(self, hit_time):
        if not self.collision_timer:
            current_time = pygame.time.get_ticks()
            if current_time - hit_time >= self.collision_timer_cooldown:
                self.collision_timer = True

    def repulsion(self):
        if not self.collision_timer:
            self.direction *= -self.resistance

    def get_damage(self, player):
        if self.collision_timer:
            self.health -= player.weapon.damage
            self.hit_time = pygame.time.get_ticks()
            self.collision_timer = False
            if self.monster_name == 'GiantSpirit':
                self.hited_sound.play()

    def check_death(self):
        if self.health <= 0:
            if self.monster_name == 'bamboo':
                pos = self.rect.center
                self.particles.create_death_particles([self.all_visible_sprites], pos, 'bamboo_death')
                self.kill()
            elif self.monster_name == 'GiantSpirit':
                self.end_game = True
                self.end_theme.play()
            else:
                self.image = pygame.image.load(monsters[self.monster_name]['dead']).convert_alpha()

            # exp
            if self.alive:
                self.player.exp += self.exp
                self.getting_exp.play()
            self.alive = False

    def update(self):
        self.check_death()
        if self.alive:
            self.repulsion()
            self.move(self.speed)
            self.animate()
            self.attack_cooldown()
            self.colusion_cooldown(self.hit_time)
