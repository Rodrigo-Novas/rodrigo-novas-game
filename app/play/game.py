"""Game module."""

import json
import sys
from typing import Any
import pygame
from helpers.helper import Helper
from utils.colors import RandomColour
from utils.bdd import Connection
from utils.buttons import Button
from utils.constants import (
    JUMP_SOUND,
    DIE_SOUND,
    HURT_SOUND,
    LEVELUP_SOUND,
    EARNED_SOUND,
    EARNED_PLUS_SOUND,
    CURE_SOUND,
    GAMEOVER_SOUND,
    FPS,
    WIDTH,
    HEIGHT,
    WHITE,
    TITLE,
    levels,
    FONT_MD,
    FONT_SM,
    DARK_BLUE,
    JUMP,
    LEFT,
    RIGHT,
    TRANSPARENT,
    PAUSE_K,
    SHOOT_K,
    GRID_SIZE,
    GREEN,
    DOWN_VOLUME,
    UP_VOLUME,
    SOUND_OF,
    RESTART_K,
    menu_font,
)

import pygame


RANDOM_COL = RandomColour()

con = Connection()

helper = Helper()

# Images

hero_walk1 = Helper.load_image("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/warrior/warrior_walk_1.png")
hero_walk2 = Helper.load_image("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/warrior/warrior_walk_2.png")
hero_jump = Helper.load_image("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/warrior/jump_warrior.png")
hero_idle = Helper.load_image("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/warrior/warrior_idle.png")
hero_images = {"run": [hero_walk1, hero_walk2], "jump": hero_jump, "idle": hero_idle}

block_images = {
    "TL": Helper.load_image("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/tiles/top_left.png"),
    "M": Helper.load_image("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/tiles/top_middle.png"),
    "TR": Helper.load_image("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/tiles/top_right.png"),
    "ER": Helper.load_image("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/tiles/end_right.png"),
    "EL": Helper.load_image("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/tiles/end_left.png"),
    "TP": Helper.load_image("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/tiles/top.png"),
    "CN": Helper.load_image("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/tiles/center.png"),
    "LF": Helper.load_image("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/tiles/lone_float.png"),
    "SP": Helper.load_image("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/tiles/special.png"),
}

heart_img = Helper.load_image("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/items/bandaid.png")
oneup_img = Helper.load_image("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/items/first_aid.png")
diamond_img = Helper.load_image("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/jewell/jewell.png")
diamond_black_img = Helper.load_image("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/jewell/diamond.png")
flag_img = Helper.load_image("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/items/flag.png")
flagpole_img = Helper.load_image("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/items/flagpole.png")
flame_img = Helper.load_image("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/flame/fuego.png")
manual_img = Helper.load_image("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/manual/manual.png")


up_volume_img = Helper.load_image("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/music/down.png")
down_volume_img = Helper.load_image("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/music/up.png")
sound_of_img = Helper.load_image("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/music/volume.png")
pause_img = Helper.load_image("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/music/pause.png")


monster_img1 = Helper.load_image("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/monster/monster-1.png")
monster_img2 = Helper.load_image("/Users/rodrinovas/Desktop/proyecto-integrador/game-p2/assets/monster/monster-2.png")
monster_images = [monster_img1, monster_img2]


class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, image, width=None, height=None):
        super().__init__()

        self.image = image
        self.image.set_colorkey(GREEN)  # SACO FONDO VERDE SI LO TIENE

        self.rect = self.image.get_rect()  # Para posicionar nuestro sprite
        self.rect.x = x
        self.rect.y = y

        self.vy = 0
        self.vx = 0

        self.width = width
        self.height = height

    def apply_gravity(self, level):
        self.vy += level.gravity
        self.vy = min(self.vy, level.terminal_velocity)


class Block(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)


