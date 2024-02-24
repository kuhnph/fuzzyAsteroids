import pygame
from models import Spaceship, Asteroid, Bullet, Target, Peach
from utils import load_sprite, wrap_position, get_random_position

class SpaceRocks:
    MIN_ASTEROID_DISTANCE = 250
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080
    def __init__(self):
        self._init_pygame()
        # self.screen = pygame.display.set_mode((800, 600))
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.background = load_sprite("space", False)
        self.clock = pygame.time.Clock()

        self.asteroids = []
        self.bullets = []
        self.spaceship = Spaceship((400, 300), self.bullets.append)
        # Added Peach
        self.peach = Peach((300, 400))

        self.capture_agents = [self.peach]
        self.target = Target(get_random_position(self.screen), 10.0)

        for _ in range(1):
            while True:
                position = get_random_position(self.screen)
                # If asteroid hits spaceship or peach, break
                if (
                    position.distance_to(self.spaceship.position)
                    > self.MIN_ASTEROID_DISTANCE
                    or
                    position.distance_to(self.peach.position)
                    > self.MIN_ASTEROID_DISTANCE
                ):
                    break

            self.asteroids.append(Asteroid(position, self.asteroids.append))

    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Space Rocks")

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()
            elif (
                self.spaceship
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
            ):
                self.spaceship.shoot()
        is_key_pressed = pygame.key.get_pressed()

        if self.spaceship:
            if is_key_pressed[pygame.K_RIGHT]:
                self.spaceship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT]:
                self.spaceship.rotate(clockwise=False)   
            if is_key_pressed[pygame.K_UP]:
                self.spaceship.accelerate()  

        # Copied above for peach, with inputs WASD
        if self.peach:
            if is_key_pressed[pygame.K_d]:
                self.peach.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_a]:
                self.peach.rotate(clockwise=False)   
            if is_key_pressed[pygame.K_w]:
                self.peach.accelerate()  

              
    # Didn't touch this for peach
    def _process_game_logic(self):
        for game_object in self._get_game_objects():

            if isinstance(game_object, Bullet):
                game_object.move_no_wrap()
            else:
                game_object.move(self.screen)
            # if isinstance(game_object, Spaceship): print(game_object.velocity[1])
        
        #check if space ship hits asteroid
        if self.spaceship:
            self.spaceship.accelerate(0)
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship):
                    self.spaceship = None
                    break
                
        for capture_agent in self.capture_agents:
            if capture_agent.collides_with(self.target):
                self.target.capture()

        # Copied above for peach
        if self.peach:
            self.peach.accelerate(0)
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.peach):
                    self.peach = None
                    break
            for bullet in self.bullets:
                if bullet.collides_with(self.peach):
                    self.peach = None
                    break
            
            if self.spaceship.collides_with(self.peach):
                self.peach = None
                self.spaceship = None
                
                

        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    break
        

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        for game_object in self._get_game_objects(): game_object.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(60)
    
    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets]

        if self.spaceship:
            game_objects.append(self.spaceship)
        if self.target:
            game_objects.append(self.target)

        # copied above for peach
        if self.peach:
            game_objects.append(self.peach)
        
        return game_objects
