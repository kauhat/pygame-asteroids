import os

import esper
import pygame
from pygame.math import Vector2

import components as c


class EntityFactory:
    def create(self, world: esper.World):
        raise NotImplementedError


class AsteroidFactory(EntityFactory):
    def create(self, world: esper.World, position: Vector2):
        print("Creating asteroid...")

        asteroid = world.create_entity()

        #
        world.add_component(asteroid, c.Transform(position))

        #
        moveable = c.Moveable()
        world.add_component(asteroid, moveable)

        #
        surface = pygame.image.load(os.path.join('assets', 'asteroid-64.png'))

        sprite = c.Sprite(surface)
        world.add_component(asteroid, sprite)

        return asteroid


class PlayerFactory(EntityFactory):
    def create(self, world: esper.World, position: Vector2):
        print("Creating player...")

        player = world.create_entity()

        #
        world.add_component(player, c.Transform(position, -90))

        #
        moveable = c.Moveable()
        moveable.drag = 0.999
        moveable.angular_drag = 0.9925
        world.add_component(player, moveable)

        #
        surface = pygame.image.load(os.path.join('assets', 'ship.png'))

        sprite = c.Sprite(surface)
        world.add_component(player, sprite)

        #
        world.add_component(player, c.Player())

        # Particles.
        emitter = c.ParticleEmitter()
        emitter.emission_rate = 50
        world.add_component(player, emitter)

        world.add_component(player, c.Camera())

        return player
