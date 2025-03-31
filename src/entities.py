# Arquivo: src/entities.py
import pygame
import random
from settings import WIDTH, HEIGHT


def load_image(path, size=None):
    image = pygame.image.load(path).convert_alpha()
    if size:
        image = pygame.transform.scale(image, size)
    return image


class Ninja(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("assets/images/ninja.png", (50, 50))
        self.rect = self.image.get_rect(center=(100, HEIGHT - 100))
        self.velocity = 5
        self.jumping = False
        self.jump_speed = 15
        self.y_velocity = 0
        self.score = 0
        self.level_complete = False

    def update(self, keys, platforms):
        self.move(keys)
        self.gravity()
        self.check_collision(platforms)

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocity
        if keys[pygame.K_UP] and not self.jumping:
            self.jump()

    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.y_velocity = -self.jump_speed

    def gravity(self):
        if self.jumping:
            self.rect.y += self.y_velocity
            self.y_velocity += 1  # Gravidade
            if self.rect.bottom >= HEIGHT - 50:  # Colisão com o chão
                self.rect.bottom = HEIGHT - 50
                self.jumping = False

    def check_collision(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.rect.bottom > platform.rect.top:
                    self.rect.bottom = platform.rect.top
                    self.jumping = False
                    self.y_velocity = 0


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image("assets/images/coin.png", (30, 30))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        if self.rect.colliderect(player.rect):
            self.kill()
            player.score += 10


class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image("assets/images/goal.png", (50, 100))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, player):
        if self.rect.colliderect(player.rect):
            player.level_complete = True


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 255, 255))  # Branco
        self.rect = self.image.get_rect(topleft=(x, y))
