"""Buttons module."""

import pygame


class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        """
        The function initializes an object with properties such as image, position, text input, font, base
        color, and hovering color.

        Args:
          image: The image parameter is the image that will be displayed on the button. It can be an image
        file or a pygame Surface object. If it is set to None, the button will use the text input as the
        image.
          pos: The "pos" parameter is a tuple that represents the x and y coordinates of the button's
        position on the screen.
          text_input: The `text_input` parameter is a string that represents the text that will be displayed
        on the button.
          font: The "font" parameter is the font object that will be used to render the text on the button.
        It should be an instance of the pygame.font.Font class.
          base_color: The base_color parameter is the color of the text when the button is not being hovered
        over.
          hovering_color: The `hovering_color` parameter is the color that the button will change to when
        the mouse is hovering over it.
        """
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.image = pygame.transform.scale(self.image, (self.text_rect.w, self.text_rect.h))
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        """
        The function updates the screen by blitting the image and text onto it.

        Args:
          screen: The "screen" parameter refers to the surface or window where the game or application is
        being displayed. It is typically a pygame Surface object.
        """
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_input(self, position):
        """
        The function checks if a given position is within the boundaries of a rectangle.

        Args:
          position: The `position` parameter is a tuple containing the x and y coordinates of a point.

        Returns:
          a boolean value. If the position is within the range defined by the rectangle's left, right, top,
        and bottom coordinates, then True is returned. Otherwise, False is returned.
        """
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def change_color(self, position):
        """
        The function changes the color of the text based on the position of the mouse cursor.

        Args:
          position: The position parameter is a tuple representing the x and y coordinates of a point on the
        screen.
        """
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
