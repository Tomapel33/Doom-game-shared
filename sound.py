import pygame as pg

class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = 'resources/sound/'  # Base path for sounds
        self.shotgun = pg.mixer.Sound(self.path + 'shotgun.wav')
        self.npc_pain = pg.mixer.Sound(self.path + 'npc_pain.wav')
        self.npc_death = pg.mixer.Sound(self.path + 'npc_death.wav')
        self.npc_shot = pg.mixer.Sound(self.path + 'npc_attack.wav')
        self.player_pain = pg.mixer.Sound(self.path + 'player_pain.wav')
        self.doom_chaingun = pg.mixer.Sound(self.path + 'doomchaingunsound.wav')  # Add the new sound
        self.theme_path = self.path + 'theme.mp3'  # Store the path to theme.mp3

    def play_music(self):
        """Play the Doom theme music in a continuous loop."""
        try:
            pg.mixer.music.load(self.theme_path)  # Load the theme music
            pg.mixer.music.set_volume(0.7)  # Set the volume to 50%
            pg.mixer.music.play(-1)  # Loop the music indefinitely
            print("Theme music is playing!")
        except Exception as e:
            print(f"Error loading music: {e}")
