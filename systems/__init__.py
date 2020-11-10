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



class MovementSystem(esper.Processor):
    def process(self, state: GameState, delta: int):
        delta_seconds = (delta / 1000)

        query = self.world.get_components(c.Transform, c.Moveable)
        for ent, (transform, moveable) in query:
            # Apply drag.
            moveable.velocity *= pow(moveable.drag, delta)

            # Apply angular drag.
            moveable.angular_velocity *= pow(moveable.angular_drag, delta)

            # Apply velocity.
            transform.position += (moveable.velocity * delta_seconds)

            # Apply angular velocity.
            transform.angle += (moveable.angular_velocity * delta_seconds)
            transform.angle = transform.angle % 360


class PlayerControlSystem(esper.Processor):
    def process(self, state: GameState, delta: int):
        delta_seconds = (delta / 1000)

        engine_impulse = state.input.player_forward - state.input.player_back
        turning_impulse = state.input.player_turn_right - state.input.player_turn_left

        query = self.world.get_components(c.Player, c.Transform, c.Moveable)
        for ent, (player, transform, moveable) in query:
            # Apply rotation.
            moveable.angular_velocity += turning_impulse * (
                player.turning_accelleration * delta_seconds)

            # Apply oomph.
            direction = Vector2(1, 0).rotate(transform.angle)

            speed = player.oof * engine_impulse * direction

            moveable.velocity += speed
