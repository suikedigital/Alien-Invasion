import pygame 
from pygame.bullet import Bullet

class BulletManager:
    """A class to manage bullets fired by the ship."""

    def __init__(self, game_logic):
        """Initialize the bullet manager."""
        self.game_logic = game_logic
        self.settings = game_logic.settings
        self.bullets = pygame.sprite.Group()

    def fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def update(self):
        """Update the position of the bullets and remove old bullets."""
        self.bullets.update()
        self._remove_offscreen_bullets()

    def _remove_offscreen_bullets(self):
        """Remove bullets that have gone off the screen."""
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def check_collions(self, aliens, stats, scoreboard):
        """Check for bullet-alien collisions and update the score."""
        collisions = pygame.sprite.groupcollide(self.bullets, aliens, True, True)
        if collisions:
            for aliens_hit in collisions.values():
                stats.score += self.settings.alien_points * len(aliens_hit)
            scoreboard.prep_score()
            scoreboard.check_high_score()

    