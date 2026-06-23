from .membership import triangular, left_shoulder, right_shoulder
from .inference import scaled_output_centroid


class HandTunedFuzzyController:
    """
    Config-driven fuzzy controller that does not require a chromosome.
    """
    requires_chromosome = False

    def __init__(self, fuzzy_config):
        self.fuzzy_config = fuzzy_config
        self._validate_config()

    def evaluate(self, heading_error, position_error, speed):
        heading_negative = right_shoulder(
            heading_error,
            self.fuzzy_config.heading_split_min,
            self.fuzzy_config.heading_split_max,
        )
        heading_positive = left_shoulder(
            heading_error,
            self.fuzzy_config.heading_split_min,
            self.fuzzy_config.heading_split_max,
        )

        direction_rule_memberships = [
            [heading_negative],
            [heading_positive],
        ]

        turn_value = scaled_output_centroid(
            direction_rule_memberships,
            self.fuzzy_config.direction_output_sets,
        )

        position_memberships = self._evaluate_sets(
            position_error,
            self.fuzzy_config.hand_position_sets,
        )
        speed_memberships = self._evaluate_sets(
            speed,
            self.fuzzy_config.hand_speed_sets,
        )
        speed_rule_memberships = self._evaluate_rule_table(
            position_memberships,
            speed_memberships,
        )

        speed_value = scaled_output_centroid(
            speed_rule_memberships,
            self.fuzzy_config.hand_speed_output_sets,
        )

        peach_turn = (
            self.fuzzy_config.counter_clockwise_action
            if turn_value > 0
            else self.fuzzy_config.clockwise_action
        )
        peach_move = (
            self.fuzzy_config.accelerate_action
            if speed_value > speed
            else self.fuzzy_config.no_acceleration_action
        )

        return list(self.fuzzy_config.ship_actions), [peach_move, peach_turn]

    def evaluate_from_features(self, features):
        return self.evaluate(
            heading_error=features["heading_error"],
            position_error=features["position_error"],
            speed=features["speed"],
        )

    def _evaluate_sets(self, value, sets):
        memberships = []

        for index, (left, center, right) in enumerate(sets):
            if index == 0:
                memberships.append(right_shoulder(value, center, right))
            elif index == len(sets) - 1:
                memberships.append(left_shoulder(value, left, center))
            else:
                memberships.append(triangular(value, left, center, right))

        return memberships

    def _evaluate_rule_table(self, position_memberships, speed_memberships):
        memberships = [[] for _ in self.fuzzy_config.hand_speed_output_sets]

        for position_index, position_value in enumerate(position_memberships):
            for speed_index, speed_value in enumerate(speed_memberships):
                output_bucket = self.fuzzy_config.hand_speed_rules[position_index][speed_index]
                memberships[output_bucket].append(min(position_value, speed_value))

        return memberships

    def _validate_config(self):
        position_count = len(self.fuzzy_config.hand_position_sets)
        speed_count = len(self.fuzzy_config.hand_speed_sets)
        output_count = len(self.fuzzy_config.hand_speed_output_sets)

        if len(self.fuzzy_config.hand_speed_rules) != position_count:
            raise ValueError("hand_speed_rules must have one row per hand_position_set")

        for row_index, row in enumerate(self.fuzzy_config.hand_speed_rules):
            if len(row) != speed_count:
                raise ValueError(
                    f"hand_speed_rules row {row_index} must have one value per hand_speed_set"
                )

            for output_bucket in row:
                if output_bucket < 0 or output_bucket >= output_count:
                    raise ValueError(
                        f"hand_speed_rules has invalid output bucket {output_bucket}. "
                        f"Expected 0 to {output_count - 1}."
                    )
