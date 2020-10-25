import copy
from os.path import commonpath
from random import randrange

import esper
import pygame
from pygame import Surface, Rect
from pygame.math import Vector2

import components as c
from state import GameState


def rotate_center(image: Surface, rect: Rect, angle):
    """Rotate a Surface, maintaining position."""
    rot_img = pygame.transform.rotate(image, angle)
    # Get a new rect and pass the center position of the old
    # rect, so that it rotates around the center.
    rect = rot_img.get_rect(center=rect.center)
    return rot_img, rect  # Return the new rect as well.


class ParticleEmissionSystem(esper.Processor):
    def __init__(self):
        self.count = 0
        self.poof_texture = Surface((5,5))
        self.poof_texture.fill((255,60,60))

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



class SpriteRenderSystem(esper.Processor):
    def __init__(self, window: Surface):
        self.render_group: pygame.sprite.Group = pygame.sprite.RenderPlain()
        self.window = window

    def get_camera_transform(self) -> Vector2:
        # Get camera position.
        camera_list = self.world.get_components(c.Camera, c.Transform)
        if len(camera_list) > 0:
            ent, (camera, transform) = camera_list[0]
            return transform

        raise RuntimeError("No camera in world.")

    def process(self, state: GameState, delta: int):
        # Clear the screen.
        self.window.fill((0, 0, 0))

        camera_transform = self.get_camera_transform()
        window_transform = c.Transform(Vector2(self.window.get_size()) / 2)

        #
        query = self.world.get_components(c.Sprite, c.Transform)
        for ent, (sprite, transform) in query:
            sprite.s.image, sprite.s.rect = rotate_center(
                sprite.base_image, sprite.s.rect, -transform.angle)

            screenspace = transform - camera_transform + window_transform

            sprite.s.rect.centerx = screenspace.position.x
            sprite.s.rect.centery = screenspace.position.y

            self.render_group.add(sprite.s)

        self.render_group.draw(self.window)

        #
        pygame.display.flip()


# TODO: Finish this.
class BlitterRenderSystem(esper.Processor):
    def __init__(self, window: Surface):
        self.render_group: pygame.sprite.Group = pygame.sprite.RenderPlain()
        self.window = window

    def process(self, state: GameState, delta: int):
        # Clear the screen.
        self.window.fill((0, 0, 0))

        #
        query = self.world.get_components(c.Sprite, c.Transform)
        for ent, (sprite, transform) in query:
            sprite.s.image, sprite.s.rect = rotate_center(
                sprite.base_image, sprite.s.rect, -transform.angle)

            sprite.s.rect.centerx = transform.position.x
            sprite.s.rect.centery = transform.position.y

            self.render_group.add(sprite.s)

        self.render_group.draw(self.window)

        #
        pygame.display.flip()


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
