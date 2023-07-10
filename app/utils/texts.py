"""Text module."""

from abc import ABC


class Text(ABC):
    def get_font(self) -> str:
        pass

    def get_text(self) -> str:
        pass

    def get_size_font(self) -> str:
        pass


class NormalText(Text):
    def __init__(self, text: str, font: str, size_font: int) -> None:
        self.__text = text
        self.__font = font
        self.__size_font = size_font

    def get_font(self) -> str:
        return self.__font

    def get_text(self) -> str:
        return self.__text

    def get_size_font(self) -> str:
        return self.__size_font

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__text},{self.__font},{self.__size_font})"


class ColoredText(NormalText):
    def __init__(self, text: str, font: str, size_font: int, word_color: tuple, background_color: tuple = None) -> None:
        super().__init__(text, font, size_font)
        self.__word_color = word_color
        self.__background_color = background_color

    def get_word_color(self):
        return self.__word_color

    def get_bk_color(self):
        return self.__background_color

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({super().__text},{super().__font},{super().__size_font},{self.__word_color},{self.__background_color})"
