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

    # These ranges are taken directly from your current controller.
    POSITION_ERROR_MIN = 0.0
    POSITION_ERROR_MAX = 2203.0

    SPEED_MIN = -0.01
    SPEED_MAX = 2.5

    def __init__(self, chromosome_config):
        self.chromosome_config = chromosome_config
        self.debugCount = 0
        pass

    def evaluate(self, chromosome, heading_error, position_error, speed):
        """
        Chromosome be changing
        """
        # if len(chromosome) != 52:
        #     raise ValueError("Controller expects a chromosome of length 52")

        position_genes, speed_genes, rule_genes, output_genes = decode_chromosome(chromosome, self.chromosome_config)

        # Input 1: heading error
        # Original code used a 2-set shoulder split at zero.
        heading_negative = right_shoulder(heading_error, 0, 0)
        heading_positive = left_shoulder(heading_error, 0, 0)

        # Input 2: position error
        position_memberships = decode_input_membership(
            position_error,
            chromosome=position_genes,
            map_min=self.POSITION_ERROR_MIN,
            map_max=self.POSITION_ERROR_MAX,
            n_sets=self.chromosome_config.n_position_sets,
        )

        # Input 3: speed
        speed_memberships = decode_input_membership(
            speed,
            chromosome=speed_genes,
            map_min=self.SPEED_MIN,
            map_max=self.SPEED_MAX,
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
        direction_output_sets = [
            [-1, -0.1, 0],
            [0, 0.1, 1],
        ]

        # Output 2: speed command
        speed_rule_memberships = decode_rules(
            position_memberships,
            speed_memberships,
            chromosome= rule_genes,
            n_sets=self.chromosome_config.n_output_sets,
        )

        speed_output_sets = decode_output_membership(
            chromosome=output_genes,
            map_min=0,
            map_max=2.5,
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

        peach_turn = "counterWise" if turn_value > 0 else "clockWise"
        peach_move = "accelerate" if speed_value > speed else "not"

        # Preserved original behavior:
        # ship action is effectively hard-coded in your current code.
        ship_actions = ["shooting", "clockWise", "accelerate"]
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