import pygame
from Settings import *


class Dialogs():
    def __init__(self, surface):
        self.surface = surface

        # fonts
        self.font = pygame.font.Font(font, font_size)

        # timer
        self.is_timer = True

        # sounds
        self.diaolg_sound = pygame.mixer.Sound('data/Sounds/Game/Voice2.wav')
        self.diaolg_sound.set_volume(0.02)

    def start_dialog(self):
        for dialog in start_dialog:
            self.draw_dialog(self.surface, dialog[0], dialog[1])

    def draw_dialog(self, surface, icon, text):
        current_text = ''
        text_index = 0
        current_time = pygame.time.get_ticks()
        self.is_timer = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    return
            # rects
            rect1 = pygame.draw.rect(surface, 'black', (0, 0, HEIGHT, 180))
            rect2 = pygame.draw.rect(surface, 'black', (0, 520, HEIGHT, 200))

            dialog_image = pygame.image.load('data/menu/dialog.png').convert_alpha()
            dialog_image_rect = dialog_image.get_rect(topleft=(0, 488))
            surface.blit(dialog_image, dialog_image_rect)

            icon_image = pygame.image.load(icon).convert_alpha()
            icon_image_rect = icon_image.get_rect(topleft=(24, 550))
            surface.blit(icon_image, icon_image_rect)

            # text
            if len(current_text) >= len(text):
                surface.blit(text_img, text_rect)
                text_index = 0
            else:
                if self.is_timer is True:
                    current_time = pygame.time.get_ticks()
                    self.is_timer = False
                    current_text += text[text_index]
                    self.diaolg_sound.play()
                    text_index += 1

                text_img = self.font.render(current_text, True, 'black')
                text_rect = text_img.get_rect(topleft=(210, 560))
                surface.blit(text_img, text_rect)

            self.timer(current_time, 70)
            pygame.display.update()

    def timer(self, time, period):
        if time:
            current_time = pygame.time.get_ticks()
            if current_time - time > period:
                self.is_timer = True
