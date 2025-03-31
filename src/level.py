import pygame
import random
from settings import *
from player import Player
from enemy import Enemy
from platform_game import Platform
from coin import Coin
from goal import Goal


class Sons:
    pass


class Level:
    def __init__(self, level_num=1):
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()

        self.player = Player()
        self.all_sprites.add(self.player)

        self.level_num = level_num
        self.completed = False
        self.background = self.load_background()

        self.setup_level()

        Sons
        self.coin_sound = pygame.mixer.Sound(os.path.join(SND_DIR, 'coin.wav'))
        self.hit_sound = pygame.mixer.Sound(os.path.join(SND_DIR, 'hit.wav'))
        self.victory_sound = pygame.mixer.Sound(os.path.join(SND_DIR, 'victory.wav'))

    def load_background(self):
        bg_num = ((self.level_num - 1) % 3) + 1
        bg_path = os.path.join(IMG_DIR, f'background_{bg_num}.png')
        bg = pygame.image.load(bg_path).convert()
        return pygame.transform.scale(bg, (WIDTH, HEIGHT))

    def setup_level(self):
        # Chão principal
        ground = Platform(0, HEIGHT - 50, WIDTH, 50)
        self.platforms.add(ground)
        self.all_sprites.add(ground)

        # Plataformas do nível
        if self.level_num == 1:
            self.create_level_1()
        elif self.level_num == 2:
            self.create_level_2()
        else:
            self.create_level_3()

        # Adiciona moedas aleatórias
        for _ in range(15):
            x = random.randint(50, WIDTH - 50)
            y = random.randint(50, HEIGHT - 150)
            coin = Coin(x, y)
            self.coins.add(coin)
            self.all_sprites.add(coin)

        # Adiciona objetivo
        goal = Goal(WIDTH - 100, HEIGHT - 130)
        self.all_sprites.add(goal)
        self.goal = goal

    def create_level_1(self):
        # Plataformas simples
        platforms = [
            (100, 400, 200, 20, False),
            (400, 300, 200, 20, False),
            (700, 200, 150, 20, True)  # Plataforma móvel
        ]

        for x, y, w, h, m in platforms:
            p = Platform(x, y, w, h, m)
            self.platforms.add(p)
            self.all_sprites.add(p)

        # Inimigos
        enemies = [
            (300, 350, 'random'),
            (500, 250, 'guard'),
            (800, 150, 'chasing')
        ]

        for x, y, t in enemies:
            e = Enemy(x, y, t)
            self.enemies.add(e)
            self.all_sprites.add(e)

    def create_level_2(self):
        # Implemente um layout mais desafiador
        pass

    def create_level_3(self):
        # Implemente o nível mais difícil
        pass

    def update(self):
        self.player.update(self.platforms, self.enemies)
        self.platforms.update()
        self.enemies.update(self.player)
        self.coins.update()
        self.goal.update()

        # Verifica colisão com moedas
        hits = pygame.sprite.spritecollide(self.player, self.coins, True)
        for coin in hits:
            self.player.coins += coin.value
            self.player.score += coin.value * 10
            self.coin_sound.play()

        # Verifica se alcançou o objetivo
        if pygame.sprite.collide_rect(self.player, self.goal):
            self.completed = True
            self.victory_sound.play()

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        self.all_sprites.draw(surface)

        # Desenha UI
        self.draw_ui(surface)

    def draw_ui(self, surface):
        font = pygame.font.SysFont('Arial', 24)

        # Score e moedas
        score_text = font.render(f"Score: {self.player.score}", True, WHITE)
        coins_text = font.render(f"Coins: {self.player.coins}", True, WHITE)
        level_text = font.render(f"Level: {self.level_num}", True, WHITE)

        surface.blit(score_text, (10, 10))
        surface.blit(coins_text, (10, 40))
        surface.blit(level_text, (10, 70))

        # Barra de vida do jogador
        self.player.draw_health(surface)