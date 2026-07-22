from pygame.math import Vector2
from pygame.transform import rotozoom
from pygame.font import Font
from .assets import load_sprite, get_random_velocity, wrap_position
from .settings import GameSettings


UP = Vector2(0, -1)
RIGHT = Vector2(1, 0)
#Single unmoving asteroid case
TEST = True


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
    MANEUVERABILITY = GameSettings.SPACESHIP_MANEUVERABILITY
    ACCELERATION = GameSettings.SPACESHIP_ACCELERATION
    BULLET_SPEED = GameSettings.SPACESHIP_BULLET_SPEED
    DAMPENING = GameSettings.SPACESHIP_DAMPENING

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
    capture agent.
    Slightly less maneuverable than the player ship.
    """
    MANEUVERABILITY = GameSettings.PEACH_MANEUVERABILITY
    ACCELERATION = GameSettings.PEACH_ACCELERATION
    DAMPENING = GameSettings.PEACH_DAMPENING

    def __init__(self, position):
        self.direction = Vector2(RIGHT)

        #Single unmoving asteroid case
        if not TEST:
            super().__init__(position, load_sprite("spaceship"), Vector2(0, 0))
        else:
            super().__init__((GameSettings.SCREEN_WIDTH/2-200,GameSettings.SCREEN_HEIGHT/2), load_sprite("spaceship"), Vector2(0, 0))

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5  #Calculate upper left corner
        surface.blit(rotated_surface, blit_position)

    def accelerate(self, acceleration=None):
        if acceleration is None:
            acceleration = self.ACCELERATION
        self.velocity += self.direction * acceleration - self.velocity * self.DAMPENING

class Asteroid(GameObject):
    def __init__(self, position, create_asteroid_callback, size=GameSettings.ASTEROID_START_SIZE):
        self.create_asteroid_callback = create_asteroid_callback
        self.size = size

        scale = GameSettings.ASTEROID_SIZE_TO_SCALE[size]
        sprite = rotozoom(load_sprite("asteroid"), 0, scale)

        #Testing stuff
        if not TEST:
            super().__init__(
                position,
                sprite,
                get_random_velocity(GameSettings.ASTEROID_MIN_SPEED, GameSettings.ASTEROID_MAX_SPEED),
            )
        #Single unmoving asteroid case
        else:
            super().__init__(
                Vector2(GameSettings.SCREEN_WIDTH/2, GameSettings.SCREEN_HEIGHT/2),
                sprite,
                (0,0),
            )


    def split(self):
        if self.size > 1:
            for _ in range(GameSettings.ASTEROID_SPLIT_COUNT):
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
        sprite = rotozoom(load_sprite("target"), 0, GameSettings.TARGET_SCALE)

        #Single unmoving asteroid case
        if not TEST:
            super().__init__(position, sprite, Vector2(0, 0))
        else:
            super().__init__((GameSettings.SCREEN_WIDTH/2+200,GameSettings.SCREEN_HEIGHT/2), sprite, Vector2(0, 0))

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        text_to_screen(
            surface,
            f"{self.capture_life:.1f}",
            (blit_position[0], blit_position[1] - GameSettings.TARGET_LABEL_OFFSET_Y),
        )
        surface.blit(self.sprite, blit_position)

    def capture(self):
        self.capture_life -= GameSettings.CAPTURE_DECREMENT


# class PseudoTarget:
#     def __init__(self, position):
#         self.position = Vector2(position)

#     def set_position(self, position):
#         self.position.update(position)

#     def draw(self, surface):
#         # Optional visual marker for debugging
#         pygame.draw.circle(
#             surface,
#             "yellow",
#             self.position,
#             6,
#             width=2,
#         )


def text_to_screen(
    surface,
    text,
    pos,
    size=GameSettings.FONT_SIZE,
    color=GameSettings.FONT_COLOR,
    font_type=GameSettings.FONT_PATH,
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
