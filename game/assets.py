from pygame.image import load
from pygame.math import Vector2
import random


def load_sprite(name: str, with_alpha: bool = True):
    """
    Load a sprite from assets/sprites/<name>.png.
    """
    path = f"assets/sprites/{name}.png"
    loaded_sprite = load(path)

    if with_alpha:
        return loaded_sprite.convert_alpha()
    return loaded_sprite.convert()


def wrap_position(position, surface):
    """
    Wrap a position around the screen bounds.
    """
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h)


def get_random_velocity(min_speed: int, max_speed: int):
    """
    Create a random 2D velocity vector with random heading.
    """
    speed = random.randint(min_speed, max_speed)
    angle = random.randrange(0, 360)
    return Vector2(speed, 0).rotate(angle)


def get_random_position(surface):
    """
    Create a random position inside the screen bounds.
    """
    return Vector2(
        random.randrange(surface.get_width()),
        random.randrange(surface.get_height()),
    )