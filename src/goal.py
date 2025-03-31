import pygame
from settings import *


class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(os.path.join(IMG_DIR, 'goal.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 80))
        self.rect = self.image.get_rect(topleft=(x, y))

        # Efeito de brilho
        self.glow = 0
        self.glow_direction = 1

    def update(self):
        # Animação de brilho
        self.glow += 0.05 * self.glow_direction
        if self.glow > 1 or self.glow < 0:
            self.glow_direction *= -1

        overlay = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, int(50 * self.glow)))
        self.image.blit(overlay, (0, 0), special_flags=pygame.BLEND_ADD)