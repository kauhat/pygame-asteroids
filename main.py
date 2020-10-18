from dataclasses import dataclass
import pygame

@dataclass
class FrameInput:
    game_quit: bool = False

    #
    player_beep: bool = False

    player_forward: float = 0.0
    player_back: float = 0.0
    player_turn_left: float = 0.0
    player_turn_right: float = 0.0

class GameState:
    def __init__(self):
        self.pendingExit = False

class Game:
    def __init__(self, window):
        #
        pygame.init()

        self.clock = pygame.time.Clock()
        self.window = window
        self.max_fps = 144

        self.state = GameState()

    def get_input(self, events):
        frame_input = FrameInput()

        for event in events:
            if event.type == pygame.QUIT:
                frame_input.quit = True
                print(frame_input)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    frame_input.quit = True

                if event.key == pygame.K_SPACE:
                    frame_input.player_beep = True

        return frame_input

    def handle_input(self, game_input):
        if game_input.quit:
            print("Quitting...")
            self.state.pendingExit = True

        if game_input.player_beep:
            print("cock")

    def tick(self, delta):
        pass

    def render(self):
        pass

    def frame_start(self):
        # Clear the screen.
        self.window.fill((0, 0, 0))

    def frame_end(self):
        #
        pygame.display.update()
        game.clock.tick_busy_loop(game.max_fps)


def setup_window(width=800, height=600):
    window = pygame.display.set_mode((width, height))

    return window


###
###
###
game = Game(setup_window())

#game.add_entity()

while not game.state.pendingExit:
    game.frame_start()

    # Get and handle user input.
    frame_input = game.get_input(pygame.event.get())
    #print(frame_input)
    #print(game.state)
    game.handle_input(frame_input)

    # Update game entities.
    delta = game.clock.tick()
    #print(delta)
    game.tick(delta)

    # Render
    game.render()

    game.frame_end()

pygame.quit()
