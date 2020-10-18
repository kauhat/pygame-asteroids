from dataclasses import dataclass
import pygame


@dataclass
class InputState:
    game_quit: bool = False

    #
    player_beep: bool = False

    player_forward: float = 0.0
    player_back: float = 0.0
    player_turn_left: float = 0.0
    player_turn_right: float = 0.0

    def apply_events(self, events):
        # Apply user inputs
        for event in events:
            if event.type == pygame.QUIT:
                self.game_quit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_quit = True

                if event.key == pygame.K_SPACE:
                    self.player_beep = True

        return self
