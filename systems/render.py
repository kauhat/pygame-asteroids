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

from transform import TransformChain
import image

class SpriteRenderSystem(esper.Processor):
    def __init__(self, window: Surface):
        self.render_group: pygame.sprite.Group = pygame.sprite.RenderPlain()
        self.window = window

    def get_camera_transform(self) -> c.Transform:
        # Get camera position.
        camera_list = self.world.get_components(c.Camera, c.Transform)

        if len(camera_list) > 0:
            ent, (camera, transform) = camera_list[0]
            return transform

        raise RuntimeError("No camera in world.")

    def process(self, state: GameState, delta: int):
        # Clear the screen.
        self.window.fill((0, 0, 0))

        camera_transform = copy.deepcopy(self.get_camera_transform())
        camera_transform.position = camera_transform.position / -2
        camera_transform.angle = camera_transform.angle * -1

        window_transform = c.Transform(Vector2(self.window.get_size()) / 4)

        #
        query = self.world.get_components(c.Sprite, c.Transform)
        for ent, (sprite, transform) in query:

            chain = TransformChain()

            # TODO: Fix this

            #screenspace = chain.stack(
            #    [window_transform, camera_transform, transform])

            worldspace = chain.stack([transform])
            screenspace = c.Transform(
                worldspace.position + window_transform.position, 0)

            #
            sprite.s.image, sprite.s.rect = image.rotate_center(
                sprite.base_image, sprite.s.rect, -worldspace.angle)

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
