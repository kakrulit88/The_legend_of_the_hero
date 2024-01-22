import pygame
from Settings import *
import sys


class Menu():
    def __init__(self, player):
        self.screen = pygame.display.get_surface()
        # music
        self.game_sound = pygame.mixer.Sound('data/Sounds/Game/main.ogg')
        self.game_sound.set_volume(0.03)
        self.game_sound.play(loops=-1)

        # fonts
        self.font_size_main = 35
        self.font_size_title = 100
        self.font_title = pygame.font.Font(font, self.font_size_title)
        self.font = pygame.font.Font(font, self.font_size_main)

        # settings
        self.rect1_len = 0
        self.rect2_len = 1280
        self.text_sdvig = 200
        self.player = player

    def main_menu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    return

            preview = pygame.image.load('data/menu/preview.png').convert_alpha()
            self.screen.blit(preview, (0, -350))
            pygame.draw.rect(self.screen, (79, 121, 66), (HEIGHT // 2 - 380, 50, 745, 240))
            text_title_1 = self.font_title.render("The legend", True, (30, 30, 30))
            text_rect_title = text_title_1.get_rect(center=(HEIGHT // 2, 120))
            self.screen.blit(text_title_1, text_rect_title)

            text_title_2 = self.font_title.render("of the hero", True, (30, 30, 30))
            text_rect_title = text_title_2.get_rect(center=(HEIGHT // 2, 230))
            self.screen.blit(text_title_2, text_rect_title)

            text = self.font.render('Нажмите любую кнопку для старта', True, (30, 30, 30))
            text_rect = text.get_rect(center=(HEIGHT // 2, 680))
            self.screen.blit(text, text_rect)
            pygame.display.update()

    def prestory(self):
        self.game_sound.stop()
        text_x = HEIGHT // 2
        text_y = 730
        self.screen.fill('black')
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    return
            self.screen.fill('black')
            for stroka_index in range(len(story_text)):
                text = self.font.render(story_text[stroka_index], True, 'white')
                text_rect = text.get_rect(center=(text_x, text_y + (55 * stroka_index)))
                self.screen.blit(text, text_rect)
            text_y -= 0.18

            pygame.display.update()

            if text_y < -2400:
                return

    def transition(self):
        heart_sound = pygame.mixer.Sound('data/Sounds/Menu/sound1.mp3')
        heart_sound.set_volume(0.1)
        heart_sound.play()

        curcle_radius = 0
        dop_surf = pygame.Surface((HEIGHT, WIDTH), pygame.SRCALPHA)
        dop_surf.fill('black')

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    return
            if curcle_radius > 1100:
                return

            pygame.draw.circle(dop_surf, (255, 255, 255), (HEIGHT // 2, WIDTH // 2), curcle_radius)

            self.screen.blit(dop_surf, (0, 0))
            curcle_radius += 0.2
            pygame.display.update()

    def transition2(self, itog_text, exp):
        if not self.rect1_len > 1000 and not self.rect2_len < 0:
            rect1 = pygame.draw.rect(self.screen, 'black', (0, 0, self.rect1_len, WIDTH))
            rect2 = pygame.draw.rect(self.screen, 'black', (self.rect2_len, 0, HEIGHT, WIDTH))
            self.rect1_len += 3
            self.rect2_len -= 3
            pygame.display.update()
        else:
            end_screen = pygame.image.load('data/menu/end.png').convert_alpha()
            self.screen.blit(end_screen, (0, -350))
            pygame.draw.rect(self.screen, (30, 30, 30), (70, 70, 1140, 580))
            for index in range(len(itog_text)):
                if index == 6:
                    text = self.font.render(f'{itog_text[index]} {exp}', True, 'white')
                    text_rect = text.get_rect(center=(HEIGHT // 2, self.text_sdvig))
                    self.text_sdvig += 50
                    self.screen.blit(text, text_rect)
                else:
                    text = self.font.render(itog_text[index], True, 'white')
                    text_rect = text.get_rect(center=(HEIGHT // 2, self.text_sdvig))
                    self.text_sdvig += 50
                    self.screen.blit(text, text_rect)
                pygame.display.update()

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        return
