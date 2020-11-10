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


class EntityTreeSystem(esper.Processor):
    def __init__(self):
        pass  #self.

    def process(self, state: GameState, delta: int):
        pass


class LifetimeExpirySystem(esper.Processor):
    def __init__(self):
        pass

    def process(self, state: GameState, delta: int):
        time = pygame.time.get_ticks()

        query = self.world.get_component(c.Lifetime)
        for ent, (lifetime) in query:
            if time > lifetime.expire_at:
                if lifetime.auto_kill:
                    if self.world.has_component(ent, c.Sprite):
                        sprite = self.world.component_for_entity(ent, c.Sprite)

                    self.world.delete_entity(ent, immediate=True)
