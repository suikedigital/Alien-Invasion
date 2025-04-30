import pygame
from pygame.sprite import Sprite
from assets.utils import AssetManager


class Alien(Sprite):
    """A class to represent a single alien in the fleet."""
    
    def __init__(self, ai_game, asset_manager):
        """Initialise the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Get the rect attribute of the alien image.
        self.asset_manager = AssetManager()
        self.image = asset_manager.load_image('assets/images/alien.bmp')
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)

    def update(self):
        """Move the alien horizontally based on the fleet direction."""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x 

    def check_edges(self):
        """
        Check if the alien is at the edge of the screen.

        Returns:
        bool: True if the alien is at the left or right edge of the screen.
        """
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)
    

        
    