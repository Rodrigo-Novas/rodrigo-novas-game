"""Menu module."""

import sys
import pygame
from helpers.helper import Helper
from utils.constants import menu_font, FONT_SM, WIDTH, HEIGHT, WHITE, HURT_SOUND, DIE_SOUND
from play.game import play
from utils.bdd import Connection
from utils.buttons import Button


helper = Helper()

conn = Connection()

BG = helper.load_image("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/backgrounds/menu.png")
PLAY = helper.load_image("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/menu/play.png")
QUIT = helper.load_image("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/menu/quit.png")
OPTION = helper.load_image("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/menu/option.png")
SCREEN = pygame.display.set_mode([WIDTH, HEIGHT])
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))


def instructions():
    """
    The `instructions` function displays instructions for a game using the Pygame library and allows the
    user to go back to the main menu.
    """
    while True:
        pygame.display.set_caption("Manual")

        position = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        text_option = menu_font(50).render("Instructions:", 1, WHITE)
        arrows_text = FONT_SM.render("Use arrows to move", 1, WHITE)
        pause_text = FONT_SM.render("Press P to pause", 1, WHITE)
        sound_text = FONT_SM.render("Press S to sound of/on", 1, WHITE)
        up_volume_text = FONT_SM.render("Up volume with B", 1, WHITE)
        down_volume_text = FONT_SM.render("Down volume with N", 1, WHITE)
        space_text = FONT_SM.render("Press SPACE to shoot", 1, WHITE)

        x1 = WIDTH / 2 - text_option.get_width() / 2
        y1 = HEIGHT / 3 - text_option.get_height() / 2

        x2 = WIDTH / 2 - arrows_text.get_width() / 2
        y2 = y1 + text_option.get_height() + 10

        x3 = WIDTH / 2 - pause_text.get_width() / 2
        y3 = y2 + text_option.get_height() + 10

        x4 = WIDTH / 2 - sound_text.get_width() / 2
        y4 = y3 + text_option.get_height() + 10

        x5 = WIDTH / 2 - space_text.get_width() / 2
        y5 = y4 + text_option.get_height() + 10

        x6 = WIDTH / 2 - up_volume_text.get_width() / 2
        y6 = y5 + text_option.get_height() + 10

        x7 = WIDTH / 2 - down_volume_text.get_width() / 2
        y7 = y6 + text_option.get_height() + 10

        SCREEN.blit(text_option, (x1, y1))
        SCREEN.blit(arrows_text, (x2, y2))
        SCREEN.blit(pause_text, (x3, y3))
        SCREEN.blit(sound_text, (x4, y4))
        SCREEN.blit(space_text, (x5, y5))
        SCREEN.blit(up_volume_text, (x6, y6))
        SCREEN.blit(down_volume_text, (x7, y7))

        back = Button(image=OPTION, pos=(450, 70), text_input="← BACK", font=menu_font(30), base_color="#d7fcd4", hovering_color=WHITE)

        back.change_color(position)
        back.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                if back.check_input(position):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.check_input(position):
                    helper.play_sound(HURT_SOUND)
                    main_menu()

        pygame.display.flip()


def text_box():
    """
    The `text_box` function creates a text input box in a Pygame window and allows the user to enter
    text.
    """
    input_text = ""
    while True:
        pygame.display.set_caption("Play")

        position = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        input_rect = pygame.Rect(350, 300, 200, 32)

        back = Button(image=OPTION, pos=(450, 70), text_input="← BACK", font=menu_font(30), base_color="#d7fcd4", hovering_color=WHITE)
        play_btn = Button(image=PLAY, pos=(450, 200), text_input="PLAY", font=menu_font(50), base_color="#d7fcd4", hovering_color=WHITE)

        for button in [play_btn, back]:
            button.change_color(position)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    if input_text != "":
                        helper.play_sound(HURT_SOUND)
                        play(input_text)
                    else:
                        helper.play_sound(DIE_SOUND)
                else:
                    if str(event.unicode) != " " and len(input_text) < 19:
                        input_text += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.check_input(position):
                    if input_text != "":
                        helper.play_sound(HURT_SOUND)
                        play(input_text)
                    else:
                        helper.play_sound(DIE_SOUND)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                if back.check_input(position):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                elif play_btn.check_input(position):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.check_input(position):
                    helper.play_sound(HURT_SOUND)
                    main_menu()

        pygame.draw.rect(SCREEN, WHITE, input_rect, 2)
        text_option = menu_font(10).render(input_text, 1, WHITE)

        SCREEN.blit(text_option, (360, 310))

        pygame.display.flip()


