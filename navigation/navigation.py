from pygame.math import Vector2
from game.settings import GameSettings
from navigation.testFuzzyNavigation import look_ahead, avoidance
from navigation.settings import NavigationSettings
import math

class Navigation:
    def __init__(self):
        self.position = Vector2(0,0)
        self.margin = 10
        self.max_avoidance_distance = NavigationSettings.MAX_AVOIDANCE_DISTANCE

        self.asteroid_states = []
        self.relevant_asteroids = []

        self.peach_position = Vector2(0,0)
        self.target_position = Vector2(0,0)
        self.target_direction = Vector2(0,0)
        self.target_distance = 0
        self.counter = 0

    def choose_pseudo_target(self,game_state):
        '''
        Basically the navigation algorithm
        '''

        self.calculate_navigation_states(game_state)
        self.filter_asteroids()
        selected_asteroid = self.select_asteroid()
        avoidance_offset = self.calculate_avoidance_offset(selected_asteroid)
        pseudo_target_distance = self.calculate_look_ahead_distance(selected_asteroid)
        self.position = self.calculate_pseudo_target_position(
            avoidance_offset,
            pseudo_target_distance)

        self.counter += 1

    def calculate_navigation_states(self, game_state):
        """
        Calculate target, Peach, and asteroid states used for navigation.
        """
        target = game_state['target']
        peach = game_state['peach']

        self.peach_position = Vector2(peach['position'])
        self.target_position = Vector2(target['position'])

        to_target = self.target_position - self.peach_position
        self.target_distance = to_target.length()

        if self.target_distance > 0:
            self.target_direction = to_target.normalize()
        else:
            self.target_direction = Vector2(0,0)

        peach_velocity = Vector2(peach['velocity'])
        if peach_velocity != Vector2(0,0):
            peach_velocity_direction = Vector2(peach_velocity).normalize()
        else:
            peach_velocity_direction = self.target_direction

        #Asteroid states
        self.asteroid_states = []
        for i, a in enumerate(game_state['asteroids']):
            asteroid_position = Vector2(a['position'])
            to_asteroid = asteroid_position - self.peach_position
            asteroid_distance = to_asteroid.length()
            if asteroid_distance > 0:
                to_asteroid_direction = to_asteroid.normalize()
            else:
                to_asteroid_direction = Vector2(0,0)
            asteroid_bearing = self.target_direction.angle_to(to_asteroid_direction)
            effective_radius = peach['radius'] + a['radius'] + self.margin
            asteroid_clearance = asteroid_distance - effective_radius
            
            #Check if asteroid is between Peach and target
            asteroid_along_target = to_asteroid.dot(self.target_direction)
            asteroid_along_velocity = to_asteroid.dot(peach_velocity_direction)

            closest_point = self.peach_position + peach_velocity_direction*asteroid_along_velocity
            cross_track_distance = (asteroid_position - closest_point).length()
            asteroid_on_velocity_path = (asteroid_along_velocity > 0 and cross_track_distance < effective_radius)

            self.asteroid_states.append({
                "index": i,
                "position": asteroid_position,
                "distance": asteroid_distance,
                "clearance": asteroid_clearance,
                "bearing": asteroid_bearing,
                "along_target": asteroid_along_target,
                "along_velocity": asteroid_along_velocity,
                "cross_track": cross_track_distance,
                "on_velocity_path": asteroid_on_velocity_path,
                "effective_radius": effective_radius,
            })

    def filter_asteroids(self):
        '''
        remove asteroids not on peach path
        '''
        self.relevant_asteroids = []

        for asteroid_state in self.asteroid_states:
            if asteroid_state["clearance"] >self. max_avoidance_distance:
                continue
            if asteroid_state["along_velocity"] <= 0:
                continue
            if not asteroid_state["on_velocity_path"]:
                continue

            self.relevant_asteroids.append(asteroid_state)

    def select_asteroid(self):
        """
        Select one asteroid for the current fuzzy navigation system.

        This can later be replaced by fuzzy threat scoring or
        weighted aggregation across all relevant asteroids.
        """
        if not self.relevant_asteroids:
            return None

        selected_asteroid = min(
            self.relevant_asteroids, key=lambda asteroid: asteroid["clearance"]
            )

        return selected_asteroid

    def calculate_avoidance_offset(self, selected_asteroid):
        """
        Run the fuzzy avoidance layer.
        """
        if selected_asteroid is None:
            return 0

        asteroid_clearance = max(
            0,
            min(
                selected_asteroid["clearance"],
                self.max_avoidance_distance
            )
        )

        avoidance_out = avoidance.evaluate({
            "asteroid_clearance": asteroid_clearance,
            "asteroid_bearing": selected_asteroid["bearing"]
        })

        return avoidance_out["avoidance_offset"]

    def calculate_look_ahead_distance(self, selected_asteroid):
        """
        Run the fuzzy look-ahead layer.
        """
        if selected_asteroid is None:
            asteroid_clearance = self.max_avoidance_distance
        else:
            asteroid_clearance = max(
                0,
                min(
                    selected_asteroid["clearance"],
                    self.max_avoidance_distance
                )
            )

        look_ahead_out = look_ahead.evaluate({
            "target_distance": self.target_distance,
            "asteroid_clearance": asteroid_clearance
        })

        return min(
            look_ahead_out["pseudo_target_distance"],
            self.target_distance
        )

    def calculate_pseudo_target_position(
        self,
        avoidance_offset,
        pseudo_target_distance
    ):
        """
        Convert the fuzzy outputs into an x-y waypoint.
        """
        navigation_direction = (
            self.target_direction.rotate(avoidance_offset)
        )

        return (
            self.peach_position
            + navigation_direction*pseudo_target_distance
        )