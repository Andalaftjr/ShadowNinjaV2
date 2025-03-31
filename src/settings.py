import os
import pygame

# Configurações do jogo
WIDTH, HEIGHT = 1000, 600
FPS = 60
TITLE = "Shadow Ninja"

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Caminhos - IMPORTANTE: caminho relativo corrigido
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # Sobe um nível para a raiz do projeto
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
IMG_DIR = os.path.join(ASSETS_DIR, 'images')
SND_DIR = os.path.join(ASSETS_DIR, 'sounds')

# Configurações do player
PLAYER_SPEED = 5
PLAYER_JUMP = 15
GRAVITY = 0.8

# Inicialização do pygame
pygame.init()
pygame.mixer.init()