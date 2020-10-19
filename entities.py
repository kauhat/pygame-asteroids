import os
import pygame
from pygame.math import Vector2


class BaseEntity:
    def tick(self, state, delta):
        raise NotImplementedError

    def init(self, state):
        pass


class SpriteComponent:
    def __init__(self, surface):
        self.base_image = surface

        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = self.base_image
        self.sprite.rect = self.base_image.get_rect()
        self.sprite.rect.center = (
            self.sprite.rect.width / 2, self.sprite.rect.height / 2)

    def add_to_group(self, group):
        group.add(self.sprite)

    def init(self, state):
        pass

    def tick(self, state, delta):
        # Update sprite if entity has transform.
        if isinstance(self, TransformComponent):
            self.sprite.image = pygame.transform.rotate(
                self.base_image, self.angle)

            self.sprite.rect.x = self.position.x
            self.sprite.rect.y = self.position.y


class TransformComponent:
    def __init__(self):
        self.position = pygame.math.Vector2()
        self.velocity = pygame.math.Vector2()
        self.drag = 1

        self.angle = 0
        self.angular_velocity = 0

    def tick(self, state, delta):
        delta_seconds = float(delta / 1000)

        # Apply drag.
        self.velocity = self.velocity * self.drag

        # Apply velocity.
        self.position += (self.velocity * delta_seconds)

        # Apply angular velocity.
        self.angle += (self.angular_velocity * delta_seconds)
        self.angle = self.angle % 360


class Asteroid(BaseEntity, SpriteComponent, TransformComponent):
    SURFACE = pygame.image.load(os.path.join('assets', 'asteroid-64.png'))

    def __init__(self):
        TransformComponent.__init__(self)
        SpriteComponent.__init__(self, self.SURFACE)

    def tick(self, state, delta):
        TransformComponent.tick(self, state, delta)
        SpriteComponent.tick(self, state, delta)

        delta_seconds = (delta / 1000)


class Player(BaseEntity, SpriteComponent, TransformComponent):
    SURFACE = pygame.image.load(os.path.join('assets', 'asteroid.png'))

    def __init__(self):
        TransformComponent.__init__(self)
        SpriteComponent.__init__(self, self.SURFACE)

        self.position: Vector2 = pygame.math.Vector2()
        self.angle = -90

        self.velocity: Vector2 = pygame.math.Vector2()
        self.drag = 0.99

        self.oof = 1
        self.turning_speed = 180

    def tick(self, state, delta):
        TransformComponent.tick(self, state, delta)
        SpriteComponent.tick(self, state, delta)

        delta_seconds = (delta / 1000)

        engine_impulse = state.input.player_forward - state.input.player_back
        turning_impulse = state.input.player_turn_right - state.input.player_turn_left

        # Apply rotation.
        self.angular_velocity = turning_impulse * self.turning_speed
        # print(self.angle)

        # Apply oomph.
        direction = Vector2(1, 0).rotate(self.angle)

        speed = (self.oof * engine_impulse) * direction

        self.velocity += speed

        #
        self.position += self.velocity * delta_seconds
