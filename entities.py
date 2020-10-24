import os

import esper
import pygame
from pygame.math import Vector2

from components import Transform, Moveable, Sprite, Player


class EntityFactory:
    def create(self, world: esper.World):
        raise NotImplementedError


class AsteroidFactory(EntityFactory):
    def create(self, world: esper.World, position: Vector2):
        print("Creating asteroid...")

        asteroid = world.create_entity()

        #
        world.add_component(asteroid, Transform(position))

        #
        moveable = Moveable()
        world.add_component(asteroid, moveable)

        #
        surface = pygame.image.load(os.path.join('assets', 'asteroid-64.png'))

        sprite = Sprite(surface)
        world.add_component(asteroid, sprite)

        return asteroid


class PlayerFactory(EntityFactory):
    def create(self, world: esper.World, position: Vector2):
        print("Creating player...")

        player = world.create_entity()

        #
        world.add_component(player, Transform(position, -90))

        #
        moveable = Moveable()
        moveable.drag = 0.999
        moveable.angular_drag = 0.99
        world.add_component(player, moveable)

        #
        surface = pygame.image.load(os.path.join('assets', 'ship.png'))

        sprite = Sprite(surface)
        world.add_component(player, sprite)

        #
        world.add_component(player, Player())

        return player
