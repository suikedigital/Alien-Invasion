import json


class Settings:
    """A class to store al settings for Alien Invasion."""

    def __init__(self):
        """Loads the config settings and Initialise the game's settings."""
        with open('assets/config.json', 'r') as f:
            self.config = json.load(f)

        # Initialise the static settings
        self.initialize_static_settings()
        # Initialise the dynamic settings
        self.initialize_dynamic_settings()
    
    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 1.5
        self.bullet_speed = 10
        self.alien_speed = 1.0
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

    def initialize_static_settings(self):
        """Initialize settings that do not change throughout the game."""
        # Initialize the game's static settings.
        # Screen settings
        self.screen_width = self.config['screen_width']
        self.screen_height = self.config['screen_height']
        self.bg_color = self.config['bg_color']
        self.frame_rate = self.config['frame_rate']
        # Initalise the Entity settings
        # Ship settings
        self.ship_limit = self.config['ship_limit']
        # Alien settings
        self.fleet_drop_speed = self.config['fleet_drop_speed']
        # Bullet settings
        self.bullet_width = self.config['bullet_width']
        self.bullet_height = self.config['bullet_height']
        self.bullet_color = self.config['bullet_color']
        self.bullets_allowed = self.config['bullets_allowed']
        # Scoring settings
        self.alien_points = 50
        self.speedup_scale = 1.1
        self.score_scale = 1.5    
        

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        