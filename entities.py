import os
import pygame
from pygame import transform
from pygame.math import Vector2
from pygame.sprite import Sprite, Group

import state
import game
from game import BaseGame


def rotate_center(image: pygame.Surface, rect, angle):
    """Rotate a Surface, maintaining position."""
    rot_img = pygame.transform.rotate(image, angle)
    # Get a new rect and pass the center position of the old
    # rect, so that it rotates around the center.
    rect = rot_img.get_rect(center=rect.center)
    return rot_img, rect  # Return the new rect as well.


class BaseComponent:
    def tick(self, components, state: state.GameState, delta):
        pass

    def key(self):
        return type(self)


class Entity:
    def __init__(self):
        self.components = {}

    def tick(self, state: state.GameState, delta: int):
        for component in self.components.values():
            if not isinstance(component, BaseComponent):
                raise ValueError("Instance is not component")

            component.tick(self.components, state, delta)

    def init(self, state: state.GameState):
        pass

    def add_component(self, component):
        if not isinstance(component, BaseComponent):
            raise ValueError("Instance is not component")

        #
        component_type = component.key()

        if component_type in self.components:
            raise KeyError("Component already exists for entity.")

        #
        self.components[component_type] = component

    def get_component(self, component_type):
        if not component_type in self.components:
            raise KeyError("Component does not exist.")

        return self.components[component_type]


class SpriteComponent(BaseComponent):
    def __init__(self, surface: pygame.Surface):
        self.base_image = surface

        self.sprite = Sprite()
        self.sprite.image = self.base_image
        self.sprite.rect = self.base_image.get_rect()
        # self.sprite.rect.center = (int(self.sprite.rect.width / 2),
        #                            int(self.sprite.rect.height / 2))

    def add_to_group(self, group):
        group.add(self.sprite)

    def tick(self, components, state: state.GameState, delta: int):
        # Update sprite if entity has transform.
        if TransformComponent in components:
            transform = components[TransformComponent]

            #
            self.sprite.image, self.sprite.rect = rotate_center(
                self.base_image, self.sprite.rect, -transform.angle)

            self.sprite.rect.centerx = transform.position.x
            self.sprite.rect.centery = transform.position.y


class TransformComponent(BaseComponent):
    def __init__(self, position: Vector2 = Vector2()):

        self.position = position
        self.velocity = pygame.math.Vector2()
        self.drag = 1.0

        self.angle = 0.0
        self.angular_velocity = 0.0
        self.angular_drag = 1.0

    def tick(self, components, state: state.GameState, delta):
        delta_seconds = float(delta / 1000)

        # Apply drag.
        self.velocity *= pow(self.drag, delta)

        # Apply angular drag.
        self.angular_velocity *= pow(self.angular_drag, delta)

        # Apply velocity.
        self.position += (self.velocity * delta_seconds)

        # Apply angular velocity.
        self.angle += (self.angular_velocity * delta_seconds)
        self.angle = self.angle % 360


class PlayerControlComponent(BaseComponent):
    def __init__(self):
        self.turning_accelleration = 1000
        self.oof = 10

    def tick(self, components, state: state.GameState, delta):
        delta_seconds = (delta / 1000)

        engine_impulse = state.input.player_forward - state.input.player_back
        turning_impulse = state.input.player_turn_right - state.input.player_turn_left

        transform = components[TransformComponent]

        # Apply rotation.
        transform.angular_velocity += turning_impulse * (
            self.turning_accelleration * delta_seconds)

        # Apply oomph.
        direction = Vector2(1, 0).rotate(transform.angle)

        speed = self.oof * engine_impulse * direction

        transform.velocity += speed


class EntityFactory:
    def create(self, game):
        raise NotImplementedError


class AsteroidFactory(EntityFactory):
    def create(self, game: BaseGame, group: Group, position: Vector2):
        print("Creating asteroid...")

        asteroid = Entity()

        #
        asteroid.add_component(TransformComponent(position))

        #
        surface = pygame.image.load(os.path.join('assets', 'asteroid-64.png'))

        sprite = SpriteComponent(surface)
        sprite.add_to_group(group)
        asteroid.add_component(sprite)

        return asteroid


class PlayerFactory(EntityFactory):
    def create(self, game: BaseGame, group: Group, position: Vector2):
        print("Creating player...")

        player = Entity()

        #
        transform = TransformComponent(position)
        transform.drag = 0.999
        transform.angular_drag = 0.99
        player.add_component(transform)

        #
        surface = pygame.image.load(os.path.join('assets', 'ship.png'))

        sprite = SpriteComponent(surface)
        sprite.add_to_group(group)
        player.add_component(sprite)

        #
        player.add_component(PlayerControlComponent())

        return player
