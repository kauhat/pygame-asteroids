import pygame
from pygame import Surface, Rect
from pygame.math import Vector2


class Sprite:
    def __init__(self, surface: Surface):
        self.base_image = surface

        self.s = pygame.sprite.Sprite()
        self.s.image = self.base_image
        self.s.rect = self.base_image.get_rect()


class Transform:
    def __init__(self, position=Vector2()):
        self.position = position
        self.angle: float = 0


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
