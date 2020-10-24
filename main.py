import esper
import pygame
from random import randrange

import components
from controls import InputState
import entities
from state import GameState
import systems

MAX_FPS = 144


def setup_window(width=800, height=600):
    size = (width, height)
    flags = pygame.HWSURFACE | pygame.DOUBLEBUF

    #
    window = pygame.display.set_mode(size, flags)

    return window


def frame_start(state: GameState):
    state.frame_start_time = pygame.time.get_ticks()


def frame_end(state: GameState):
    state.frame_end_time = pygame.time.get_ticks()

    # Wait if time remaining to cap framerate.
    frame_time = (state.frame_end_time - state.frame_start_time)
    time_remaining = (1000 // MAX_FPS) - frame_time

    if time_remaining > 0:
        pygame.time.delay(time_remaining)

    # print("Real Time: " + str(frame_time))
    # print("Remaining: " + str(time_remaining))
    # print("FPS: " + str(int(game.clock.get_fps())))


def get_input():
    events = pygame.event.get()
    pressed = pygame.key.get_pressed()

    frame_input = InputState()
    frame_input.apply_events(events)
    frame_input.apply_pressed(pressed)

    return frame_input


def run():
    pygame.init()

    window = setup_window()

    clock = pygame.time.Clock()
    state = GameState()

    # Create ECS world.
    world = esper.World()

    # Add systems/processors.
    world.add_processor(systems.SpriteRenderSystem(window))
    world.add_processor(systems.MovementSystem())
    world.add_processor(systems.PlayerControlSystem())

    # Add asteroids.
    amount = 200
    width, height = window.get_size()

    for i in range(amount):
        position = pygame.math.Vector2(randrange(width), randrange(height))
        asteroid = entities.AsteroidFactory().create(world, position)

        moveable = world.component_for_entity(asteroid, components.Moveable)
        moveable.velocity.x = 10
        moveable.velocity.rotate_ip(randrange(360))
        moveable.angular_velocity = randrange(-45, 45)

        transform = world.component_for_entity(asteroid, components.Transform)
        transform.angle = randrange(360)

    # Add player.
    position_p = pygame.math.Vector2(width / 2, height / 2)
    player = entities.PlayerFactory().create(world, position_p)


    # Main loop.
    while not state.pendingExit:
        frame_start(state)

        # Get and handle user input.
        state.update_input(get_input())

        # Update game entities.
        delta = clock.tick()
        world.process(state, delta)

        frame_end(state)

    #
    pygame.quit()


###
###
###

run()
