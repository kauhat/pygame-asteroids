import pygame
from pygame.math import Vector2


class Asteroid:
    def __init__(self):
        self.position: Vector2 = pygame.math.Vector2()
        self.velocity: Vector2 = pygame.math.Vector2()

        self.jitter_angle = 0
        self.jitter_amount = 10

    def tick(self, state, delta):
        # Apply velocity.
        self.position += (self.velocity * (delta / 1000))

        # Apply jitter.
        rotations_per_second = .2
        self.jitter_angle += (1000 * rotations_per_second) * (delta / 1000)

        if self.jitter_angle > 360:
            self.jitter_angle = self.jitter_angle - 360

        jitter = Vector2(self.jitter_amount, 0).rotate(
            self.jitter_angle)

        self.position += (jitter * (delta / 1000))

    def render(self, surf):
        # Cast to int 🤮
        position = (int(self.position.x), int(self.position.y))

        pygame.draw.circle(surf, (255, 255, 255), position, 10)
