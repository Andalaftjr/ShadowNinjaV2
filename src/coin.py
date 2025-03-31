import pygame
import random
from settings import *


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(os.path.join(IMG_DIR, 'coin.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(center=(x, y))
        self.value = random.randint(1, 5)

        # Animação
        self.original_image = self.image
        self.angle = 0

    def update(self):
        # Rotação da moeda
        self.angle = (self.angle + 5) % 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)