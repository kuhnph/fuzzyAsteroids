import math

from game.settings import ActionSettings
from controllers.testFuzzy import vehicle_controller
from navigation.navigation import Navigation


ACTION_CONFIG = ActionSettings()
N = Navigation()


class TestControl:
    """
    Basic Peach controller that steers toward the target.
    """

    def __init__(self, game):
        self.game = game

    def navigation_step(self, state):
        N.choose_pseudo_target(game_state=state)

    def control_step(self):
        state = self.game.get_entity_states()
        self.navigation_step(state)
        pseudo_target_position = N.position

        peach_actions = self.get_peach_actions(
            state=state,
            pseudo_target_position=pseudo_target_position,
        )
        self.game.play_step(ship_actions=[], peach_actions=peach_actions)
        return self.game.get_entity_states()

    def get_peach_actions(self, state, pseudo_target_position):
        peach = state["peach"]

        if peach is None or pseudo_target_position is None:
            return []

        heading_error = self._heading_error_to_target(peach, pseudo_target_position)
        position_error = math.hypot(
            peach['position'][0] - pseudo_target_position[0],
            peach['position'][1] - pseudo_target_position[1],
        )

        speed = (peach['velocity'][0]**2+peach['velocity'][1]**2)**.5
        actions = []

        outputs = vehicle_controller.evaluate({
                    "heading_error": heading_error,
                    "distance_error": position_error,
                    "speed": speed,
                    })
        

        if outputs['desired_turn_rate'] < 0:
            actions.append(ACTION_CONFIG.counter_clockwise_action)
        elif  outputs['desired_turn_rate'] > 0:
            actions.append(ACTION_CONFIG.clockwise_action)

        if outputs['desired_speed'] > speed:
            actions.append(ACTION_CONFIG.accelerate_action)

        return actions

    def _heading_error_to_target(self, O1, target_position):
        O1_position = O1["position"]
        O1_direction = O1["direction"]

        current_heading = math.atan2(O1_direction[1], O1_direction[0])
        target_heading = math.atan2(
            target_position[1] - O1_position[1],
            target_position[0] - O1_position[0],
        )

        return self._normalize_angle(target_heading - current_heading)

    def _normalize_angle(self, angle):
        while angle > math.pi:
            angle -= 2 * math.pi

        while angle < -math.pi:
            angle += 2 * math.pi

        return angle


# Backward-compatible alias for the original lowercase class name.
testControl = TestControl
