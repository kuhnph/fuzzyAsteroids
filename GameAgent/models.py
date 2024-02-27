# Importing necessary modules
from pygame.math import Vector2            # Importing the Vector2 class for 2D vectors
from pygame.transform import rotozoom      # Importing rotozoom for rotating sprites
from pygame.font import Font
from utils import load_sprite, get_random_position, get_random_velocity, wrap_position  # Custom utility functions

# Defining a vector representing upwards direction
UP = Vector2(0, -1)

# Base class representing a generic game object
class GameObject:
    def __init__(self, position, sprite, velocity):
        # Initializing object's attributes
        self.position = Vector2(position)  # Position vector
        self.sprite = sprite                # Image representing the object
        self.radius = sprite.get_width() / 2  # Radius for collision detection
        self.velocity = Vector2(velocity)  # Velocity vector

    # Method to draw the object on a surface
    def draw(self, surface):
        # Calculating position for blitting to center the sprite
        blit_position = self.position - Vector2(self.radius)
        # Blitting the sprite onto the surface
        surface.blit(self.sprite, blit_position)

    # Method to move the object
    def move(self, surface):
        # Wrapping position around the screen if it goes out of bounds
        self.position = wrap_position(self.position + self.velocity, surface)
        # Updating position based on velocity
        self.position += self.velocity

    def move_no_wrap(self):
        # Wrapping position around the screen if it goes out of bounds
        self.position = self.position + self.velocity
        # Updating position based on velocity
        self.position += self.velocity

    # Method to check collision with another object
    def collides_with(self, other_obj):
        # Calculating distance between this object and another object
        distance = self.position.distance_to(other_obj.position)
        # Checking if the distance is less than the sum of the radii for collision
        return distance < self.radius + other_obj.radius
    
    # position getter
    @property
    def position(self):
        return self._position
    # position setter
    @position.setter
    def position(self, p):
        self._position = p

# Subclass representing a spaceship, inheriting from GameObject
class Spaceship(GameObject):
    MANEUVERABILITY = 5   # Rate of rotation
    ACCELERATION = .1     # Acceleration rate
    BULLET_SPEED = 3      # Speed of bullets fired from the spaceship
    DAMPENING = .01

    def __init__(self, position, create_bullet_callback):
        # Initializing spaceship attributes
        self.create_bullet_callback = create_bullet_callback
        self.direction = Vector2(UP)  # Current direction the spaceship is facing
        super().__init__(position, load_sprite("ship"), Vector2(0))  # Calling base class constructor

    # Method to rotate the spaceship
    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    # Method to draw the rotated spaceship
    def draw(self, surface):
        # Calculating angle between spaceship's direction and upwards direction
        angle = self.direction.angle_to(UP)
        # Rotating the sprite according to the angle
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        # Getting size of rotated sprite
        rotated_surface_size = Vector2(rotated_surface.get_size())
        # Calculating blit position to center the rotated sprite
        blit_position = self.position - rotated_surface_size * 0.5
        # Blitting the rotated sprite onto the surface
        surface.blit(rotated_surface, blit_position)

    # Method to accelerate the spaceship
    def accelerate(self, ACCELERATION=ACCELERATION):
        # Updating velocity based on direction and acceleration rate
        self.velocity += self.direction * ACCELERATION - self.velocity*self.DAMPENING

    # Method to shoot bullets from the spaceship
    def shoot(self):
        # Calculating velocity for the bullet
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
        # Creating a new bullet object at spaceship's position with calculated velocity
        bullet = Bullet(self.position, bullet_velocity)
        # Calling a callback function to handle the created bullet
        self.create_bullet_callback(bullet)



# Subclass representing an asteroid, inheriting from GameObject
class Asteroid(GameObject):
    def __init__(self, position, create_asteroid_callback, size=3):
        self.create_asteroid_callback = create_asteroid_callback
        self.size = size    #initialize the size of the asteroids

        #define asteroid scales
        size_to_scale = {
            3: 1,
            2: .5,
            1: .25
        }
        scale = size_to_scale[size] #initialize asteroid scale
        sprite = rotozoom(load_sprite('asteroid'),0,scale) #uses the rotozoom class to scale the sprite


        # Initializing asteroid attributes
        super().__init__(
            position, sprite, get_random_velocity(1, 3)
        )

    #method for splitting asteroids
    def split(self):
        if self.size > 1:
            for _ in range(2):
                asteroid = Asteroid(
                    self.position, self.create_asteroid_callback, self.size-1
                )
                self.create_asteroid_callback(asteroid)

# Subclass representing a bullet, inheriting from GameObject
class Bullet(GameObject):
    def __init__(self, position, velocity):
        # Initializing bullet attributes
        super().__init__(position, load_sprite('bullet'), velocity)


# Subclass representing a spaceship, inheriting from GameObject
class Peach(GameObject):
    '''
    Made Peach half as maneuverable and fast as Spaceship Class.
    This way, Peach has need for 
    '''
    MANEUVERABILITY = 2.5      # Rate of rotation
    ACCELERATION    = .05     # Acceleration rate
    DAMPENING       = .01

    def __init__(self, position):
        # Initializing spaceship attributes
        self.direction = Vector2(UP)  # Current direction the spaceship is facing
        super().__init__(position, load_sprite("spaceship"), Vector2(0))  # Calling base class constructor

    # Method to rotate the spaceship
    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    # Method to draw the rotated spaceship
    def draw(self, surface):
        # Calculating angle between spaceship's direction and upwards direction
        angle = self.direction.angle_to(UP)
        # Rotating the sprite according to the angle
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        # Getting size of rotated sprite
        rotated_surface_size = Vector2(rotated_surface.get_size())
        # Calculating blit position to center the rotated sprite
        blit_position = self.position - rotated_surface_size * 0.5
        # Blitting the rotated sprite onto the surface
        surface.blit(rotated_surface, blit_position)

    # Method to accelerate the spaceship
    def accelerate(self, ACCELERATION=ACCELERATION):
        # Updating velocity based on direction and acceleration rate
        self.velocity += self.direction * ACCELERATION - self.velocity*self.DAMPENING


class Target(GameObject):
    def __init__(self, position, capture_life):
        self.capture_life = capture_life
        # initialize target attributes
        self.sprite = rotozoom(load_sprite('target'),0,0.5)
        super().__init__(position, self.sprite , Vector2(0))  # Calling base class constructor

    # Method to draw the target
    def draw(self, surface):
        # Calculating position for blitting to center the sprite
        blit_position = self.position - Vector2(self.radius)
        # draw teh capture life
        text_to_screen(surface, '{:.1f}'.format(self.capture_life), (blit_position[0], blit_position[1]-20))
        # Blitting the sprite onto the surface
        surface.blit(self.sprite, blit_position)

    # capture function
    def capture(self):
        self.capture_life -= 0.1

    # damsel getter
    @property
    def damsel(self):
        return self._damsel
    # damsel setter
    @damsel.setter
    def damsel(self, d):
        self._damsel = d #eez nuts
    
def text_to_screen(surface, text, pos, size = 20, color = 'white', font_type = 'assets/fonts/ubuntu.mono.ttf'):
    try:
        text = str(text)
        font = Font(font_type, size)
        text = font.render(text, True, color)
        surface.blit(text, pos)

    except Exception as e:
        print('Font Error in text_to_screen, oopsie poopsie')
        raise e