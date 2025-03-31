import pygame
import os
import random
from settings import *


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, is_moving=False):
        super().__init__()

        # Carrega imagem da plataforma
        try:
            img_path = os.path.join(IMG_DIR, 'platform.png')
            self.image = pygame.image.load(img_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width, height))
        except:
            # Fallback se a imagem não existir
            self.image = pygame.Surface((width, height))
            self.image.fill((100, 100, 100))  # Cinza

        self.rect = self.image.get_rect(topleft=(x, y))

        # Configurações para plataformas móveis
        self.is_moving = is_moving
        if is_moving:
            self.move_speed = random.choice([-1, 1])
            self.move_range = random.randint(50, 200)
            self.start_x = x

    def update(self):
        if self.is_moving:
            self.rect.x += self.move_speed
            if (abs(self.rect.x - self.start_x) > self.move_range):
                self.move_speed *= -1