class Flame(Entity):
    def __init__(self, image, facing_right, flame_state="ready") -> Any:
        super().__init__(0, 0, image, 200, 200)
        self.image_flame = pygame.transform.flip(image, 1, 0)
        self.image_flame_left = pygame.transform.flip(image, 1, 0)
        self.facing_right = facing_right
        self.flame_state = flame_state

    def respawn(self, level):
        self.rect.x = level.start_x
        self.rect.y = level.start_y
        self.facing_right = True

    def shoot_flame(self, window, x, y):
        self.flame_state = "fire"
        window.blit(flame_img, (x, y))
        self.rect.x = x
        self.rect.y = y
        pygame.display.flip()

    def process_enemies_flame(self, enemies):
        hit_list = pygame.sprite.spritecollide(self, enemies, True)
        if len(hit_list) > 0:
            helper.play_sound(HURT_SOUND)
            self.rect.x = WIDTH + 100

    def update(self, level):
        self.process_enemies_flame(level.enemies)


class Warrior(Entity):
    def __init__(self, images):
        super().__init__(0, 0, images["idle"], 200, 200)

        self.image_idle_left = images["idle"]
        self.image_idle_right = pygame.transform.flip(images["idle"], 1, 0)
        self.images_run_left = images["run"]
        self.images_run_right = [pygame.transform.flip(img, 1, 0) for img in self.images_run_left]
        self.image_jump_right = pygame.transform.flip(images["jump"], 1, 0)
        self.image_jump_left = images["jump"]

        self.running_images = self.images_run_right
        self.image_index = 0
        self.steps = 0

        self.speed = 5
        self.jump_power = 20

        self.vx = 0
        self.vy = 0
        self.facing_right = True
        self.on_ground = True

        self.score = 0
        self.lives = 3
        self.hearts = 3
        self.max_hearts = 3
        self.invincibility = 0

    def move_left(self):
        self.vx = -self.speed
        self.facing_right = False

    def move_right(self):
        self.vx = self.speed
        self.facing_right = True

    def stop(self):
        self.vx = 0

    def jump(self, block):
        self.rect.y += 1

        hit_list = pygame.sprite.spritecollide(self, block, False)

        if len(hit_list) > 0:
            self.vy = -1 * self.jump_power
            helper.play_sound(JUMP_SOUND)

        self.rect.y -= 1

    def check_world_boundaries(self, level):
        if self.rect.left < 0:  # El valor int de la coordenada X del lado izquierdo del rectángulo
            self.rect.left = 0
        elif self.rect.right > level.width:
            self.rect.right = level.width

    def move_and_process_blocks(self, blocks):
        self.rect.x += self.vx
        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        for block in hit_list:
            if self.vx > 0:
                self.rect.right = block.rect.left
                self.vx = 0
            elif self.vx < 0:
                self.rect.left = block.rect.right
                self.vx = 0

        self.on_ground = False
        self.rect.y += self.vy + 1
        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        for block in hit_list:
            if self.vy > 0:
                self.rect.bottom = block.rect.top
                self.vy = 0
                self.on_ground = True
            elif self.vy < 0:
                self.rect.top = block.rect.bottom
                self.vy = 0

    def process_enemies(self, enemies):
        hit_list = pygame.sprite.spritecollide(self, enemies, False)
        if len(hit_list) > 0 and self.invincibility == 0:
            helper.play_sound(HURT_SOUND)
            self.hearts -= 1
            self.invincibility = int(0.75 * FPS)

    def process_band_aid(self, band_aid):
        hit_list = pygame.sprite.spritecollide(self, band_aid, True)

        if len(hit_list) > 0 and self.hearts < 5:
            helper.play_sound(CURE_SOUND)
            self.hearts += 1

    def process_diamond(self, diamonds):
        hit_list = pygame.sprite.spritecollide(self, diamonds, True)

        if len(hit_list) > 0:
            helper.play_sound(EARNED_SOUND)
            self.score += 1

    def process_diamond_black(self, diamonds_black):
        hit_list = pygame.sprite.spritecollide(self, diamonds_black, True)

        if len(hit_list) > 0:
            helper.play_sound(EARNED_PLUS_SOUND)
            self.score += 10

    def check_flag(self, level):
        hit_list = pygame.sprite.spritecollide(self, level.flag, False)

        if len(hit_list) > 0:
            level.completed = True
            helper.play_sound(LEVELUP_SOUND)

    def set_image(self):
        if self.on_ground:
            if self.vx != 0:
                if self.facing_right:
                    self.running_images = self.images_run_right
                else:
                    self.running_images = self.images_run_left

                self.steps = (self.steps + 1) % self.speed

                if self.steps == 0:
                    self.image_index = (self.image_index + 1) % len(self.running_images)
                    self.image = self.running_images[self.image_index]
            else:
                if self.facing_right:
                    self.image = self.image_idle_right
                else:
                    self.image = self.image_idle_left
        else:
            if self.facing_right:
                self.image = self.image_jump_right
            else:
                self.image = self.image_jump_left

    def die(self):
        self.lives -= 1

        if self.lives > 0:
            helper.play_sound(DIE_SOUND)
        else:
            helper.play_sound(GAMEOVER_SOUND)

    def respawn(self, level):
        self.rect.x = level.start_x
        self.rect.y = level.start_y
        self.hearts = self.max_hearts
        self.invincibility = 0
        self.facing_right = True

    def not_respawn(self, level):
        self.rect.x = level.start_x
        self.rect.y = level.start_y
        self.hearts = self.max_hearts
        self.invincibility = 0
        self.facing_right = True

    def update(self, level):
        self.process_enemies(level.enemies)
        self.process_band_aid(level.band_aid)
        self.process_diamond(level.diamonds)
        self.process_diamond_black(level.diamonds_black)
        self.apply_gravity(level)
        self.move_and_process_blocks(level.blocks)
        self.check_world_boundaries(level)
        self.set_image()

        if self.hearts > 0:
            self.check_flag(level)

            if self.invincibility > 0:
                self.invincibility -= 1
        else:
            self.die()


