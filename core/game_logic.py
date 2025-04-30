import sys
from time import sleep

import pygame

from core.settings import Settings
from core.game_stats import GameStats

from ui.scoreboard import Scoreboard
from ui.button import Button

from entities.ship import Ship
from entities.bullet import Bullet
from entities.alien import Alien
from entities.fleet_manager import FleetManager
from entities.bullet_manager import BulletManager

from assets.utils import AssetManager


class GameLogic:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.bg_color = (self.settings.bg_color) 
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # Start alien invasion in an inactive state. 
        self.game_active = False
        self.play_button = Button(self, "Play")

        # Create and Instance to store game statistics 
        # and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.asset_manager = AssetManager()
        self.fleet_manager = FleetManager(self)
        self.bullet_manager - BulletManager(self)

        self.ship = Ship(self, self.asset_manager)
        
        self._create_fleet()

    def _fire_bullet(self):
        """Delegate the firing of a bullet to the BulletManager."""
        self.bullet_manager.fire_bullet()

    def _update_bullets(self):
        """Delegate the updating of bullets to the BulletManager."""
        self.bullet_manager.update()
        self.bullet_manager.check_collions(self.fleet_manager.aliens, self.stats, self.sb)

    def _update_aliens(self):
        """Check if the fleet is at an edge, then update positions"""
        self.fleet_manager.update()
        self._check_ship_alien_collisions()
        self._check_aliens_bottom()

    def _reset_entities(self):
        """Remove all bullets and aliens from the screen, and then create a new fleet and center the ship."""
        self.bullets.empty()
        self.fleet_manager.aliens.empty()
        self.fleet_manager.create_fleet()
        self.ship.center_ship()
        

    def _update_screen(self):
         # Redraw the screen during each pass through the loop.
        self.screen.fill(self.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw the play burron iof the game is inactive.
        if not self.game_active:
            self.play_button.draw_button() 
            
        # Make the most recent drawn screen visible. 
        pygame.display.flip()

    # Event handling
    def _check_events(self):
        """Respond to keypresses, releases and mouse events, and hands them off to the appropriate methods."""
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self._handle_keydown(event)
            elif event.type == pygame.KEYUP:
                self._handle_keyup(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mousebuttondown(event)    

    # Respond to key presses
    def _handle_keydown(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_p:
            self.game_active = not self.game_active
        elif event.key == pygame.K_f:
            self._toggle_fullscreen()
            

    def _toggle_fullscreen(self):
        if self.screen.get_flags() & pygame.FULLSCREEN:
            self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        else:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    # Respond to key releases
    def _handle_keyup(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _handle_mousebuttondown(self, event):
        mouse_pos = pygame.mouse.get_pos()
        self._check_play_button(mouse_pos)

    # Respond to mouse events
    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # Reset the game settings.
            self._reset_game_settings()
            self.game_active = True
            self._reset_entities()
            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def _reset_game_settings(self):
        """Reset the game settings to their initial values."""
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()


    def _ship_hit(self):
        """ Respond to the ship being hit by an alien """
        if self.stats.ships_left > 0:
            #Decrement ships left and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # Get rid of any remaining aliens and bullets.
            self.bullets.empty()
            self.aliens.empty()
            # Create a new fleet and centre the ship.
            self._create_fleet()
            self.ship.center_ship()
            # Pause.
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_ship_alien_collisions(self):
        """Check for any aliens that have hit the ship. If so, get rid of the ship."""
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break
    
        # Check if all aliens have been destroyed, Create a new level if so.
        if not self.aliens:
            self._start_new_level()
            
    def _start_new_level(self):
        """Start a new level by creating a new fleet and increasing difficulty."""
        self.bullets.empty()
        self._create_fleet()
        self.settings.increase_speed()
        self.stats.level += 1
        self.sb.prep_level()



