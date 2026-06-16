import pygame
import random
from pygame.math import Vector2

from .entities import Spaceship, Peach, Asteroid, Bullet, Target
from .assets import load_sprite, get_random_position
from .input_handlers import handle_manual_input, apply_agent_actions


class SpaceRocks:
    MIN_ASTEROID_DISTANCE = 250
    SCREEN_WIDTH = int(1920/1.5)
    SCREEN_HEIGHT = int(1080/1.5)
    max_train_ticks = 2000
    START_CAPTURE_LIFE = 10
    margin = 20
    PEACH_POSITION = (random.uniform(margin, SCREEN_WIDTH - margin), random.uniform(margin, SCREEN_HEIGHT - margin))
    TARGET_POSITION = (random.uniform(margin, SCREEN_WIDTH - margin), random.uniform(margin, SCREEN_HEIGHT - margin))

    def __init__(self, user_input=True, enable_player=False, render=True, fps=1000):
        """
        Parameters
        ----------
        user_input : bool
            If True, manual keyboard input is used.
            If False, actions must be passed into play_step().
        enable_player : bool
            If True, spawn the player spaceship.
            If False, only Peach exists.
        """
        #Game stuffs
        self.user_input = user_input
        self.enable_player = enable_player
        self.render = render
        self.fps = fps

        self._init_pygame()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.background = load_sprite("space", with_alpha=False)
        self.clock = pygame.time.Clock()

        self.asteroids = []
        self.bullets = []

        self.spaceship = (
            Spaceship((400, 300), self.bullets.append)
            if self.enable_player
            else None
        )

        self.peach = Peach(self.PEACH_POSITION)
        self.capture_agents = [self.peach]

        self.target = Target(self.TARGET_POSITION, self.START_CAPTURE_LIFE)

        # Training / episode bookkeeping
        self.ticks = 0
        self.current_life = self.START_CAPTURE_LIFE
        self.RESET = False

        # You currently initialize with zero asteroids in the newer file.
        # Keep that behavior for now.
        self.spawn_initial_asteroids(count=0)

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Space Rocks")

    def spawn_initial_asteroids(self, count=1):
        for _ in range(count):
            while True:
                position = get_random_position(self.screen)

                far_from_ship = (
                    True if self.spaceship is None
                    else position.distance_to(self.spaceship.position) > self.MIN_ASTEROID_DISTANCE
                )
                far_from_peach = (
                    True if self.peach is None
                    else position.distance_to(self.peach.position) > self.MIN_ASTEROID_DISTANCE
                )

                if far_from_ship and far_from_peach:
                    break

            self.asteroids.append(Asteroid(position, self.asteroids.append))

    def reset_episode(self):
        """
        Soft reset for training.
        """
        peach_initial_position = self.random_position_away()
        target_initial_position = self.random_position_away()
        self.initial_position_error = target_initial_position.distance_to(peach_initial_position)

        self.peach = Peach(peach_initial_position)
        self.capture_agents = [self.peach]
        self.target = Target(target_initial_position, self.START_CAPTURE_LIFE)

        self.asteroids = []
        self.bullets = []

        self.spaceship = (
            Spaceship((400, 300), self.bullets.append)
            if self.enable_player
            else None
        )

        self.ticks = 0
        self.current_life = self.START_CAPTURE_LIFE
        self.RESET = False

    def play_step(self, ship_actions=None, peach_actions=None):
        """
        Advance the game by one frame.
        """
        if self.user_input:
            handle_manual_input(self)
        else:
            apply_agent_actions(self, ship_actions, peach_actions)

        self._process_game_logic()

        #only render if I wanna
        if self.render:
            self._draw()

    def move_target_if_captured(self):
        """
        When the target is fully captured, move it to a new random spot
        and reset capture life.
        """
        if self.current_life < 0:
            self.target = Target(get_random_position(self.screen), self.START_CAPTURE_LIFE)

    def _process_game_logic(self):
        # Move all active game objects
        for game_object in self._get_game_objects():
            if isinstance(game_object, Bullet):
                game_object.move_no_wrap()
            else:
                game_object.move(self.screen)

        # Dampen ship drift if active
        if self.spaceship is not None:
            self.spaceship.accelerate(0)
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship):
                    self.spaceship = None
                    break

        # Capture logic
        for capture_agent in self.capture_agents:
            if capture_agent is not None and capture_agent.collides_with(self.target):
                self.target.capture()

        # Peach collision logic
        if self.peach is not None:
            self.peach.accelerate(0)

            for asteroid in self.asteroids:
                if asteroid.collides_with(self.peach):
                    self.peach = None
                    break

            if self.peach is not None:
                for bullet in self.bullets:
                    if bullet.collides_with(self.peach):
                        self.peach = None
                        break

        # Ship / Peach collision
        if self.peach is not None and self.spaceship is not None:
            if self.spaceship.collides_with(self.peach):
                self.peach = None
                self.spaceship = None

        # Bullet / asteroid collision
        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    break

        self.move_target_if_captured()

        self.clock.tick_busy_loop()
        self.ticks += 1
        self.current_life = self.target.capture_life
        self.RESET = False

    def _draw(self):
        self.screen.blit(self.background, (0, 0))

        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        pygame.display.flip()
        self.clock.tick(self.fps)

    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets]

        if self.spaceship is not None:
            game_objects.append(self.spaceship)

        if self.target is not None:
            game_objects.append(self.target)

        if self.peach is not None:
            game_objects.append(self.peach)

        return game_objects
    
    def random_position(self, margin=80):
        x = random.uniform(margin, self.SCREEN_WIDTH-margin)
        y = random.uniform(margin, self.SCREEN_HEIGHT-margin)

        return Vector2(x,y)
    
    # def random_position_away(self, margin=80, min_distance = 100, max_attempts=100):
    #     object_positions = [object_position.position for object_position in self._get_game_objects()]

    #     for _ in range(max_attempts):                                      #loop up to this many times
    #         candidate = self.random_position()               #define a random position for a guy
    #         for object_position in object_positions:                #loop through the game object positions
    #             if candidate.distance_to(object_position) >= min_distance:  #return candidate position if it meets the requirements
    #                 return candidate
        
    #     return self.random_position()    #return candidate anyway know we gave it the ole college try
    def random_position_away(self, margin=80, min_distance=200, max_attempts=100):
        object_positions = [
            obj.position for obj in self._get_game_objects()
            if obj is not None
        ]

        for _ in range(max_attempts):
            candidate = self.random_position(margin=margin)

            if all(candidate.distance_to(pos) >= min_distance for pos in object_positions):
                return candidate
        print("AHHHHHHHHHH")
        return self.random_position(margin=margin)