"""Constants module."""

import pygame

# screen resolution
RES = (1000, 700)

# Controls
LEFT = pygame.K_LEFT
RIGHT = pygame.K_RIGHT
JUMP = pygame.K_SPACE

# Window settings
TITLE = "The Quest for Ancient Fire"
WIDTH = 960
HEIGHT = 500
FPS = 60

# Sounds
pygame.mixer.pre_init()  # Me salta la excepcion pygame.error: mixer not initialized
pygame.init()


JUMP_SOUND = pygame.mixer.Sound("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/sounds/jump.wav")
EARNED_SOUND = pygame.mixer.Sound("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/sounds/earned.wav")
HURT_SOUND = pygame.mixer.Sound("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/sounds/hurt.ogg")
DIE_SOUND = pygame.mixer.Sound("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/sounds/death.wav")
LEVELUP_SOUND = pygame.mixer.Sound("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/sounds/level_up.wav")
GAMEOVER_SOUND = pygame.mixer.Sound("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/sounds/game_over.wav")
BULLET_SOUND = pygame.mixer.Sound("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/sounds/bullet.mp3")
CURE_SOUND = pygame.mixer.Sound("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/sounds/cure.wav")
EARNED_PLUS_SOUND = pygame.mixer.Sound("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/sounds/earned_plus.wav")

# Controls
LEFT = pygame.K_LEFT
RIGHT = pygame.K_RIGHT
JUMP = pygame.K_UP
PAUSE_K = ord("p")
SHOOT_K = pygame.K_SPACE
UP_VOLUME = pygame.K_n
DOWN_VOLUME = pygame.K_b
SOUND_OF = pygame.K_s
RESTART_K = pygame.K_r

# Levels
levels = [
    "/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/app/levels/level-1.json",
    "/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/app/levels/level-2.json",
    "/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/app/levels/level-3.json",
]

# Colors
TRANSPARENT = (0, 0, 0, 0)
DARK_BLUE = (16, 86, 103)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0, 255)
BLACK = (0, 0, 0)

# Fonts
FONT_SM = pygame.font.Font("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/fonts/minya_nouvelle_bd.ttf", 32)
FONT_MD = pygame.font.Font("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/fonts/minya_nouvelle_bd.ttf", 64)
FONT_LG = pygame.font.Font("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/fonts/thats_super.ttf", 72)


def menu_font(size):
    font_menu = pygame.font.Font("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/fonts/menu.ttf", size)
    return font_menu


BULLETS_LIMIT = 5
BULLETS_COLOR = BLACK
GRID_SIZE = 50