class Enemy(Entity):
    def __init__(self, x, y, images, hearts=1):
        super().__init__(x, y, images[0], GRID_SIZE, GRID_SIZE)

        self.images_left = images
        self.images_right = [pygame.transform.flip(img, 1, 0) for img in images]
        self.current_images = self.images_left
        self.image_index = 0
        self.steps = 0
        self.hearts = hearts

    def reverse(self):
        self.vx *= -1

        if self.vx < 0:
            self.current_images = self.images_left
        else:
            self.current_images = self.images_right

        self.image = self.current_images[self.image_index]

    def check_world_boundaries(self, level):
        if self.rect.left < 0:
            self.rect.left = 0
            self.reverse()
        elif self.rect.right > level.width:
            self.rect.right = level.width
            self.reverse()

    def move_and_process_blocks(self, blocks):
        self.rect.x += self.vx
        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        for block in hit_list:
            if self.vx > 0:
                self.rect.right = block.rect.left
                self.reverse()
            elif self.vx < 0:
                self.rect.left = block.rect.right
                self.reverse()

        self.rect.y += self.vy
        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        for block in hit_list:
            if self.vy > 0:
                self.rect.bottom = block.rect.top
                self.vy = 0
            elif self.vy < 0:
                self.rect.top = block.rect.bottom
                self.vy = 0

    def set_images(self):
        if self.steps == 0:
            self.image = self.current_images[self.image_index]
            self.image_index = (self.image_index + 1) % len(self.current_images)

        self.steps = (self.steps + 1) % 20  # El 20% parece funcionar bien


    def update(self, level):
        self.apply_gravity(level)
        self.move_and_process_blocks(level.blocks)
        self.check_world_boundaries(level)
        self.set_images()

    def reset(self):
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.vx = self.start_vx
        self.vy = self.start_vy
        self.current_images = self.images_left
        self.image = self.current_images[0]
        self.steps = 0


