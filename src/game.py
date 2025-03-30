# Arquivo: src/game.py
# Gerencia o loop principal, eventos e controle dos níveis do jogo Shadow Ninja

import pygame
from settings import WIDTH, HEIGHT, FPS, BLACK, TOTAL_LEVELS
from level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Shadow Ninja")
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_level_number = 1
        self.level = Level(self.current_level_number)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        keys = pygame.key.get_pressed()
        self.level.update(keys)
        # Se o jogador atingir o lado direito da tela, avança para o próximo nível
        if self.level.player.rect.left >= WIDTH - 50:
            self.current_level_number += 1
            if self.current_level_number > TOTAL_LEVELS:
                print("Parabéns! Você completou o jogo Shadow Ninja!")
                self.running = False
            else:
                self.level = Level(self.current_level_number)

    def draw(self):
        self.screen.fill(BLACK)
        self.level.draw(self.screen)
        # Desenha o nível atual na tela
        font = pygame.font.SysFont("arial", 24)
        level_text = font.render(f"Nível: {self.current_level_number}/{TOTAL_LEVELS}", True, (255, 255, 255))
        self.screen.blit(level_text, (10, 10))
        pygame.display.update()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()
        pygame.quit()
