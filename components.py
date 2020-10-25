from __future__ import annotations

import random
from typing import Union

import pygame
from pygame import Surface, Rect
from pygame.math import Vector2

class Variance:
    def __init__(self, base: float, variance: float):
        self.base = base
        self.variance = variance

    def get_float(self):
        result = self.base

        if self.variance > 0.0:
            result += random.uniform(-self.variance, +self.variance)

        return result

    def get_int(self):
        result = int(self.base)

        variance = int(self.variance)
        if variance > 0:
            result += random.randrange(-variance, +variance)

        return result

###
###
###
class Sprite:
    def __init__(self, surface: Surface):
        self.base_image = surface

        self.s = pygame.sprite.Sprite()
        self.s.image = self.base_image
        self.s.rect = self.base_image.get_rect()

    def __del__(self):
        self.s.kill()


class Transform:
    def __init__(self, position=Vector2(), angle: float = 0.0):
        self.position = position
        self.angle = angle

    def __add__(self, other: Transform):
        pos = self.position + other.position
        angle = self.angle + other.angle

        return Transform(pos, angle)

    def __sub__(self, other: Transform):
        pos = self.position - other.position
        angle = self.angle - other.angle

        return Transform(pos, angle)


class Moveable:
    def __init__(self):
        self.velocity = Vector2()
        self.drag = 1.0

        self.angular_velocity = 0.0
        self.angular_drag = 1.0


class Collideable:
    def __init__(self, rect: Rect):
        self.rect = rect


class Player:
    def __init__(self):
        self.turning_accelleration = 1000
        self.oof = 10

class ParticleEmitter:
    def __init__(self):
        self.offset = Vector2(-35, 0)
        self.offset_angle = Variance(180.0, 45.0)

        self.velocity = Variance(50.0, 25.0)

        self.last_emission = 0
        self.emission_rate = 0
        self.emission_variance = 0
        self.particle_lifetime = Variance(1000, 500)


class Lifetime:
    def __init__(self, created_at: int, expire_at: int):
        self.auto_kill = True
        self.created_at = created_at
        self.expire_at = expire_at

class Camera:
    pass
