from core.game_logic import GameLogic

class GameLoop:
    def __init__(self):
        self.running = True
        self.game_state = "menu"  # Possible states: menu, playing, paused, game_over
        self.game = GameLogic()

    def run_game(self):
        """Start the main loop for the game."""
        while self.running:
            self.game._check_events
            if self.game.game_active:
                self.game.update_game()

                self.game.ship.update()
                self.game._update_bullets()
                self.game._update_aliens()
            self.game._update_screen()
            self.game.clock.tick(self.game.settings.frame_rate)  # Set the frame rate to the configured value

            
    def handle_events(self):
        # Handle user input and events
        pass

    def update(self):
        # Update game state based on events and logic
        pass

    def render(self):
        # Render the current game state to the screen
        pass
