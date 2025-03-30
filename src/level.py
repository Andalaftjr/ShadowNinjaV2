# Arquivo: src/level.py
# Gerencia os elementos de cada nível: cenário, jogador e inimigos

import pygame
import random
from settings import WIDTH, HEIGHT, GREEN
from entities import Ninja, Enemy

class Level:
    def __init__(self, level_number):
        self.level_number = level_number
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        # Cria o chão/plataforma
        platform = pygame.sprite.Sprite()
        platform.image = pygame.Surface((WIDTH, 50))
        platform.image.fill(GREEN)
        platform.rect = platform.image.get_rect(topleft=(0, HEIGHT - 50))
        self.all_sprites.add(platform)

        # Cria o jogador
        self.player = Ninja()
        self.all_sprites.add(self.player)

        # Cria inimigos com dificuldade crescente
        enemy_speed = 2 + (level_number - 1)
        quantidade_inimigos = 3 + level_number
        for _ in range(quantidade_inimigos):
            x = random.randint(WIDTH, WIDTH + 300)
            y = random.randint(100, HEIGHT - 100)
            enemy = Enemy(x, y, enemy_speed)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)

    def update(self, keys):
        self.player.update(keys)
        for enemy in self.enemies:
            enemy.update()

    def draw(self, screen):
        self.all_sprites.draw(screen)
