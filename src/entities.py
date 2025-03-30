# Arquivo: src/entities.py
# Define as entidades do jogo: Ninja (jogador) e Enemy (inimigo)

import pygame
from settings import WIDTH, HEIGHT

def load_image(path, size=None):
    """
    Carrega uma imagem e a redimensiona se size for fornecido.
    """
    image = pygame.image.load(path).convert_alpha()
    if size:
        image = pygame.transform.scale(image, size)
    return image

class Ninja(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("assets/images/ninja.png", (50, 50))
        self.rect = self.image.get_rect()
        self.rect.topleft = (50, HEIGHT - 150)
        self.velocity = 5
        self.is_jumping = False
        self.jump_count = 10

    def move(self, dx, dy):
        self.rect.x += dx * self.velocity
        self.rect.y += dy * self.velocity
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.move(-1, 0)
        if keys[pygame.K_RIGHT]:
            self.move(1, 0)
        if not self.is_jumping and keys[pygame.K_SPACE]:
            self.is_jumping = True
        elif self.is_jumping:
            if self.jump_count >= -10:
                neg = 1 if self.jump_count >= 0 else -1
                self.rect.y -= (self.jump_count ** 2) * 0.4 * neg
                self.jump_count -= 1
            else:
                self.is_jumping = False
                self.jump_count = 10

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = load_image("assets/images/enemy.png", (50, 50))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.left = WIDTH
            self.rect.y = (HEIGHT - 100) - (self.rect.y % 150)
