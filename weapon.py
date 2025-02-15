from sprite_object import *

class Weapon(AnimatedSprite):
    def __init__(self, game, path='resources/sprites/weapon/0.png', scale=0.4, animation_time=90):
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
        self.images = deque(
            [pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
             for img in self.images])
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())
        self.reloading = False
        self.num_images = len(self.images)
        self.frame_counter = 0
        self.damage = 50

    def animate_shot(self):
        if self.reloading:
            self.game.player.shot = False
            if self.animation_trigger:
                self.images.rotate(-1)  # Rotates images for animation
                self.image = self.images[0]  # Updates to the first image in the rotated list.
                self.frame_counter += 1
                if self.frame_counter == self.num_images:
                    self.reloading = False
                    self.frame_counter = 0

    def draw(self):
        self.game.screen.blit(self.images[0], self.weapon_pos)

    def update(self):
        self.check_animation_time()
        self.animate_shot()

class WeaponTwo(AnimatedSprite):
    def __init__(self, game, scale=1.5, animation_time=90):  # Increased scale for larger image
        path_idle = 'resources/sprites/wepontwo/doom_gun1.png'
        path_shoot = 'resources/sprites/wepontwo/doom_gun2.png'
        path_shot1 = 'resources/sprites/wepontwo/doomshot3.png'
        path_shot2 = 'resources/sprites/wepontwo/doomshot4.png'
        super().__init__(game=game, path=path_idle, scale=scale, animation_time=animation_time)

        # Load and scale all images
        self.idle_image = pg.image.load(path_idle).convert_alpha()
        self.shoot_image = pg.image.load(path_shoot).convert_alpha()
        self.shot_image1 = pg.image.load(path_shot1).convert_alpha()
        self.shot_image2 = pg.image.load(path_shot2).convert_alpha()

        self.idle_image = pg.transform.smoothscale(self.idle_image,
                                                   (self.idle_image.get_width() * scale,
                                                    self.idle_image.get_height() * scale))
        self.shoot_image = pg.transform.smoothscale(self.shoot_image,
                                                    (self.idle_image.get_width(), self.idle_image.get_height()))

        # Adjust the scale factor for the shot images here to make them bigger
        shot_scale = 1.4  # Increase this value to make the shot images larger
        self.shot_image1 = pg.transform.smoothscale(self.shot_image1,
                                                    (self.shot_image1.get_width() * shot_scale,
                                                     self.shot_image1.get_height() * shot_scale))
        self.shot_image2 = pg.transform.smoothscale(self.shot_image2,
                                                    (self.shot_image2.get_width() * shot_scale,
                                                     self.shot_image2.get_height() * shot_scale))

        self.images = deque([self.idle_image, self.shoot_image])
        self.shot_images = deque([self.shot_image1, self.shot_image2])
        self.image = self.idle_image  # Set initial image
        self.weapon_pos = (HALF_WIDTH - self.idle_image.get_width() // 2,
                           HEIGHT - self.idle_image.get_height() + 20)  # Adjusted position lower
        # Adjust shot_pos to be at the end of the machine gun's image (the barrel)
        self.shot_pos = (HALF_WIDTH - self.shot_image1.get_width() // 2,
                         HEIGHT - self.idle_image.get_height() - 45)  # Adjust this value to tweak position
        self.reloading = False
        self.num_images = len(self.images)
        self.frame_counter = 0
        self.shot_frame_counter = 0
        self.damage = 50

    def animate_shot(self):
        if pg.mouse.get_pressed()[0]:  # Check if left mouse button is held down
            self.game.player.shot = True
            if self.animation_trigger:
                self.image = self.shoot_image if self.image == self.idle_image else self.idle_image  # Toggle between images
                self.frame_counter += 1
                if self.frame_counter == self.num_images:
                    self.frame_counter = 0
                self.shot_images.rotate(-1)  # Rotate shot images for animation
                self.shot_frame_counter += 1
                if self.shot_frame_counter == len(self.shot_images):
                    self.shot_frame_counter = 0
                # Play the chaingun sound if the difficulty is hard
                if self.game.difficulty == 'hard':
                    self.game.sound.doom_chaingun.play()
        else:
            self.game.player.shot = False
            self.image = self.idle_image  # Reset to idle image

    def draw(self):
        self.game.screen.blit(self.image, self.weapon_pos)
        if self.game.player.shot:
            self.game.screen.blit(self.shot_images[0], self.shot_pos)

    def update(self):
        self.check_animation_time()
        self.animate_shot()