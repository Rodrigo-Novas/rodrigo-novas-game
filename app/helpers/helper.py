"""Helper module."""

import pygame
from utils.constants import GRID_SIZE


# The Helper class has a constructor that takes a boolean parameter to determine if sound is on or
# off.
class Helper:
    def __init__(self, sound_on: bool = True) -> None:
        self.__sound_on = sound_on

    @staticmethod
    def load_image(file_path, width=GRID_SIZE, height=GRID_SIZE):
        """
        The `load_image` function loads an image from a file path and resizes it to a specified width and
        height using the pygame library in Python.

        Args:
            file_path: The file path is the location of the image file that you want to load. It should be a
        string that specifies the path to the file, including the file name and extension.
            width: The width parameter specifies the desired width of the loaded image. By default, it is set
        to the value of the GRID_SIZE constant.
            height: The `height` parameter is the desired height of the loaded image. By default, it is set to
        `GRID_SIZE`, which suggests that `GRID_SIZE` is a constant representing the desired height and width
        of the image.

        Returns:
            the loaded and scaled image.
        """
        img = pygame.image.load(file_path)
        img = pygame.transform.scale(img, (width, height))

        return img

    def play_sound(self, sound, loops=0, maxtime=0, fade_ms=0):
        """
        The function `play_sound` plays a given sound with optional parameters for loops, maximum time, and
        fade duration.

        Args:
          sound: The sound object that you want to play. This can be an instance of the pygame.mixer.Sound
        class.
          loops: The "loops" parameter determines how many times the sound will be played. By default, it is
        set to 0, which means the sound will only play once. If you set it to a positive integer, the sound
        will play that many times. If you set it to -1, the. Defaults to 0
          maxtime: The `maxtime` parameter is used to specify the maximum duration of the sound in
        milliseconds. If the sound exceeds this duration, it will be truncated. If `maxtime` is set to 0
        (default), the sound will play in its entirety. Defaults to 0
          fade_ms: The fade_ms parameter is the duration in milliseconds over which the sound will fade in
        or out. If fade_ms is set to a positive value, the sound will fade in over the specified duration
        when it starts playing, and fade out over the same duration when it stops playing. If fade_ms is
        set. Defaults to 0
        """
        if self.__sound_on:
            sound.play(loops, maxtime, fade_ms)

    def play_music(self):
        """
        The function `play_music` plays music continuously if the sound is turned on.
        """
        if self.__sound_on:
            pygame.mixer.music.play(-1)
