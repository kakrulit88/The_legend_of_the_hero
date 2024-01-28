import pygame
from random import choice
from Settings import *
from Objects import Object
from Player import Player
from Hud import *
from math import atan2, tan
from Menu import *
from Enemy import *
from Dialogs import *


class Level():
    def __init__(self):
        self.surface = pygame.display.get_surface()
        self.all_visible_sprites = Camera('data/level_graphics/map.png',
                                          'data/level_graphics/map_above.png')
        self.obsticles_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        self.pict_slovar = pict_items

        self.player = None

        # create map
        self.create_map(slovar_layouts_level1, (1664, 2368))

        # hud
        self.hud = HUD(self.player)

        # sounds
        self.main_theme = pygame.mixer.Sound('data/Sounds/Game/main_theme.ogg')
        self.main_theme.set_volume(0.05)
        self.dungeon_theme = pygame.mixer.Sound('data/Sounds/Game/Dungeon.ogg')
        self.dungeon_theme.set_volume(0.05)
        self.dead_theme = pygame.mixer.Sound('data/Sounds/Game/GameOver.wav')
        self.dead_theme.set_volume(0.05)

        # dialogs
        self.dialogs = Dialogs(self.surface)
        self.is_dialog = True

        # menu
        self.menu = Menu(self.player)
        self.menu.game_sound.stop()
        self.end_game = False
        self.itog_text = ''

    def create_map(self, slovar_layouts, player_pos):
        self.player = Player(player_pos, [self.all_visible_sprites],
                             self.obsticles_sprites, self.all_visible_sprites, self.attack_sprites,
                             self.attackable_sprites)

        for layout_type, layout in slovar_layouts.items():
            for row_index, row in enumerate(layout):
                for colum_index, colum in enumerate(row):
                    x = colum_index * 64
                    y = row_index * 64

                    if layout_type == 'границы':
                        if layout[row_index][colum_index] == '4':
                            Object((x, y), [self.obsticles_sprites], 'граница')
                    if layout_type == 'трава':
                        if layout[row_index][colum_index] != '-1':
                            Object((x, y), [self.all_visible_sprites, self.obsticles_sprites, self.attackable_sprites],
                                   'трава',
                                   choice(self.pict_slovar['трава']))
                    if layout_type == 'переходы':
                        if layout[row_index][colum_index] != '-1':
                            Object((x, y), [self.obsticles_sprites], 'переход')
                    if layout_type == 'монстры':

                        if layout[row_index][colum_index] == '0':
                            Enemy((x, y), [self.all_visible_sprites, self.attackable_sprites], 'bamboo',
                                  self.obsticles_sprites, self.all_visible_sprites)
                        elif layout[row_index][colum_index] == '1':
                            Enemy((x, y), [self.all_visible_sprites, self.attackable_sprites], 'slime',
                                  self.obsticles_sprites, self.all_visible_sprites)
                        elif layout[row_index][colum_index] == '2':
                            Enemy((x, y), [self.all_visible_sprites, self.attackable_sprites], 'GiantSpirit',
                                  self.obsticles_sprites, self.all_visible_sprites)

    def check_new_level(self):
        if self.player.next_level:
            last_hp = self.player.health
            last_score = self.player.exp

            self.player.sounds[self.player.sound_index].stop()

            self.all_visible_sprites = Camera('data/level_graphics/lvl2_map.png',
                                              'data/level_graphics/lvl2_map_above.png')
            self.obsticles_sprites = pygame.sprite.Group()
            self.attack_sprites = pygame.sprite.Group()
            self.attackable_sprites = pygame.sprite.Group()

            self.player = None

            self.create_map(slovar_layouts_level2, (960, 1600))

            self.player.health = last_hp
            self.player.exp = last_score
            self.player.sound_index = 1

            self.hud = HUD(self.player)

            self.main_theme.stop()
            self.dungeon_theme.play(loops=-1)

    def check_game_end(self):
        for sprite in self.attackable_sprites:
            if sprite.sprite_type == 'enemy':
                if sprite.end_game is True:
                    self.end_game = True
                    sprite.kill()
                    self.dungeon_theme.stop()

    def check_player_death(self):
        if self.player.alive is False:
            self.player.sounds[self.player.sound_index].stop()
            self.end_game = True
            self.player.end_game = True
            self.player.sound_playing = False
            self.dungeon_theme.stop()
            self.main_theme.stop()
            self.dead_theme.play()

    def run(self):
        self.check_new_level()
        self.check_game_end()
        if not self.is_dialog:
            if not self.end_game:
                self.check_player_death()
                self.all_visible_sprites.camera_offset(self.player)
                self.all_visible_sprites.update_enemy(self.player)
                self.all_visible_sprites.update()
                self.hud.update()
            if self.end_game and self.player.health <= 0:
                self.itog_text = dead_text
            elif self.end_game and self.player.health > 0:
                self.itog_text = end_text
            if self.end_game:
                for sprite in self.attackable_sprites:
                    if sprite.sprite_type == 'enemy':
                        sprite.kill()
                self.all_visible_sprites.camera_offset(self.player)
                self.all_visible_sprites.update()
                self.hud.update()

                self.menu.transition2(self.itog_text, self.player.exp)

        else:
            self.player.dialog = True
            self.all_visible_sprites.camera_offset(self.player)
            self.dialogs.start_dialog()
            self.main_theme.play(loops=-1)

            self.is_dialog = False
            self.player.dialog = False


