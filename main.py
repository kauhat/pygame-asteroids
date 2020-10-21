import pygame
from random import randrange

import entities
import controls


class GameState:
    def __init__(self):
        self.pendingExit = False

        self.input: controls.InputState = None


class Game:
    def __init__(self, window):
        self.clock = pygame.time.Clock()
        self.window = window
        self.max_fps = 144

        self.state = GameState()
        self.entities = []
        self.render_groups = {
            "gameplay": pygame.sprite.RenderPlain()
        }

    def add_entity(self, entity):
        entity.init(self)
        self.entities.append(entity)

        return entity

    def get_input(self):
        events = pygame.event.get()
        pressed = pygame.key.get_pressed()

        frame_input = controls.InputState()
        frame_input.apply_events(events)
        frame_input.apply_pressed(pressed)

        return frame_input

    def handle_input(self, game_input):
        if game_input.game_quit:
            print("Quitting...")
            self.state.pendingExit = True

        # Add current frame input map to state.
        self.state.previous_input = self.state.input
        self.state.input = game_input

    def tick(self, delta):
        for entity in self.entities:
            entity.tick(self.state, delta)

    def render(self):
        # Clear the screen.
        self.window.fill((0, 0, 0))

        # for entity in self.entities:
        #    entity.render(game.state, game.window)

        self.render_groups['gameplay'].draw(self.window)

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
    position = pygame.math.Vector2(randrange(width), randrange(height))
    asteroid = entities.AsteroidFactory().create(game, position)

    transform = asteroid.get_component(entities.TransformComponent)
    transform.velocity.x = 10
    transform.velocity.rotate(randrange(360))

    transform.angle = randrange(360)
    transform.angular_velocity = randrange(-45, 45)

    sprite = asteroid.get_component(entities.SpriteComponent)
    sprite.add_to_group(game.render_groups['gameplay'])

    game.add_entity(asteroid)

# Add player.
# player = entities.Player()
# player.position.x = width / 2
# player.position.y = height / 2

# player.add_to_group(game.render_groups['gameplay'])

# game.add_entity(player)

# Main loop.
while not game.state.pendingExit:
    game.frame_start()

    # Get and handle user input.
    frame_input = game.get_input()
    game.handle_input(frame_input)

    # Update game entities.
    delta = game.clock.tick()
    game.tick(delta)

    # Render
    game.render()

    game.frame_end()

#
pygame.quit()
