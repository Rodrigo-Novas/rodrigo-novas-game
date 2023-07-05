import pygame

GRID_SIZE = 64

class Helper():
    def __init__(self, sound_on: bool = True) -> None:
        self.__sound_on = sound_on
    
    def load_image(file_path, width=GRID_SIZE, height=GRID_SIZE):
        img = pygame.image.load(file_path)
        img = pygame.transform.scale(img, (width, height))

        return img

    def play_sound(self, sound, loops=0, maxtime=0, fade_ms=0):
        if self.__sound_on:
            sound.play(loops, maxtime, fade_ms)

    def play_music(self):
        if self.__sound_on:
            pygame.mixer.music.play(-1)