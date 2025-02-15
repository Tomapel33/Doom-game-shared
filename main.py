import pygame as pg
import sys
import traceback
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import Weapon, WeaponTwo
from sound import *
from pathfinding import *


class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(True)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT
        pg.time.set_timer(self.global_event, 40)
        self.difficulty = None

        print(f"Current working directory: {os.getcwd()}")

        self.sound = Sound(self)
        self.sound.play_music()

        self.background_image = pg.image.load('resources/menu/doom.image.png')
        self.background_image = pg.transform.scale(self.background_image, RES)
        self.choose_image = pg.image.load('resources/menu/Choose Skill Level.png')
        self.easy_image = pg.image.load('resources/menu/Im Too Young To Die..png')
        self.medium_image = pg.image.load('resources/menu/Hurt Me Plenty..png')
        self.hard_image = pg.image.load('resources/menu/Nightmare!.png')
        self.skeleton_image = pg.image.load('resources/menu/Skull Not Burning Eyes.png')
        self.skeleton_burning_image = pg.image.load('resources/menu/Skull Burning Eyes.png')
        self.win_image = pg.image.load('resources/menu/doom.win.png')
        self.choose_image = pg.transform.scale(self.choose_image, (1000, 100))
        self.easy_image = pg.transform.scale(self.easy_image, (900, 100))
        self.medium_image = pg.transform.scale(self.medium_image, (900, 100))
        self.hard_image = pg.transform.scale(self.hard_image, (900, 100))
        self.skeleton_image = pg.transform.scale(self.skeleton_image, (70, 100))
        self.skeleton_burning_image = pg.transform.scale(self.skeleton_burning_image, (70, 100))
        self.win_image = pg.transform.scale(self.win_image, RES)

        # Initialize image rects
        self.easy_image_rect = self.easy_image.get_rect()
        self.medium_image_rect = self.medium_image.get_rect()
        self.hard_image_rect = self.hard_image.get_rect()

        self.hovered_difficulty = None
        self.run_start_screen()

    def run_start_screen(self):
        while True:
            self.check_start_screen_events()
            self.draw_start_screen()

    def check_start_screen_events(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        self.hovered_difficulty = None

        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if self.is_button_clicked(mouse_x, mouse_y, self.easy_image_rect):
                    self.difficulty = "easy"
                    print("Selected difficulty: Easy")
                    self.new_game()
                    return
                elif self.is_button_clicked(mouse_x, mouse_y, self.medium_image_rect):
                    self.difficulty = "medium"
                    print("Selected difficulty: Medium")
                    self.new_game()
                    return
                elif self.is_button_clicked(mouse_x, mouse_y, self.hard_image_rect):
                    self.difficulty = "hard"
                    print("Selected difficulty: Hard")
                    self.new_game()
                    return

        if self.is_button_clicked(mouse_x, mouse_y, self.easy_image_rect):
            self.hovered_difficulty = "easy"
        elif self.is_button_clicked(mouse_x, mouse_y, self.medium_image_rect):
            self.hovered_difficulty = "medium"
        elif self.is_button_clicked(mouse_x, mouse_y, self.hard_image_rect):
            self.hovered_difficulty = "hard"

    def is_button_clicked(self, mouse_x, mouse_y, rect):
        return rect.collidepoint(mouse_x, mouse_y)

    def draw_start_screen(self):
        self.screen.blit(self.background_image, (0, 0))

        choose_image_pos = (WIDTH // 2 - self.choose_image.get_width() // 2, 70)  # Moved down by 20 pixels
        easy_image_pos = (WIDTH // 2 - self.easy_image.get_width() // 2, 220)  # Moved down by 20 pixels
        medium_image_pos = (WIDTH // 2 - self.medium_image.get_width() // 2, 340)  # Moved down by 20 pixels
        hard_image_pos = (WIDTH // 2 - self.hard_image.get_width() // 2, 460)  # Moved down by 20 pixels

        skeleton_left_easy_pos = (WIDTH // 2 - self.easy_image.get_width() // 2 - 250, 220)  # Moved down by 20 pixels
        skeleton_right_easy_pos = (WIDTH // 2 + self.easy_image.get_width() // 2 + 50, 220)  # Moved down by 20 pixels
        skeleton_left_medium_pos = (WIDTH // 2 - self.medium_image.get_width() // 2 - 250, 340)  # Moved down by 20 pixels
        skeleton_right_medium_pos = (WIDTH // 2 + self.medium_image.get_width() // 2 + 50, 340)  # Moved down by 20 pixels
        skeleton_left_hard_pos = (WIDTH // 2 - self.hard_image.get_width() // 2 - 250, 460)  # Moved down by 20 pixels
        skeleton_right_hard_pos = (WIDTH // 2 + self.hard_image.get_width() // 2 + 50, 460)  # Moved down by 20 pixels

        self.screen.blit(self.choose_image, choose_image_pos)
        self.easy_image_rect.topleft = easy_image_pos
        self.medium_image_rect.topleft = medium_image_pos
        self.hard_image_rect.topleft = hard_image_pos

        self.screen.blit(self.easy_image, easy_image_pos)
        self.screen.blit(self.medium_image, medium_image_pos)
        self.screen.blit(self.hard_image, hard_image_pos)

        if self.hovered_difficulty == "easy":
            self.screen.blit(self.skeleton_burning_image, skeleton_left_easy_pos)
            self.screen.blit(self.skeleton_burning_image, skeleton_right_easy_pos)
        else:
            self.screen.blit(self.skeleton_image, skeleton_left_easy_pos)
            self.screen.blit(self.skeleton_image, skeleton_right_easy_pos)

        if self.hovered_difficulty == "medium":
            self.screen.blit(self.skeleton_burning_image, skeleton_left_medium_pos)
            self.screen.blit(self.skeleton_burning_image, skeleton_right_medium_pos)
        else:
            self.screen.blit(self.skeleton_image, skeleton_left_medium_pos)
            self.screen.blit(self.skeleton_image, skeleton_right_medium_pos)

        if self.hovered_difficulty == "hard":
            self.screen.blit(self.skeleton_burning_image, skeleton_left_hard_pos)
            self.screen.blit(self.skeleton_burning_image, skeleton_right_hard_pos)
        else:
            self.screen.blit(self.skeleton_image, skeleton_left_hard_pos)
            self.screen.blit(self.skeleton_image, skeleton_right_hard_pos)

        pg.display.flip()

    def new_game(self):
        print("Starting new game...")
        try:
            self.set_difficulty()
            print(f"Difficulty set. Enemy health: {self.enemy_health}, Enemy damage: {self.enemy_damage}")

            self.map = Map(self)
            print("Map initialized.")
            self.player = Player(self)
            print("Player initialized.")
            self.object_renderer = ObjectRenderer(self)
            print("ObjectRenderer initialized.")
            self.raycasting = RayCasting(self)
            print("RayCasting initialized.")
            self.object_handler = ObjectHandler(self)
            print("ObjectHandler initialized.")
            if self.difficulty == 'hard':
                self.weapon = WeaponTwo(self)
                print("WeaponTwo initialized.")
            else:
                self.weapon = Weapon(self)
                print("Weapon initialized.")
            self.sound = Sound(self)
            print("Sound system initialized.")
            print("Music playing.")
            self.pathfinding = PathFinding(self)
            print("PathFinding initialized.")

            pg.mouse.set_visible(False)
            self.run_game()
        except Exception as e:
            print(f"An error occurred during game initialization: {e}")
            traceback.print_exc()
            pg.quit()
            sys.exit()

    def set_difficulty(self):
        if self.difficulty == 'easy':
            self.enemy_health = {'NPC': 100, 'CacoDemonNPC': 100, 'CyberDemonNPC': 250}
            self.enemy_damage = {'NPC': 2, 'CacoDemonNPC': 1, 'CyberDemonNPC': 2}
        elif self.difficulty == 'medium':
            self.enemy_health = {'NPC': 125, 'CacoDemonNPC': 150, 'CyberDemonNPC': 350}
            self.enemy_damage = {'NPC': 2, 'CacoDemonNPC': 2, 'CyberDemonNPC': 3}
        elif self.difficulty == 'hard':
            self.enemy_health = {'NPC': 0, 'CacoDemonNPC':0, 'CyberDemonNPC': 5000}
            self.enemy_damage = {'NPC': 2, 'CacoDemonNPC': 1, 'CyberDemonNPC': 5}
        print(f"Set difficulty: {self.difficulty}")
        print(f"Enemy Health: {self.enemy_health}")
        print(f"Enemy Damage: {self.enemy_damage}")

    def update(self):
        if self.object_handler.all_enemies_dead():
            self.display_win_screen()
        else:
            self.player.update()
            self.raycasting.update()
            self.object_handler.update()
            self.weapon.update()
            pg.display.flip()
            self.delta_time = self.clock.tick(FPS)
            pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def display_win_screen(self):
        print("Displaying win screen")
        self.screen.blit(self.win_image, (0, 0))
        pg.display.flip()
        pg.time.delay(3000)
        self.run_start_screen()

    def draw(self):
        self.object_renderer.draw()
        self.weapon.draw()

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)

    def run_game(self):
        print("Game loop started.")
        while True:
            try:
                self.check_events()
                self.update()
                self.draw()
            except Exception as e:
                print(f"An error occurred during the game loop: {e}")
                traceback.print_exc()
                pg.quit()
                sys.exit()


if __name__ == '__main__':
    game = Game()
    game.run_game()