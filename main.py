import esper
import pygame
from random import randrange

import components as c
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


def frame_end(state: GameState, clock):
    state.frame_end_time = pygame.time.get_ticks()

    # Wait if time remaining to cap framerate.
    frame_time = (state.frame_end_time - state.frame_start_time)
    time_remaining = (1000 // MAX_FPS) - frame_time

    if time_remaining > 0:
        pygame.time.delay(time_remaining)

    if state.show_frame_debug:
        next_debug = state.last_frame_debug + 1000

        if state.frame_end_time > next_debug:
            print("Real Time: " + str(frame_time))
            print("Remaining: " + str(time_remaining))
            print("FPS: " + str(int(clock.get_fps())))

            state.last_frame_debug = state.frame_end_time


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
    #world.add_processor(systems.EntityTreeSystem, priority=3)

    world.add_processor(systems.MovementSystem(), priority=2)
    world.add_processor(systems.ParticleEmissionSystem())
    world.add_processor(systems.LifetimeExpirySystem())
    world.add_processor(systems.PlayerControlSystem())
    world.add_processor(systems.SpriteRenderSystem(window))

    # Add player.
    player = entities.PlayerFactory().create(world)

    # Add asteroids.
    width, height = window.get_size()

    asteroids = entities.AsteroidFactory().create(world, 200)

    for asteroid in asteroids:
        transform = world.component_for_entity(asteroid, c.Transform)
        transform.position.x = randrange(width)
        transform.position.y = randrange(height)

        moveable = world.component_for_entity(asteroid, c.Moveable)
        moveable.velocity.x = 10
        moveable.velocity.rotate_ip(randrange(360))
        moveable.angular_velocity = randrange(-45, 45)

        transform = world.component_for_entity(asteroid, c.Transform)
        transform.angle = randrange(360)

    # Main loop.
    while not state.pending_exit:
        frame_start(state)

        # Get and handle user input.
        state.update_input(get_input())

        # Update game entities.
        delta = clock.tick()

        if not state.is_paused:
            world.process(state, delta)

        frame_end(state, clock)

        #
        #if state.frame_end_time > 500:
        #    state.is_paused = True

    #
    pygame.quit()


###
###
###

run()