class Monster(Enemy):
    def __init__(self, x, y, images):
        super().__init__(x, y, images)

        self.start_x = x
        self.start_y = y
        self.start_vx = -2
        self.start_vy = 0

        self.vx = self.start_vx
        self.vy = self.start_vy

    def move_and_process_blocks(self, blocks):
        reverse = False

        self.rect.x += self.vx
        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        for block in hit_list:
            if self.vx > 0:
                self.rect.right = block.rect.left
                self.reverse()
            elif self.vx < 0:
                self.rect.left = block.rect.right
                self.reverse()

        self.rect.y += self.vy
        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        reverse = True

        for block in hit_list:
            if self.vy >= 0:
                self.rect.bottom = block.rect.top
                self.vy = 0

                if self.vx > 0 and self.rect.right <= block.rect.right:
                    reverse = False

                elif self.vx < 0 and self.rect.left >= block.rect.left:
                    reverse = False

        if reverse:
            self.reverse()


class OneUp(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)


class Diamond(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)


class DiamondBlack(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)


class Heart(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)


class Flag(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)


class Level:
    def __init__(self, file_path):
        self.starting_blocks = []
        self.starting_enemies = []
        self.starting_powerups = []
        self.starting_flag = []
        self.starting_flame = []
        self.starting_diamonds = []
        self.starting_diamond_black = []
        self.starting_buttons = []

        self.blocks = pygame.sprite.Group()  # esto es una lista para almacenar las instancias de mis entidades
        self.enemies = pygame.sprite.Group()
        self.band_aid = pygame.sprite.Group()
        self.diamonds = pygame.sprite.Group()
        self.diamonds_black = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.flag = pygame.sprite.Group()

        self.active_sprites = pygame.sprite.Group()
        self.inactive_sprites = pygame.sprite.Group()

        self.x_grid = GRID_SIZE * 8

        with open(file_path, "r") as f:
            data = f.read()

        map_data = json.loads(data)

        self.width = map_data["width"] * GRID_SIZE
        self.height = map_data["height"] * GRID_SIZE

        self.start_x = map_data["start"][0] * GRID_SIZE
        self.start_y = map_data["start"][1] * GRID_SIZE

        for item in map_data["blocks"]:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            img = block_images[item[2]]
            self.starting_blocks.append(Block(x, y, img))

        for item in map_data["monsters"]:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_enemies.append(Monster(x, y, monster_images))

        for item in map_data["oneups"]:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_powerups.append(OneUp(x, y, oneup_img))

        for item in map_data["diamonds"]:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_diamonds.append(Diamond(x, y, diamond_img))

        for item in map_data["diamonds_black"]:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_diamond_black.append(DiamondBlack(x, y, diamond_black_img))

        for item in map_data["hearts"]:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_powerups.append(Heart(x, y, heart_img))

        for i, item in enumerate(map_data["flag"]):
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE

            if i == 0:
                img = flag_img
            else:
                img = flagpole_img

            self.starting_flag.append(Flag(x, y, img))

        # mis distintas capas del juego
        self.background_layer = pygame.Surface(
            [self.width, self.height], pygame.SRCALPHA, 32
        )  # depth representa el numero de bits a usar para un color
        self.scenery_layer = pygame.Surface([self.width, self.height], pygame.SRCALPHA, 32)
        self.inactive_layer = pygame.Surface([self.width, self.height], pygame.SRCALPHA, 32)
        self.active_layer = pygame.Surface([self.width, self.height], pygame.SRCALPHA, 32)

        if map_data["background-color"] != "":
            self.background_layer.fill(map_data["background-color"])

        if map_data["background-img"] != "":
            background_img = pygame.image.load(map_data["background-img"]).convert_alpha()

            if map_data["background-fill-y"]:
                h = background_img.get_height()
                w = int(background_img.get_width() * HEIGHT / h)
                background_img = pygame.transform.scale(background_img, (w, HEIGHT))

            if "bottom" in map_data["background-position"]:
                start_y = self.height - background_img.get_height()

            if map_data["background-repeat-x"]:
                for x in range(0, self.width, background_img.get_width()):
                    self.background_layer.blit(background_img, [x, start_y])  # repito la imagen por todo el width
            else:
                self.background_layer.blit(background_img, [0, start_y])

        if map_data["scenery-img"] != "":
            scenery_img = pygame.image.load(map_data["scenery-img"]).convert_alpha()

            if map_data["scenery-fill-y"]:
                h = scenery_img.get_height()
                w = int(scenery_img.get_width() * HEIGHT / h)
                scenery_img = pygame.transform.scale(scenery_img, (w, HEIGHT))

            if "bottom" in map_data["scenery-position"]:
                start_y = self.height - scenery_img.get_height()

            if map_data["scenery-repeat-x"]:
                for x in range(0, self.width, scenery_img.get_width()):
                    self.scenery_layer.blit(scenery_img, [x, start_y])
            else:
                self.scenery_layer.blit(scenery_img, [0, start_y])

        pygame.mixer.music.load(map_data["music"])

        self.gravity = map_data["gravity"]
        self.terminal_velocity = map_data["terminal-velocity"]

        self.completed = False

        self.blocks.add(self.starting_blocks)
        self.enemies.add(self.starting_enemies)
        self.band_aid.add(self.starting_powerups)
        self.diamonds.add(self.starting_diamonds)
        self.diamonds_black.add(self.starting_diamond_black)
        self.powerups.add(self.starting_powerups)
        self.flag.add(self.starting_flag)
        self.inactive_sprites.add(self.blocks, self.flag)

        for s in self.active_sprites:
            s.image.convert()

        for s in self.inactive_sprites:
            s.image.convert()

        self.inactive_sprites.draw(self.inactive_layer)  # aca creo mis sprites

        self.background_layer.convert()
        self.scenery_layer.convert()
        self.inactive_layer.convert()
        self.active_layer.convert()

    def reset(self):
        self.enemies.add(self.starting_enemies)
        self.powerups.add(self.starting_powerups)
        self.diamonds.add(self.starting_diamonds)
        self.diamonds_black.add(self.starting_diamonds)

        self.active_sprites.add(self.enemies, self.powerups, self.diamonds, self.diamonds_black)

        for e in self.enemies:
            e.reset()


