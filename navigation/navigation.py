from pygame.math import Vector2
from game.settings import GameSettings
from navigation.testFuzzyNavigation import look_ahead, avoidance
import math

class Navigation:
    def __init__(self):
        self.position = (0,0)
        self.margin = 1

    def choose_pseudo_target(self, game_state):
        """
        Choose a navigation target from a read-only entity-state snapshot.
        """
        target = game_state['target']
        peach = game_state['peach']
        peach_position = Vector2(peach['position'])
        target_postion = Vector2(target['position'])
        to_target = target_postion - peach_position
        target_distance = to_target.length()
        target_direction = to_target.normalize()
        peach_velocity = Vector2(peach['velocity'])
        if peach_velocity != Vector2(0,0):
            peach_velocity_direction = Vector2(peach_velocity).normalize()
        else:
            peach_velocity_direction = target_direction

        #Asteroid states
        asteroid_states = []
        for i, a in enumerate(game_state['asteroids']):
            to_asteroid = Vector2(a['position']) - peach_position
            to_asteroid_direction = to_asteroid.normalize()
            asteroid_bearing = target_direction.angle_to(to_asteroid_direction)
            effective_radius = peach['radius'] + a['radius'] + self.margin
            asteroid_distance = to_asteroid.length()
            asteroid_clearance = to_asteroid.length() - effective_radius
            
            #Check if asteroid is between Peach and target
            asteroid_offset = to_asteroid.dot(target_direction)
            asteroid_along_velocity = to_asteroid.dot(peach_velocity_direction)
            closest_point = peach_position + peach_velocity_direction*asteroid_along_velocity
            cross_track_distance = (game_state['asteroids'][0]['position'] - closest_point).length()
            asteroid_on_velocity_path = (asteroid_along_velocity > 0 and cross_track_distance < effective_radius)

            asteroid_states.append({
                "index": i,
                "position": a['position'],
                "distance": asteroid_distance,
                "clearance": asteroid_clearance,
                "bearing": asteroid_bearing,
                "along_velocity": asteroid_along_velocity,
                "cross_track": cross_track_distance,
                "on_velocity_path": asteroid_on_velocity_path,
                "effective_radius": effective_radius,
            })
        
        max_avoidance_distance = 50
        #Now filter out relevant asteroid states
        for asteroid_state in asteroid_states:
            if asteroid_state["clearance"] > max_avoidance_distance:
                continue

            if asteroid_state["along_velocity"] <= 0:
                continue

            if not asteroid_state["on_velocity_path"]:
                continue

            relevant_asteroids.append(asteroid_state)
        

        avoidance_out = avoidance.evaluate({
            "asteroid_clearance": asteroid_clearance_list[0],
            "asteroid_bearing": asteroid_bearing_list[0]
        })

        look_ahead_out = look_ahead.evaluate({
            "target_distance": target_distance,
            "asteroid_clearance": asteroid_clearance_list[0]                
        })

        if not asterdoid_on_velcoty_path:
            avoidance_offset = 0

        navigation_direction = (target_direction.rotate(avoidance_offset))
        pseudo_target_distance = min(
            look_ahead_out["pseudo_target_distance"],
            target_distance,
        )


        self.position = (
            peach_position + navigation_direction * pseudo_target_distance
        )

        # print(f'asteroid offset: {asteroid_offset}\ntarget distance: {target_distance}')
        # print(f'avoidance offset: {avoidance_offset}')
        # print(f'navigation_direction: {navigation_direction}')
        # print(f'pesudo target distance: {pseudo_target_distance}\n')