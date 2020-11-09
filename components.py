from __future__ import annotations
from typing import Optional, Union

import pygame as pg
import pygame
import data


class Parent(data.CanBeDirty):
    def __init__(self, entity: int) -> None:
        self.dirty = True
        self.entity = entity


###
###
###
class Sprite:
    def __init__(self, surface: pg.Surface) -> None:
        self.base_image = surface

        self.s = pg.sprite.Sprite()
        self.s.image = self.base_image
        self.s.rect = self.base_image.get_rect()

    def __del__(self):
        self.s.kill()


class Transform(data.CanInheritFromParent):
    def __init__(self,
                 position: Optional[pg.math.Vector2] = None,
                 angle: float = 0.0) -> None:
        if position is None:
            position = pg.math.Vector2(0, 0)

        self.position = position
        self.angle = angle


class Moveable:
    def __init__(self) -> None:
        self.velocity = pg.math.Vector2()
        self.drag = 1.0

        self.angular_velocity = 0.0
        self.angular_drag = 1.0


class Collideable:
    def __init__(self, rect: pg.Rect) -> None:
        self.rect = rect


class Player:
    def __init__(self) -> None:
        self.turning_accelleration = 1000
        self.oof = 10


class ParticleEmitter:
    def __init__(self) -> None:
        self.offset = pg.math.Vector2(-35, 0)
        self.offset_angle = data.Variance(180.0, 45.0)

        self.velocity = data.Variance(50.0, 25.0)

        self.last_emission = 0
        self.emission_rate = 0
        self.emission_variance = 0
        self.particle_lifetime = data.Variance(1000, 500)


class Lifetime:
    def __init__(self, created_at: int, expire_at: int) -> None:
        self.auto_kill = True
        self.created_at = created_at
        self.expire_at = expire_at


class Camera:
    pass