class Pause:
    def __init__(self):
        self.paused = pygame.mixer.music.get_busy()

    def toggle(self):
        if self.paused:
            pygame.mixer.music.pause()
        if not self.paused:
            pygame.mixer.music.play(-1)
        self.paused = not self.paused


class Volume:
    def __init__(self):
        self.count = pygame.mixer.music.get_volume()

    def toggle(self, up=False):
        if up:
            self.count += 0.2
            if self.count < 1:
                pygame.mixer.music.set_volume(self.count)
        else:
            self.count -= 0.2
            if self.count > 0:
                pygame.mixer.music.set_volume(self.count)


class Game:
    SPLASH = 0
    START = 1
    PLAYING = 2
    PAUSED = 3
    LEVEL_COMPLETED = 4
    GAME_OVER = 5
    VICTORY = 6
    UNPAUSED = 7
    MANUAL = 8

    def __init__(self, user):
        self.window = pygame.display.set_mode([WIDTH, HEIGHT])
        self.user = user
        self.clock = pygame.time.Clock()
        self.done = False
        self.flag_insert = True

        self.reset()

    def paused_game(self):
        self.clock = pygame.time.Clock()
        self.stage = Game.PAUSED

    def manual_game(self):
        self.clock = pygame.time.Clock()
        self.stage = Game.MANUAL

    def unpaused_game(self):
        self.stage = Game.PLAYING

    def start(self):
        self.level = Level(levels[self.current_level])
        self.qty_level = 1
        self.level.reset()
        self.hero.respawn(self.level)
        self.flame.respawn(self.level)

    def advance(self):
        self.current_level += 1
        self.start()
        self.stage = Game.START

    def reset(self):
        self.hero = Warrior(hero_images)
        self.flame = Flame(flame_img, self.hero.facing_right)
        self.current_level = 0
        self.qty_level = 1
        self.start()
        self.stage = Game.SPLASH
        self.flag_insert = True

    def display_splash(self, surface):
        line1 = FONT_MD.render(TITLE, 1, DARK_BLUE)
        line2 = FONT_SM.render("Press any key to start.", 1, WHITE)
        data = con.get_last_user_order_by_score(self.user)
        if data is not None:
            line3 = FONT_MD.render(str(data[1]), 1, DARK_BLUE)
            line4 = FONT_MD.render(str(data[2]), 1, DARK_BLUE)

        x1 = WIDTH / 2 - line1.get_width() / 2
        y1 = HEIGHT / 3 - line1.get_height() / 2

        x2 = WIDTH / 2 - line2.get_width() / 2
        y2 = y1 + line1.get_height() + 16
        if data is not None:
            x3 = WIDTH / 2 - line3.get_width() / 2
            y3 = y2 + line2.get_height() + 16
            x4 = WIDTH / 2 - line4.get_width() / 2
            y4 = y3 + line3.get_height() + 16

        surface.blit(line1, (x1, y1))
        surface.blit(line2, (x2, y2))
        if data is not None:
            surface.blit(line3, (x3, y3))
            surface.blit(line4, (x4, y4))

    def display_paused(self, surface):
        line1 = FONT_MD.render(TITLE, 1, DARK_BLUE)
        line2 = FONT_SM.render("Paused. Press p key to reanude.", 1, WHITE)

        x1 = WIDTH / 2 - line1.get_width() / 2
        y1 = HEIGHT / 3 - line1.get_height() / 2

        x2 = WIDTH / 2 - line2.get_width() / 2
        y2 = y1 + line1.get_height() + 16

        surface.blit(line1, (x1, y1))
        surface.blit(line2, (x2, y2))

    def display_message(self, surface, primary_text, secondary_text):
        line1 = FONT_MD.render(primary_text, 1, WHITE)
        line2 = FONT_SM.render(secondary_text, 1, WHITE)

        x1 = WIDTH / 2 - line1.get_width() / 2
        y1 = HEIGHT / 3 - line1.get_height() / 2

        x2 = WIDTH / 2 - line2.get_width() / 2
        y2 = y1 + line1.get_height() + 16

        surface.blit(line1, (x1, y1))
        surface.blit(line2, (x2, y2))

    def display_stats(self, surface):
        position = pygame.mouse.get_pos()
        hearts_text = FONT_SM.render("Hearts: " + str(self.hero.hearts), 1, WHITE)
        lives_text = FONT_SM.render("Lives: " + str(self.hero.lives), 1, WHITE)
        score_text = FONT_SM.render("Score: " + str(self.hero.score), 1, WHITE)
        level_text = FONT_SM.render("Level: " + str(self.current_level), 1, WHITE)
        self.sound_btn = Button(
            image=sound_of_img, pos=(40, 100), text_input=" ", font=menu_font(20), base_color="#d7fcd4", hovering_color=WHITE
        )

        self.up_btn = Button(
            image=up_volume_img, pos=(40, 150), text_input=" ", font=menu_font(20), base_color="#d7fcd4", hovering_color=WHITE
        )
        self.down_btn = Button(
            image=down_volume_img, pos=(40, 200), text_input=" ", font=menu_font(20), base_color="#d7fcd4", hovering_color=WHITE
        )

        self.pause_btn = Button(
            image=pause_img, pos=(40, 250), text_input=" ", font=menu_font(20), base_color="#d7fcd4", hovering_color=WHITE
        )

        surface.blit(score_text, (WIDTH - score_text.get_width() - 32, 32))
        surface.blit(manual_img, (10, 10))
        surface.blit(hearts_text, (WIDTH - score_text.get_width() - 200, 32))
        surface.blit(lives_text, (WIDTH - score_text.get_width() - 200, 64))
        surface.blit(level_text, (WIDTH - score_text.get_width() - 200, 96))
        for button in [self.sound_btn, self.pause_btn, self.up_btn, self.down_btn]:
            button.change_color(position)
            button.update(self.window)

    def display_manual(self, surface):
        title_text = FONT_MD.render(TITLE, 1, DARK_BLUE)
        instructions_text = FONT_SM.render("INSTRUCTIONS", 1, RANDOM_COL.return_colour())
        arrows_text = FONT_SM.render("Use arrows to move", 1, WHITE)
        pause_text = FONT_SM.render("Press P to pause", 1, WHITE)
        sound_text = FONT_SM.render("Press S to sound of/on", 1, WHITE)
        up_volume_text = FONT_SM.render("Up volume with B", 1, WHITE)
        down_volume_text = FONT_SM.render("Down volume with N", 1, WHITE)
        space_text = FONT_SM.render("Press SPACE to shoot", 1, WHITE)

        x1 = WIDTH / 2 - title_text.get_width() / 2
        y1 = HEIGHT / 3 - title_text.get_height() / 2

        x2 = WIDTH / 2 - instructions_text.get_width() / 2
        y2 = y1 + title_text.get_height() + 10

        x3 = WIDTH / 2 - arrows_text.get_width() / 2
        y3 = y2 + instructions_text.get_height() + 10

        x4 = WIDTH / 2 - pause_text.get_width() / 2
        y4 = y3 + instructions_text.get_height() + 10

        x5 = WIDTH / 2 - sound_text.get_width() / 2
        y5 = y4 + instructions_text.get_height() + 10

        x6 = WIDTH / 2 - space_text.get_width() / 2
        y6 = y5 + instructions_text.get_height() + 10

        x7 = WIDTH / 2 - up_volume_text.get_width() / 2
        y7 = y6 + instructions_text.get_height() + 10

        x8 = WIDTH / 2 - down_volume_text.get_width() / 2
        y8 = y7 + instructions_text.get_height() + 10

        surface.blit(title_text, (x1, y1))
        surface.blit(instructions_text, (x2, y2))
        surface.blit(arrows_text, (x3, y3))
        surface.blit(pause_text, (x4, y4))
        surface.blit(sound_text, (x5, y5))
        surface.blit(space_text, (x6, y6))
        surface.blit(up_volume_text, (x7, y7))
        surface.blit(down_volume_text, (x8, y8))

    def process_events(self):
        self.pause_music = Pause()
        self.volume = Volume()
        position = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            elif event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if manual_img.get_rect().collidepoint(x, y):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                elif self.down_btn.check_input(position):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                elif self.up_btn.check_input(position):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                elif self.sound_btn.check_input(position):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                elif self.pause_btn.check_input(position):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if self.stage == Game.PLAYING:
                    if manual_img.get_rect().collidepoint(x, y):
                        self.manual_game()
                    if self.up_btn.check_input(position):
                        self.volume.toggle()
                    if self.down_btn.check_input(position):
                        self.volume.toggle(True)
                    if self.sound_btn.check_input(position):
                        self.pause_music.toggle()
                    if self.pause_btn.check_input(position):
                        self.paused_game()
                elif self.stage == Game.MANUAL:
                    self.unpaused_game()
                elif self.stage == Game.PAUSED:
                    if self.pause_btn.check_input(position):
                        self.unpaused_game()

            elif event.type == pygame.KEYDOWN:
                if self.stage == Game.SPLASH or self.stage == Game.START:
                    self.stage = Game.PLAYING
                    helper.play_music()

                elif self.stage == Game.PLAYING:
                    if event.key == JUMP:
                        self.hero.jump(self.level.blocks)
                    if event.key == SOUND_OF:
                        self.pause_music.toggle()
                    if event.key == PAUSE_K:
                        self.paused_game()
                    if event.key == DOWN_VOLUME:
                        self.volume.toggle()
                    if event.key == UP_VOLUME:
                        self.volume.toggle(True)
                    if event.key == SHOOT_K:
                        self.level.x_grid += 10
                        self.flame.shoot_flame(self.window, self.level.x_grid, self.hero.rect.y)
                elif self.stage == Game.PAUSED:
                    if event.key == PAUSE_K:
                        self.unpaused_game()

                elif self.stage == Game.LEVEL_COMPLETED:
                    self.advance()

                elif self.stage == Game.VICTORY or self.stage == Game.GAME_OVER:
                    if self.flag_insert:
                        con.insert_data(self.user, self.hero.score)
                        self.flag_insert = False
                    if event.key == RESTART_K:
                        self.reset()

        pressed = pygame.key.get_pressed()

        if self.stage == Game.PLAYING:
            if pressed[LEFT]:
                self.hero.move_left()
            elif pressed[RIGHT]:
                self.hero.move_right()
            else:
                self.hero.stop()

    def update(self):
        if self.stage == Game.PLAYING:
            self.flame.update(self.level)
            self.hero.update(self.level)
            self.level.enemies.update(self.level)
        if self.level.completed:
            if self.current_level < len(levels) - 1:
                self.stage = Game.LEVEL_COMPLETED
            else:
                self.stage = Game.VICTORY
            pygame.mixer.music.stop()

        elif self.hero.lives == 0:
            self.stage = Game.GAME_OVER
            pygame.mixer.music.stop()

        elif self.hero.hearts == 0:
            self.level.reset()
            self.hero.respawn(self.level)

    def calculate_offset(self):
        x = -1 * self.hero.rect.centerx + WIDTH / 2 # obtengo el centerx del heroe divido por dos para obtener la mitad de la pantalla
        if self.hero.rect.centerx < WIDTH / 2:
            x = 0
        elif self.hero.rect.centerx > self.level.width - WIDTH / 2:
            x = -1 * self.level.width + WIDTH

        return x, 0

    def draw(self):
        offset_x, offset_y = self.calculate_offset()

        self.level.active_layer.fill(TRANSPARENT)
        self.level.active_sprites.draw(self.level.active_layer)

        if self.hero.invincibility % 3 < 2:
            self.level.active_layer.blit(self.hero.image, [self.hero.rect.x, self.hero.rect.y])

        self.window.blit(self.level.background_layer, [offset_x / 3, offset_y])
        self.window.blit(self.level.scenery_layer, [offset_x / 2, offset_y])
        self.window.blit(self.level.inactive_layer, [offset_x, offset_y])
        self.window.blit(self.level.active_layer, [offset_x, offset_y])

        self.display_stats(self.window)
        if self.flame.flame_state == "fire":
            self.level.x_grid += 10
            self.flame.shoot_flame(self.window, self.level.x_grid, self.hero.rect.y)
            if self.level.x_grid >= WIDTH:
                self.flame.flame_state = "ready"
                self.level.x_grid = GRID_SIZE * 8

        if self.stage == Game.SPLASH:
            self.display_splash(self.window)
        elif self.stage == Game.START:
            self.display_message(self.window, "Ready?!!!", "Press any key to start.")
        elif self.stage == Game.PAUSED:
            self.display_paused(self.window)
        elif self.stage == Game.MANUAL:
            self.display_manual(self.window)
        elif self.stage == Game.LEVEL_COMPLETED:
            self.display_message(self.window, "Level Complete", "Press any key to continue.")
        elif self.stage == Game.VICTORY:
            self.display_message(self.window, "You Win!", f"Press 'R' to restart.  User: {self.user} Score: {self.hero.score}")
        elif self.stage == Game.GAME_OVER:
            self.display_message(self.window, "Game Over", "Press 'R' to restart.")

        pygame.display.flip()

    def loop(self):
        while not self.done:
            self.process_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)  # por cada segundo deben pasar 60 fotogramas


def play(user):
    con.create_table()
    game = Game(user)
    game.start()
    game.loop()
    pygame.quit()
    sys.exit()
