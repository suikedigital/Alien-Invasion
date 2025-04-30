import pygame
import logging
import sys

class AssetManager:
    """A class to manage game assets, like images and sounds."""

    def __init__(self):
        self.cache = {} # Cache to store loaded assets

    def load_image(self, file_path: str):
        """Load an image from the given file path and cache it."""
        if file_path in self.cache:
            return self.cache[file_path]
        try:
            image = pygame.image.load()
            self.cache[file_path] = image
            return image
        except pygame.error as e:
            logging.info(f"Error loading image '{file_path}': {e}")