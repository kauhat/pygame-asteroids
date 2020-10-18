import pygame
from random import randrange

import entities
import controls


class GameState:
    def __init__(self):
        self.pendingExit = False


class Game:
    def __init__(self, window):
        self.clock = pygame.time.Clock()
        self.window = window
        self.max_fps = 144

        self.state = GameState()
        self.entities = []

    def add_entity(self, entity):
        self.entities.append(entity)

        return entity

    def get_input(self, events):
        frame_input = controls.InputState().apply_events(events)

        return frame_input

    def handle_input(self, game_input):
        if game_input.game_quit:
            print("Quitting...")
            self.state.pendingExit = True

        if game_input.player_beep:
            print("beep")

    def tick(self, delta):
        for entity in self.entities:
            entity.tick(self.state, delta)

    def render(self):
        # Clear the screen.
        self.window.fill((0, 0, 0))

        for entity in self.entities:
            entity.render(game.window)

        #
        pygame.display.update()

    def frame_start(self):
        self.frame_start_time = pygame.time.get_ticks()

    def frame_end(self):
        self.frame_end_time = pygame.time.get_ticks()

        # Wait if time remaining to cap framerate.
        frame_time = (self.frame_end_time - self.frame_start_time)
        time_remaining = (1000 // self.max_fps) - frame_time

        if time_remaining > 0:
            pygame.time.delay(time_remaining)

        # print("Real Time: " + str(frame_time))
        # print("Remaining: " + str(time_remaining))
        # print("FPS: " + str(int(game.clock.get_fps())))

###
###
###
def setup_window(width=800, height=600):
    window = pygame.display.set_mode((width, height))

    return window


###
###
###
pygame.init()
game = Game(setup_window())

# Add asteroids.
amount = 200
width, height = game.window.get_size()

for i in range(amount):
    asteroid = entities.Asteroid()
    asteroid.position.x = randrange(width)
    asteroid.position.y = randrange(height)
    asteroid.velocity = pygame.math.Vector2(10, 0).rotate(randrange(360))

    game.add_entity(asteroid)

# Main loop.
while not game.state.pendingExit:
    game.frame_start()

    # Get and handle user input.
    frame_input = game.get_input(pygame.event.get())
    game.handle_input(frame_input)

    # Update game entities.
    delta = game.clock.tick()
    game.tick(delta)

    # Render
    game.render()

    game.frame_end()

#
pygame.quit()
