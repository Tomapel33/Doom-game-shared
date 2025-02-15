import pygame as pg
from settings import *

class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('resources/textures/sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        self.blood_screen = self.get_texture('resources/textures/blood_screen.png', RES)
        self.digit_size = 90
        self.digit_images = [self.get_texture(f'resources/textures/digits/{i}.png', [self.digit_size] * 2) for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))
        self.game_over_image = self.get_texture('resources/textures/game_over.png', RES)

        # Load head background and animation images
        self.load_head_images()
        self.head_animation_index = 0
        self.head_animation_time = 500  # Milliseconds per frame
        self.last_head_update = pg.time.get_ticks()
        self.current_animation = 'normal'  # Track current animation state
        self.below_80_cycle = [0, 1, 2, 1]  # Custom cycle for below-80 health animation
        self.below_80_index = 0  # Index for custom cycle
        self.below_60_cycle = [0, 1, 2, 1]  # Custom cycle for below-60 health animation
        self.below_60_index = 0  # Index for custom cycle
        self.below_40_cycle = [0, 1, 2, 1]  # Custom cycle for below-40 health animation
        self.below_40_index = 0  # Index for custom cycle
        self.below_20_cycle = [0, 1, 2, 1]  # Custom cycle for below-20 health animation
        self.below_20_index = 0  # Index for custom cycle

    def load_head_images(self):
        self.head_background = self.get_texture('resources/head/doom.backround.png', (200, 200))  # Enlarged background
        self.head_images = [
            self.get_texture('resources/head/doom.head1.png', (180, 180)),  # Enlarged head images
            self.get_texture('resources/head/doom.head2.png', (180, 180)),
            self.get_texture('resources/head/doom.head3.png', (180, 180))
        ]
        # Load hit animation images
        self.head_hit_images = [
            self.get_texture('resources/head/doom.headhit1.png', (180, 180)),  # Enlarged hit images
            self.get_texture('resources/head/doom.headhit2.png', (180, 180))
        ]
        # Load below-80 health animation images
        self.head_80_images = [
            self.get_texture('resources/head/doom.head80(1).png', (180, 180)),  # Enlarged below-80 images
            self.get_texture('resources/head/doom.head80(2).png', (180, 180)),
            self.get_texture('resources/head/doom.head80(3).png', (180, 180))
        ]
        # Load below-60 health animation images
        self.head_60_images = [
            self.get_texture('resources/head/doom.head60(1).png', (180, 180)),  # Enlarged below-60 images
            self.get_texture('resources/head/doom.head60(2).png', (180, 180)),
            self.get_texture('resources/head/doom.head60(3).png', (180, 180))
        ]
        # Load below-40 health animation images
        self.head_40_images = [
            self.get_texture('resources/head/doom.head40(1).png', (180, 180)),  # Enlarged below-40 images
            self.get_texture('resources/head/doom.head40(2).png', (180, 180)),
            self.get_texture('resources/head/doom.head40(3).png', (180, 180))
        ]
        # Load below-20 health animation images
        self.head_20_images = [
            self.get_texture('resources/head/doom.head20(1).png', (180, 180)),  # Enlarged below-20 images
            self.get_texture('resources/head/doom.head20(2).png', (180, 180)),
            self.get_texture('resources/head/doom.head20(3).png', (180, 180))
        ]

    def update_head_animation(self):
        now = pg.time.get_ticks()
        if now - self.last_head_update > self.head_animation_time:
            self.last_head_update = now
            if self.game.player.hit:
                # Switch to hit animation
                self.current_animation = 'hit'
                self.head_animation_index = (self.head_animation_index + 1) % len(self.head_hit_images)
                print(f"Switching to hit animation, index: {self.head_animation_index}")
                # Reset hit flag
                self.game.player.hit = False
            elif self.game.player.health < 20:
                # Switch to below-20 health animation
                if self.current_animation != 'below_20':
                    self.head_animation_index = 0  # Reset index when switching animations
                    self.below_20_index = 0  # Reset custom cycle index
                self.current_animation = 'below_20'
                self.head_animation_index = self.below_20_cycle[self.below_20_index]
                self.below_20_index = (self.below_20_index + 1) % len(self.below_20_cycle)
                print(f"Switching to below-20 animation, index: {self.head_animation_index}")
            elif self.game.player.health < 40:
                # Switch to below-40 health animation
                if self.current_animation != 'below_40':
                    self.head_animation_index = 0  # Reset index when switching animations
                    self.below_40_index = 0  # Reset custom cycle index
                self.current_animation = 'below_40'
                self.head_animation_index = self.below_40_cycle[self.below_40_index]
                self.below_40_index = (self.below_40_index + 1) % len(self.below_40_cycle)
                print(f"Switching to below-40 animation, index: {self.head_animation_index}")
            elif self.game.player.health < 60:
                # Switch to below-60 health animation
                if self.current_animation != 'below_60':
                    self.head_animation_index = 0  # Reset index when switching animations
                    self.below_60_index = 0  # Reset custom cycle index
                self.current_animation = 'below_60'
                self.head_animation_index = self.below_60_cycle[self.below_60_index]
                self.below_60_index = (self.below_60_index + 1) % len(self.below_60_cycle)
                print(f"Switching to below-60 animation, index: {self.head_animation_index}")
            elif self.game.player.health < 80:
                # Switch to below-80 health animation
                if self.current_animation != 'below_80':
                    self.head_animation_index = 0  # Reset index when switching animations
                    self.below_80_index = 0  # Reset custom cycle index
                self.current_animation = 'below_80'
                self.head_animation_index = self.below_80_cycle[self.below_80_index]
                self.below_80_index = (self.below_80_index + 1) % len(self.below_80_cycle)
                print(f"Switching to below-80 animation, index: {self.head_animation_index}")
            else:
                # Switch to normal animation if not already in the normal animation
                if self.current_animation != 'normal':
                    self.head_animation_index = 0  # Reset index when switching animations
                self.current_animation = 'normal'
                self.head_animation_index = (self.head_animation_index + 1) % len(self.head_images)
                print(f"Switching to normal animation, index: {self.head_animation_index}")

    def draw_head(self):
        # Draw the background
        self.screen.blit(self.head_background, (WIDTH - 190, 10))  # Adjusted position for larger images
        # Draw the current head image on top of the background
        try:
            if self.current_animation == 'hit':
                head_image = self.head_hit_images[self.head_animation_index]
            elif self.current_animation == 'below_20':
                head_image = self.head_20_images[self.head_animation_index]
            elif self.current_animation == 'below_40':
                head_image = self.head_40_images[self.head_animation_index]
            elif self.current_animation == 'below_60':
                head_image = self.head_60_images[self.head_animation_index]
            elif self.current_animation == 'below_80':
                head_image = self.head_80_images[self.head_animation_index]
            else:
                head_image = self.head_images[self.head_animation_index]
            self.screen.blit(head_image, (WIDTH - 190, 20))  # Adjusted position for larger images
        except IndexError as e:
            print(f"Error drawing head animation: {e}, index: {self.head_animation_index}")

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()
        self.update_head_animation()
        self.draw_head()

    def game_over(self):
        self.screen.blit(self.game_over_image, (0, 0))

    def draw_player_health(self):
        health = str(self.game.player.health)
        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], (i * self.digit_size, 0))
        self.screen.blit(self.digits['10'], ((i + 1) * self.digit_size, 0))

    def player_damage(self):
        self.screen.blit(self.blood_screen, (0, 0))

    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        # floor
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        return {
            1: self.get_texture('resources/textures/1.png'),
            2: self.get_texture('resources/textures/2.png'),
            3: self.get_texture('resources/textures/3.png'),
            4: self.get_texture('resources/textures/4.png'),
            5: self.get_texture('resources/textures/5.png'),
        }