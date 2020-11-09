import os
import copy

import esper
import pygame
from pygame.math import Vector2

import components as c


class EntityFactory:
    def __init__(self) -> None:
        self.components = []
        self.resources = {}

    @property
    def name(self):
        raise NotImplementedError

    def create(self, world: esper.World, amount=1):
        print(f"Creating {self.name} x{amount}")

        entities = []

        for i in range(amount):
            entities.append(world.create_entity())
            self.build(world, entities[-1])

        return entities

    def build(self, world: esper.World, entity: int):
        raise NotImplementedError


class AsteroidFactory(EntityFactory):
    def __init__(self) -> None:
        super().__init__()

        self.resources['surface'] = pygame.image.load(
            os.path.join('assets', 'asteroid-64.png'))

    @property
    def name(self):
        return "asteroid"

    def build(self, world: esper.World, entity: int):
        world.add_component(entity, c.Transform())
        world.add_component(entity, c.Moveable())
        world.add_component(entity, c.Sprite(self.resources['surface']))


class PlayerFactory(EntityFactory):
    def __init__(self) -> None:
        super().__init__()

        self.resources['surface'] = pygame.image.load(
            os.path.join('assets', 'ship.png'))

    @property
    def name(self):
        return "player"

    def build(self, world: esper.World, entity: int):
        world.add_component(entity, c.Transform(None, -90))

        #
        moveable = c.Moveable()
        moveable.drag = 0.999
        moveable.angular_drag = 0.9925
        world.add_component(entity, moveable)

        world.add_component(entity, c.Sprite(self.resources['surface']))
        world.add_component(entity, c.Player())

        # Particles.
        # emitter = world.create_entity()
        # world.add_component(emitter, c.Parent(entity))
        # world.add_component(emitter, c.Transform())

        # emitter_source = c.ParticleEmitter()
        # emitter_source.emission_rate = 50
        # world.add_component(emitter, emitter_source)

        #
        world.add_component(entity, c.Camera())
