import esper
import pygame
from pygame import Surface, Rect
from pygame.math import Vector2

from components import Transform, Moveable, Sprite, Player
from state import GameState


def rotate_center(image: Surface, rect: Rect, angle):
    """Rotate a Surface, maintaining position."""
    rot_img = pygame.transform.rotate(image, angle)
    # Get a new rect and pass the center position of the old
    # rect, so that it rotates around the center.
    rect = rot_img.get_rect(center=rect.center)
    return rot_img, rect  # Return the new rect as well.


class SpriteRenderSystem(esper.Processor):
    def __init__(self, window: Surface) -> None:
        self.render_group: pygame.sprite.Group = pygame.sprite.RenderPlain()
        self.window = window

    def process(self, state: GameState, delta: int):
        # Clear the screen.
        self.window.fill((0, 0, 0))

        #
        query = self.world.get_components(Sprite, Transform)
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

        query = self.world.get_components(Transform, Moveable)
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

        query = self.world.get_components(Player, Transform, Moveable)
        for ent, (player, transform, moveable) in query:
            # Apply rotation.
            moveable.angular_velocity += turning_impulse * (
                player.turning_accelleration * delta_seconds)

            # Apply oomph.
            direction = Vector2(1, 0).rotate(transform.angle)

            speed = player.oof * engine_impulse * direction

            moveable.velocity += speed
