from __future__ import annotations
import copy
from os.path import commonpath
from random import randrange
from typing import Optional, Union

import esper
import pygame
from pygame import Surface, Rect
from pygame.math import Vector2

import components as c
from components import Transform
from state import GameState


class ParticleEmissionSystem(esper.Processor):
    def __init__(self):
        self.count = 0
        self.poof_texture = Surface((5, 5))
        self.poof_texture.fill((255, 60, 60))

    def process(self, state: GameState, delta: int):
        time = pygame.time.get_ticks()

        query = self.world.get_components(c.ParticleEmitter, c.Transform)
        for ent, (emitter, transform) in query:
            if time > emitter.last_emission + emitter.emission_rate:
                self.emit(emitter, copy.copy(transform.position),
                          transform.angle)

    def emit(self, emitter: c.ParticleEmitter, root_pos: Vector2,
             root_angle: float):
        particle = self.world.create_entity()

        #
        self.world.add_component(particle, c.Sprite(self.poof_texture))

        #
        position = root_pos + (emitter.offset.rotate(root_angle))

        angle_offset = emitter.offset_angle.get_float()
        angle = root_angle + angle_offset

        transform = c.Transform(position, angle)
        self.world.add_component(particle, transform)

        #
        moveable = c.Moveable()
        moveable.velocity.x = emitter.velocity.get_float()
        moveable.velocity.rotate_ip(transform.angle)

        self.world.add_component(particle, moveable)

        #
        created_at = pygame.time.get_ticks()
        expire_at = created_at + emitter.particle_lifetime.get_int()

        lifetime = c.Lifetime(created_at, expire_at)
        self.world.add_component(particle, c.Lifetime(created_at, expire_at))

        self.count += 1

        emitter.last_emission = created_at
