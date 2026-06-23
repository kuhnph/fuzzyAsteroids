from .membership import left_shoulder, right_shoulder
from .chromosome import (
    decode_input_membership,
    decode_output_membership,
    decode_rules,
    decode_chromosome,
)
from .inference import scaled_output_centroid


class FuzzyController:
    """
    Chromosome-driven fuzzy controller for Peach.

    Expected feature inputs
    -----------------------
    heading_error : float
    position_error : float
    speed : float
    """
    requires_chromosome = True

    def __init__(self, chromosome_config):
        self.chromosome_config = chromosome_config
        self.debugCount = 0

    def evaluate(self, chromosome, heading_error, position_error, speed):
        """
        Chromosome be changing
        """
        # if len(chromosome) != 52:
        #     raise ValueError("Controller expects a chromosome of length 52")

        position_genes, speed_genes, rule_genes, output_genes = decode_chromosome(chromosome, self.chromosome_config)

        # Input 1: heading error
        # Original code used a 2-set shoulder split at zero.
        heading_negative = right_shoulder(
            heading_error,
            self.chromosome_config.heading_split_min,
            self.chromosome_config.heading_split_max,
        )
        heading_positive = left_shoulder(
            heading_error,
            self.chromosome_config.heading_split_min,
            self.chromosome_config.heading_split_max,
        )

        # Input 2: position error
        position_memberships = decode_input_membership(
            position_error,
            chromosome=position_genes,
            map_min=self.chromosome_config.position_error_min,
            map_max=self.chromosome_config.position_error_max,
            n_sets=self.chromosome_config.n_position_sets,
        )

        # Input 3: speed
        speed_memberships = decode_input_membership(
            speed,
            chromosome=speed_genes,
            map_min=self.chromosome_config.speed_min,
            map_max=self.chromosome_config.speed_max,
            n_sets=self.chromosome_config.n_speed_sets,
        )

        # Output 1: turn direction
        # Preserved from original code:
        #   if angle negative -> go clockWise
        #   if angle positive -> go counterWise
        direction_rule_memberships = [
            [heading_negative],
            [heading_positive],
        ]
        direction_output_sets = self.chromosome_config.direction_output_sets

        # Output 2: speed command
        speed_rule_memberships = decode_rules(
            position_memberships,
            speed_memberships,
            chromosome= rule_genes,
            n_sets=self.chromosome_config.n_output_sets,
        )

        speed_output_sets = decode_output_membership(
            chromosome=output_genes,
            map_min=self.chromosome_config.speed_output_min,
            map_max=self.chromosome_config.speed_output_max,
            n_sets=self.chromosome_config.n_output_sets,
        )


        # Defuzzify outputs
        turn_value = scaled_output_centroid(
            direction_rule_memberships,
            direction_output_sets,
        )


        speed_value = scaled_output_centroid(
            speed_rule_memberships,
            speed_output_sets,
        )

        peach_turn = (
            self.chromosome_config.counter_clockwise_action
            if turn_value > 0
            else self.chromosome_config.clockwise_action
        )
        peach_move = (
            self.chromosome_config.accelerate_action
            if speed_value > speed
            else self.chromosome_config.no_acceleration_action
        )

        # Preserved original behavior:
        # ship action is effectively hard-coded in your current code.
        ship_actions = list(self.chromosome_config.ship_actions)
        peach_actions = [peach_move, peach_turn]

        # if self.debugCount % 10 == 0:
            # print(f"{peach_actions[0]}, {peach_actions[1]}")
            # print(f"speed = {speed} | speed value = {speed_value}")

        self.debugCount+=1
        return ship_actions, peach_actions

    def evaluate_from_features(self, chromosome, features):
        """
        Convenience wrapper for passing a features dict.
        """
        return self.evaluate(
            chromosome=chromosome,
            heading_error=features["heading_error"],
            position_error=features["position_error"],
            speed=features["speed"],
        )
