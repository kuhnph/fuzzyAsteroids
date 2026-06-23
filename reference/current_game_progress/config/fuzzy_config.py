from __future__ import annotations

from dataclasses import dataclass

@dataclass
class ChromosomeConfig:
    controller_mode: str = "genetic"
    genetic_controller_mode: str = "genetic"
    hand_tuned_controller_mode: str = "hand_tuned"

    n_position_sets: int = 20
    n_speed_sets: int = 20
    n_output_sets: int = 20
    gene_min: int = 0
    gene_max: int = 19

    position_error_min: float = 0.0
    position_error_max: float = 2203.0
    speed_min: float = -0.01
    speed_max: float = 2.5
    speed_output_min: float = 0.0
    speed_output_max: float = 2.5

    heading_split_min: float = 0.0
    heading_split_max: float = 0.0
    direction_output_sets: tuple[tuple[float, float, float], ...] = (
        (-1, -0.1, 0),
        (0, 0.1, 1),
    )
    shoot_action: str = "shooting"
    clockwise_action: str = "clockWise"
    counter_clockwise_action: str = "counterWise"
    accelerate_action: str = "accelerate"
    no_acceleration_action: str = "not"

    @property
    def ship_actions(self):
        return (
            self.shoot_action,
            self.clockwise_action,
            self.accelerate_action,
        )

    hand_position_sets: tuple[tuple[float, float, float], ...] = (
        (0.0, 0.0, 150.0),
        (75.0, 250.0, 500.0),
        (350.0, 800.0, 1250.0),
        (1000.0, 1500.0, 1900.0),
        (1700.0, 2203.0, 2203.0),
    )
    hand_speed_sets: tuple[tuple[float, float, float], ...] = (
        (-0.01, -0.01, 0.25),
        (0.1, 0.5, 0.9),
        (0.7, 1.2, 1.7),
        (1.5, 2.0, 2.35),
        (2.2, 2.5, 2.5),
    )
    hand_speed_output_sets: tuple[tuple[float, float, float], ...] = (
        (0.0, 0.0, 0.35),
        (0.2, 0.65, 1.0),
        (0.8, 1.25, 1.7),
        (1.45, 1.9, 2.25),
        (2.05, 2.5, 2.5),
    )
    hand_speed_rules: tuple[tuple[int, ...], ...] = (
        (0, 0, 0, 0, 0),
        (2, 1, 0, 0, 0),
        (3, 2, 1, 0, 0),
        (4, 3, 2, 1, 0),
        (4, 4, 3, 2, 1),
    )

    @property
    def position_gene_count(self):
        return 2 * self.n_position_sets - 2

    @property
    def speed_gene_count(self):
        return 2 * self.n_speed_sets - 2

    @property
    def rule_gene_count(self):
        return self.n_position_sets * self.n_speed_sets

    @property
    def output_gene_count(self):
        return 2 * self.n_output_sets - 2

    @property
    def length(self):
        return (
            self.position_gene_count
            + self.speed_gene_count
            + self.rule_gene_count
            + self.output_gene_count
        )
