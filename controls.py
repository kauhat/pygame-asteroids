from dataclasses import dataclass
import pygame


@dataclass
class InputState:
    game_quit = False

    #
    player_shoot = False

    player_forward = 0.0
    player_back = 0.0
    player_turn_left = 0.0
    player_turn_right = 0.0

    def apply_events(self, events):
        # Apply user inputs.
        for event in events:
            if event.type == pygame.QUIT:
                self.game_quit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_quit = True

        return self

    def apply_pressed(self, keys):
        # Player control.
        if keys[pygame.K_UP]:
            self.player_forward = 1.0

        if keys[pygame.K_DOWN]:
            self.player_back = 1.0

        if keys[pygame.K_LEFT]:
            self.player_turn_left = 1.0

        if keys[pygame.K_RIGHT]:
            self.player_turn_right = 1.0

        if keys[pygame.K_SPACE]:
            self.player_shoot = True
