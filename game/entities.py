from pygame.math import Vector2
from pygame.transform import rotozoom
from pygame.font import Font
import os
# import sys
# rootPath = os.path.dirname(os.path.dirname(__file__))
# sys.path.append(rootPath)

from .assets import load_sprite, get_random_velocity, wrap_position


UP = Vector2(0, -1)
RIGHT = Vector2(1, 0)


class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface):
        """
        Move with screen wrapping.
        """
        self.position = wrap_position(self.position + self.velocity, surface)

    def move_no_wrap(self):
        """
        Move without screen wrapping.
        """
        self.position = self.position + self.velocity

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius


class Spaceship(GameObject):
    MANEUVERABILITY = 5
    ACCELERATION = 0.1
    BULLET_SPEED = 3
    DAMPENING = 0.01

    def __init__(self, position, create_bullet_callback):
        self.create_bullet_callback = create_bullet_callback
        self.direction = Vector2(UP)
        super().__init__(position, load_sprite("ship"), Vector2(0, 0))

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def accelerate(self, acceleration=None):
        if acceleration is None:
            acceleration = self.ACCELERATION
        self.velocity += self.direction * acceleration - self.velocity * self.DAMPENING

    def shoot(self):
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
        bullet = Bullet(self.position, bullet_velocity)
        self.create_bullet_callback(bullet)


class Peach(GameObject):
    """
    AI-controlled capture agent.
    Slightly less maneuverable than the player ship.
    """
    MANEUVERABILITY = 2.5
    ACCELERATION = 0.05
    DAMPENING = 0.01

    def __init__(self, position):
        self.direction = Vector2(RIGHT)
        super().__init__(position, load_sprite("spaceship"), Vector2(0, 0))

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def accelerate(self, acceleration=None):
        if acceleration is None:
            acceleration = self.ACCELERATION
        self.velocity += self.direction * acceleration - self.velocity * self.DAMPENING


class Asteroid(GameObject):
    def __init__(self, position, create_asteroid_callback, size=3):
        self.create_asteroid_callback = create_asteroid_callback
        self.size = size

        size_to_scale = {
            3: 1.0,
            2: 0.5,
            1: 0.25,
        }

        scale = size_to_scale[size]
        sprite = rotozoom(load_sprite("asteroid"), 0, scale)

        super().__init__(position, sprite, get_random_velocity(1, 3))

    def split(self):
        if self.size > 1:
            for _ in range(2):
                asteroid = Asteroid(
                    self.position,
                    self.create_asteroid_callback,
                    self.size - 1
                )
                self.create_asteroid_callback(asteroid)


class Bullet(GameObject):
    def __init__(self, position, velocity):
        super().__init__(position, load_sprite("bullet"), velocity)


class Target(GameObject):
    def __init__(self, position, capture_life):
        self.capture_life = capture_life
        sprite = rotozoom(load_sprite("target"), 0, 0.5)
        super().__init__(position, sprite, Vector2(0, 0))

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        text_to_screen(
            surface,
            f"{self.capture_life:.1f}",
            (blit_position[0], blit_position[1] - 20),
        )
        surface.blit(self.sprite, blit_position)

    def capture(self):
        self.capture_life -= 0.1


def text_to_screen(
    surface,
    text,
    pos,
    size=20,
    color="white",
    font_type=os.path.join('assets','fonts','ubuntu.mono.ttf'),
):
    """
    Draw text to the pygame surface.
    """
    try:
        text = str(text)
        font = Font(font_type, size)
        rendered = font.render(text, True, color)
        surface.blit(rendered, pos)
    except Exception as exc:
        print("Font Error in text_to_screen")
        raise exc