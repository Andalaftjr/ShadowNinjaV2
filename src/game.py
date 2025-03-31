import pygame
import sys
from settings import *
from level import Level


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        self.current_level = 1
        self.max_level = 3
        self.level = Level(self.current_level)

        # Estados do jogo
        self.game_active = True
        self.game_over = False
        self.victory = False

        # Fonte
        self.font = pygame.font.SysFont('Arial', 36)

    def run(self):
        while True:
            self.handle_events()

            if self.game_active:
                self.update()
                self.draw()
            elif self.game_over:
                self.draw_game_over()
            elif self.victory:
                self.draw_victory()

            pygame.display.flip()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                # Reinicia o jogo
                if not self.game_active and event.key == pygame.K_r:
                    self.reset_game()

    def update(self):
        self.level.update()

        # Verifica se o jogador morreu
        if self.level.player.health <= 0:
            self.game_active = False
            self.game_over = True

        # Verifica se completou o nível
        if self.level.completed:
            if self.current_level < self.max_level:
                self.current_level += 1
                self.level = Level(self.current_level)
            else:
                self.game_active = False
                self.victory = True

    def draw(self):
        self.level.draw(self.screen)

    def draw_game_over(self):
        self.screen.fill(BLACK)
        text = self.font.render("GAME OVER - Press R to Restart", True, RED)
        text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.screen.blit(text, text_rect)

    def draw_victory(self):
        self.screen.fill(BLACK)
        text = self.font.render("VICTORY! - Press R to Play Again", True, GREEN)
        score_text = self.font.render(f"Final Score: {self.level.player.score}", True, WHITE)

        text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 50))
        score_rect = score_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 50))

        self.screen.blit(text, text_rect)
        self.screen.blit(score_text, score_rect)

    def reset_game(self):
        self.current_level = 1
        self.level = Level(self.current_level)
        self.game_active = True
        self.game_over = False
        self.victory = False