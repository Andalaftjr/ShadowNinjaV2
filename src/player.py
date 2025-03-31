import pygame
import os
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Configurações iniciais
        self.rect = pygame.Rect(100, HEIGHT - 150, 50, 50)
        self.vel_y = 0
        self.on_ground = False
        self.facing_right = True
        self.score = 0
        self.health = 100
        self.coins = 0
        self.invincible = False
        self.invincible_timer = 0

        # Carrega assets com fallback
        self.load_assets()

        # Animação
        self.animation_frames = {}
        self.load_animation()
        self.current_frame = 0
        self.animation_speed = 0.15
        self.image = self.animation_frames["idle"][0]

    def load_assets(self):
        """Carrega imagens e sons com fallback"""
        try:
            # Imagem do jogador
            self.original_image = pygame.image.load(os.path.join(IMG_DIR, 'ninja.png')).convert_alpha()
            self.original_image = pygame.transform.scale(self.original_image, (50, 50))
        except:
            print(f"AVISO: Imagem do jogador não encontrada em {os.path.join(IMG_DIR, 'ninja.png')}")
            self.original_image = pygame.Surface((50, 50))
            self.original_image.fill(BLUE)

        try:
            # Som do pulo
            self.jump_sound = pygame.mixer.Sound(os.path.join(SND_DIR, 'jump.wav'))
        except:
            print(f"AVISO: Som de pulo não encontrado")
            self.jump_sound = None

    def load_animation(self):
        """Sistema básico de animação (pode ser expandido)"""
        self.animation_frames = {
            "idle": [self.original_image],
            "run": [
                pygame.transform.flip(self.original_image, True, False),
                self.original_image
            ],
            "jump": [pygame.transform.rotate(self.original_image, 10)]
        }

    def update(self, platforms, enemies):
        keys = pygame.key.get_pressed()

        # Atualiza estado de invencibilidade
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False

        # Movimento horizontal (corrigido typo PLAYER_SPEED)
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
            self.facing_right = True

        # Pulo
        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()

        # Aplica gravidade
        self.apply_gravity()

        # Limita movimento na tela
        self.constrain_movement()

        # Verifica colisões
        self.check_platform_collision(platforms)
        self.check_enemy_collision(enemies)

        # Atualiza animação
        self.update_animation()

    def jump(self):
        """Lógica do pulo"""
        self.vel_y = -PLAYER_JUMP
        self.on_ground = False
        if self.jump_sound:
            self.jump_sound.play()

    def apply_gravity(self):
        """Aplica gravidade ao jogador"""
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

    def constrain_movement(self):
        """Mantém jogador dentro da tela"""
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def check_platform_collision(self, platforms):
        """Verifica colisão com plataformas"""
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:  # Caindo
                    self.rect.bottom = platform.rect.top
                    self.on_ground = True
                    self.vel_y = 0
                elif self.vel_y < 0:  # Subindo
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0

    def check_enemy_collision(self, enemies):
        """Verifica colisão com inimigos"""
        if self.invincible:
            return

        hits = pygame.sprite.spritecollide(self, enemies, False)
        for enemy in hits:
            if self.vel_y > 0 and self.rect.bottom < enemy.rect.centery:
                # Pulo em cima do inimigo
                enemy.take_damage(50)
                self.vel_y = -PLAYER_JUMP * 0.7
            else:
                # Dano do inimigo
                self.take_damage(10)
                # Knockback
                knockback_dir = -1 if self.rect.x < enemy.rect.x else 1
                self.rect.x += 30 * knockback_dir

    def take_damage(self, amount):
        """Lógica para receber dano"""
        if not self.invincible:
            self.health -= amount
            self.invincible = True
            self.invincible_timer = 60  # 1 segundo de invencibilidade

    def update_animation(self):
        """Atualiza o frame de animação atual"""
        if not self.on_ground:
            self.current_frame = 0
            self.image = self.animation_frames["jump"][0]
        elif abs(self.vel_y) > 0.5:
            self.current_frame = (self.current_frame + self.animation_speed) % len(self.animation_frames["run"])
            self.image = self.animation_frames["run"][int(self.current_frame)]
        else:
            self.current_frame = 0
            self.image = self.animation_frames["idle"][0]

        # Espelha a imagem se estiver virado para esquerda
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

    def draw_health(self, surface):
        """Desenha a barra de vida acima do jogador"""
        health_width = 50 * (self.health / 100)
        outline_rect = pygame.Rect(self.rect.x, self.rect.y - 15, 50, 5)
        health_rect = pygame.Rect(self.rect.x, self.rect.y - 15, health_width, 5)

        pygame.draw.rect(surface, RED, outline_rect)
        pygame.draw.rect(surface, GREEN, health_rect)

        # Efeito de piscar quando invencível
        if self.invincible and self.invincible_timer % 10 < 5:
            pygame.draw.rect(surface, WHITE, outline_rect, 1)