def scores():
    """
    This function displays the top ten scores and corresponding players in a pygame window.
    """
    while True:
        pygame.display.set_caption("Scores")

        i = 35
        column_space = 400
        position = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        back = Button(image=OPTION, pos=(450, 70), text_input="← BACK", font=menu_font(30), base_color="#d7fcd4", hovering_color=WHITE)

        for button in [back]:
            button.change_color(position)
            button.update(SCREEN)

        head1 = menu_font(25).render(f"SCORE", True, WHITE)
        head2 = menu_font(25).render(f"PLAYER", True, WHITE)
        SCREEN.blit(head1, [WIDTH / 5, (100)])
        SCREEN.blit(head2, [WIDTH / 5 + column_space, (100)])
        top_ten = conn.get_top_ten_score()
        if top_ten is not None:
            for player in top_ten:
                column1 = menu_font(15).render("{:>3}".format(player[2]), True, WHITE)
                column2 = menu_font(15).render("{:30}".format(player[1]), True, WHITE)
                SCREEN.blit(column1, [WIDTH / 5, (100) + i])
                SCREEN.blit(column2, [WIDTH / 5 + column_space, (100) + i])
                i += 35

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                if back.check_input(position):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.check_input(position):
                    helper.play_sound(HURT_SOUND)
                    main_menu()

        pygame.display.flip()


def main_menu():
    """
    The `main_menu` function displays a menu screen with buttons for playing the game, accessing
    instructions, viewing scores, and quitting the game.
    """
    while True:
        pygame.display.set_caption("Menu")
        SCREEN.blit(BG, (0, 0))

        position = pygame.mouse.get_pos()
        text_menu = menu_font(50).render("MAIN MENU", 1, "#b68f40")
        menu_rect = text_menu.get_rect(center=(450, 50))

        play_btn = Button(image=PLAY, pos=(450, 130), text_input="PLAY", font=menu_font(50), base_color="#d7fcd4", hovering_color=WHITE)
        quit_btn = Button(image=QUIT, pos=(450, 230), text_input="QUIT", font=menu_font(50), base_color="#d7fcd4", hovering_color=WHITE)
        instruction_btn = Button(
            image=OPTION, pos=(450, 330), text_input="INSTRUCTIONS", font=menu_font(50), base_color="#d7fcd4", hovering_color=WHITE
        )
        scores_btn = Button(
            image=OPTION, pos=(450, 430), text_input="SCORES", font=menu_font(50), base_color="#d7fcd4", hovering_color=WHITE
        )

        SCREEN.blit(text_menu, menu_rect)

        for button in [play_btn, instruction_btn, quit_btn, scores_btn]:
            button.change_color(position)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                if play_btn.check_input(position):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                elif instruction_btn.check_input(position):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                elif scores_btn.check_input(position):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                elif quit_btn.check_input(position):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.check_input(position):
                    helper.play_sound(HURT_SOUND)
                    text_box()
                if instruction_btn.check_input(position):
                    helper.play_sound(HURT_SOUND)
                    instructions()
                if scores_btn.check_input(position):
                    helper.play_sound(HURT_SOUND)
                    scores()
                if quit_btn.check_input(position):
                    helper.play_sound(HURT_SOUND)
                    pygame.quit()
                    sys.exit()
        pygame.display.flip()

