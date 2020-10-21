import os
import pygame
from pygame.math import Vector2


def rotate_center(image, rect, angle):
    """Rotate a Surface, maintaining position."""
    rot_img = pygame.transform.rotate(image, angle)
    # Get a new rect and pass the center position of the old
    # rect, so that it rotates around the center.
    rect = rot_img.get_rect(center=rect.center)
    return rot_img, rect  # Return the new rect as well.


class Entity:
    def __init__(self):
        self.components = {}

    def add_component(self, component):
        component_type = type(component)

        if component_type in self.components:
            raise "Component already exists."

        self.components[component_type] = component

    def get_component(self, component_type):
        return self.components[component_type]

    def tick(self, state, delta):
        for component in self.components:
            component.tick(self.components, state, delta)

    def init(self, state):
        pass


class BaseComponent:
    def tick(self, components, state, delta):
        pass


class SpriteComponent(BaseComponent):
    def __init__(self, surface):
        self.base_image = surface

        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = self.base_image
        self.sprite.rect = self.base_image.get_rect()
        self.sprite.rect.center = (
            self.sprite.rect.width / 2, self.sprite.rect.height / 2)

    def add_to_group(self, group):
        group.add(self.sprite)

    def tick(self, components, state, delta):
        # Update sprite if entity has transform.
        if isinstance(self, TransformComponent):
            self.sprite.image, self.sprite.rect = rotate_center(self.base_image, self.sprite.rect, self.angle)

            self.sprite.rect.y = self.position.y
            self.sprite.rect.x = self.position.x


class TransformComponent(BaseComponent):
    def __init__(self, position: Vector2 = Vector2()):
        self.position = position
        self.velocity = pygame.math.Vector2()
        self.drag = 1

        self.angle = 0
        self.angular_velocity = 0

    def tick(self, components, state, delta):
        delta_seconds = float(delta / 1000)

        # Apply drag.
        self.velocity *= (self.drag / delta_seconds)

        # Apply velocity.
        self.position += (self.velocity * delta_seconds)

        # Apply angular velocity.
        self.angle += (self.angular_velocity * delta_seconds)
        self.angle = self.angle % 360


class PlayerComponent(BaseComponent):
    def __init__(self):
        self.turning_speed = 180
        self.oof = 10

    def tick(self, components, state, delta):
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


class EntityFactory:
    def create(self, game):
        raise NotImplementedError


class AsteroidFactory(EntityFactory):
    SURFACE = pygame.image.load(os.path.join('assets', 'asteroid-64.png'))

    def create(self, game, position):
        asteroid = Entity()
        asteroid.add_component(TransformComponent(position))
        asteroid.add_component(SpriteComponent(self.SURFACE))

        return asteroid


class PlayerFactory(EntityFactory):
    SURFACE = pygame.image.load(os.path.join('assets', 'ship.png'))

    def create(self, game, position):
        player = Entity()

        transform = TransformComponent(position)
        transform.angle = -90
        transform.drag = 0.9

        player.add_component(transform)
        player.add_component(SpriteComponent(self.SURFACE))


