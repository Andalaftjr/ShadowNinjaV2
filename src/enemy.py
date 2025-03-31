import pygame
import random
from settings import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type='random'):
        super().__init__()
        self.enemy_type = enemy_type

        # Carrega imagem baseada no tipo
        if enemy_type == 'chasing':
            img_path = os.path.join(IMG_DIR, 'enemy_chasing.png')
        elif enemy_type == 'guard':
            img_path = os.path.join(IMG_DIR, 'guard.png')
        else:  # random
            img_path = os.path.join(IMG_DIR, 'enemy_random.png')

        self.image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))

        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = random.choice([-2, -1, 1, 2])
        self.health = 100
        self.damage = 10
        self.patrol_range = random.randint(50, 200)
        self.start_x = x

    def update(self, player=None):
        # Comportamento diferente baseado no tipo
        if self.enemy_type == 'random':
            self.rect.x += self.speed
            if (self.rect.left < max(0, self.start_x - self.patrol_range) or
                    self.rect.right > min(WIDTH, self.start_x + self.patrol_range)):
                self.speed = -self.speed

        elif self.enemy_type == 'chasing' and player:
            if player.rect.x < self.rect.x:
                self.rect.x -= 2
            elif player.rect.x > self.rect.x:
                self.rect.x += 2

        elif self.enemy_type == 'guard':
            # Fica parado até o player chegar perto
            if player and abs(self.rect.x - player.rect.x) < 300:
                if player.rect.x < self.rect.x:
                    self.rect.x -= 1.5
                elif player.rect.x > self.rect.x:
                    self.rect.x += 1.5

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
            return True
        return False