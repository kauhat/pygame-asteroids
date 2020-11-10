import pygame
from pygame import Surface, Rect
from pygame.math import Vector2

def rotate_center(image: Surface, rect: Rect, angle):
    """Rotate a Surface, maintaining position."""
    rot_img = pygame.transform.rotate(image, angle)

    # Get a new rect and pass the center position of the old
    # rect, so that it rotates around the center.
    rect = rot_img.get_rect(center=rect.center)
    return rot_img, rect  # Return the new rect as well.