class Camera(pygame.sprite.Group):
    def __init__(self, map_img, map_behind_img):
        super().__init__()
        self.surface = pygame.display.get_surface()

        self.shadows = False

        self.compensation = [0, 0]
        self.ground_surface = pygame.image.load(map_img).convert_alpha()
        self.ground_rect = self.ground_surface.get_rect(topleft=(0, 0))

        self.ground_front_surface = pygame.image.load(map_behind_img).convert_alpha()
        self.ground_front_rect = self.ground_surface.get_rect(topleft=(0, 0))

    def camera_offset(self, player):
        # turn on/off shadows
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            self.shadows = True
        if keys[pygame.K_2]:
            self.shadows = False

        self.compensation[0] = player.rect.centerx - HEIGHT // 2
        self.compensation[1] = player.rect.centery - WIDTH // 2

        self.ground_rect_pos = (self.ground_rect.topleft[0] - self.compensation[0],
                                self.ground_rect.topleft[1] - self.compensation[1])

        self.ground_behind_rect_pos = (self.ground_front_rect.topleft[0] - self.compensation[0],
                                       self.ground_front_rect.topleft[1] - self.compensation[1])

        self.surface.blit(self.ground_surface, self.ground_rect_pos)
        if not self.shadows:
            for sprite in sorted(self.sprites(), key=lambda x: x.rect.centery):
                new_pos = (sprite.rect.x - self.compensation[0], sprite.rect.y - self.compensation[1])
                if sprite.sprite_type == 'particle' and sprite.particle_type == 'static':
                    self.surface.blit(sprite.image, new_pos)
                    sprite.kill()

        for sprite in sorted(self.sprites(), key=lambda x: x.rect.centery):
            new_pos = (sprite.rect.x - self.compensation[0], sprite.rect.y - self.compensation[1])
            if sprite.sprite_type == 'particle' and sprite.particle_type == 'static':
                continue
            self.surface.blit(sprite.image, new_pos)

            # shadows
            if self.shadows:
                if sprite.sprite_type == 'player' or sprite.sprite_type == 'enemy' or sprite.sprite_type == 'трава':
                    if sprite.sprite_type == 'player':
                        sprite.mask = [(x + 32, y) for x, y in sprite.mask]
                        shape_surf = pygame.Surface((1000, 1000), pygame.SRCALPHA)
                        pygame.draw.polygon(shape_surf, (0, 0, 0, 128),
                                            self.get_shadows(sprite.mask, sprite, (sprite.rect.x, sprite.rect.y)))
                        self.surface.blit(shape_surf, ((HEIGHT // 2 - 64), (WIDTH // 2 + 30)))

                    elif sprite.sprite_type == 'трава':
                        shape_surf = pygame.Surface((100, 100), pygame.SRCALPHA)
                        pygame.draw.polygon(shape_surf, (0, 0, 0, 128),
                                            self.get_shadows(sprite.mask, sprite, sprite.pos))
                        self.surface.blit(shape_surf, ((new_pos[0] - 20), (new_pos[1] + 52)))

                    elif sprite.sprite_type == 'enemy':
                        shape_surf = pygame.Surface((100, 100), pygame.SRCALPHA)
                        pygame.draw.polygon(shape_surf, (0, 0, 0, 128), self.get_shadows(sprite.mask, sprite, new_pos))
                        self.surface.blit(shape_surf, ((new_pos[0] - 22), (new_pos[1] + 59)))

        self.surface.blit(self.ground_front_surface, self.ground_behind_rect_pos)

    def get_shadows(self, mask, sprite, pos):
        sun_pos = pygame.Vector2(6000, 0)
        target_pos = pygame.Vector2(pos)
        # sun_angle = -0.4

        shadow_coords = []
        if sprite.sprite_type == 'player':
            sun_angle = atan2((sun_pos.y - target_pos.y), (sun_pos.x - target_pos.x))
            sun_angle = -0.4
            for x, y in mask:
                shadow_height = (18 - y) * 1.4
                shadow_width = shadow_height * tan(sun_angle)
                shadow_point = (x + shadow_width - 23, y + shadow_height)
                shadow_coords.append(shadow_point)
            return shadow_coords
        if sprite.sprite_type == 'enemy':
            for x, y in mask:
                sun_angle = atan2((sun_pos.y - target_pos.y), (sun_pos.x - target_pos.x))
                shadow_height = (18 - y) * 1.4
                shadow_width = shadow_height * tan(sun_angle)
                shadow_point = (x + shadow_width + 21, y + shadow_height)
                shadow_coords.append(shadow_point)
            return shadow_coords
        else:
            for x, y in mask:
                sun_angle = -0.4
                shadow_height = (15 - y) * 1.4
                shadow_width = shadow_height * tan(sun_angle)
                shadow_point = (x + shadow_width, y + shadow_height)
                shadow_coords.append(shadow_point)
            return shadow_coords

    def update_enemy(self, player):
        for enemy in self.sprites():
            if enemy.sprite_type == 'enemy':
                enemy.enemy_update(player)
