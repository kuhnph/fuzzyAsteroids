import time
from collections import deque

from game import SpaceRocks
from fuzzy import build_controller

from .features import extract_features
from .cost import compute_episode_cost
from .ga import initialize_ga, step_generation
from .logging import (
    write_generation_cost,
    write_velocity_sample,
    write_position_error_sample,
)
from config.training_config import TrainingConfig
from config.fuzzy_config import ChromosomeConfig


class TrainingAgent:
    def __init__(self, render=False, controller_mode=None):
        self.training_samples = TrainingConfig.training_samples
        self.memory = deque(maxlen=TrainingConfig.max_memory)

        # GA state
        self.ga_initialized = False
        self.generation = 0


        self.TOURNSIZE = TrainingConfig.TOURNSIZE
        self.POPULATION_SIZE = TrainingConfig.POPULATION_SIZE
        self.CXPB = TrainingConfig.CXPB
        self.MUTPB = TrainingConfig.MUTPB

        self.chromosome_config = ChromosomeConfig()
        if controller_mode is not None:
            self.chromosome_config.controller_mode = controller_mode

        self.N = self.chromosome_config.length
        self.INT_MIN = self.chromosome_config.gene_min
        self.INT_MAX = self.chromosome_config.gene_max

        # Environment + controller
        #TODO make separate agents
        self.game = SpaceRocks(user_input=False, enable_player=False, render=render)
        self.controller = build_controller(self.chromosome_config)

        # Episode bookkeeping
        self.overshoot_error = 0.0
        self.pop_evals = 0

        # Optional history
        self.vs = []
        self.time_steps = []

        # Cached last extracted features
        self.states = None
        self.relative_states = None
        self.game_time = 0
        self.v = 0.0


    def reset_episode_tracking(self):
        self.overshoot_error = 0.0
        self.states = None
        self.relative_states = None
        self.game_time = 0
        self.v = 0.0
        self.vs = []
        self.time_steps = []

    def refresh_features(self):
        """
        Pull the current game state into the agent cache.
        """
        features = extract_features(self.game)

        self.states = features["states"]
        self.relative_states = features["relative_states"]
        self.game_time = features["game_time"]
        self.v = features["speed"]

        return features

    def controller_step(self, chromosome=None):
        """
        Run one fuzzy-control step from the current cached features.
        """
        heading_error = self.relative_states[3]
        position_error = self.relative_states[0]
        speed = self.v

        self.vs.append(speed)
        self.time_steps.append(self.game_time)

        write_velocity_sample(self.game_time, speed)
        write_position_error_sample(self.game_time, position_error)

        if self.controller.requires_chromosome:
            if chromosome is None:
                raise ValueError("Genetic fuzzy controller requires a chromosome")

            ship_actions, peach_actions = self.controller.evaluate(
                chromosome=chromosome,
                heading_error=heading_error,
                position_error=position_error,
                speed=speed,
            )
        else:
            ship_actions, peach_actions = self.controller.evaluate(
                heading_error=heading_error,
                position_error=position_error,
                speed=speed,
            )

        return ship_actions, peach_actions

    def update_overshoot_metric(self):
        """
        Preserve the later agent_final.py behavior:
        after capture starts, track the max position error observed.
        """
        position_error = self.relative_states[0]

        if self.game.current_life < self.game.START_CAPTURE_LIFE:
            self.overshoot_error = max(self.overshoot_error, position_error)

    def evaluate_one_episode(self, chromosome=None):
        """
        Evaluate the active controller over a single episode.

        Returns
        -------
        float
            Episode cost.
        """
        self.game.reset_episode()
        self.reset_episode_tracking()

        velocity_sum = 0.0
        velocity_count = 0
        heading_sum = 0.0

        while True:
            if self.game.peach is None:
                break

            self.refresh_features()
            ship_actions, peach_actions = self.controller_step(chromosome)

            self.game.play_step(ship_actions, peach_actions)
            self.update_overshoot_metric()

            speed_sample = (self.states[2]**2 + self.states[3]**2) ** 0.5
            heading_sample = self.relative_states[1]

            heading_sum += heading_sample
            velocity_sum += speed_sample
            velocity_count += 1

            if self.game.current_life < 0:
                break

            if self.game.ticks > self.game.max_train_ticks:
                break

        if self.game.peach is not None:
            self.refresh_features()
            final_position_error = self.relative_states[0]
        else:
            final_position_error = TrainingConfig.LOST_AGENT_COST

        average_velocity = velocity_sum / velocity_count if velocity_count > 0 else 0.0

        if velocity_count > 0 and self.game.initial_position_error > 0:
            progress_fraction = (
                self.game.initial_position_error - final_position_error
            ) / self.game.initial_position_error
        else:
            progress_fraction = 0.0

        cost = compute_episode_cost(
            self.game,
            overshoot_error=self.overshoot_error,
            average_velocity=average_velocity,
            progress_fraction=progress_fraction,
        )

        print(cost)
        return cost

    def evaluate_chromosome(self, chromosome):
        """
        Evaluate one chromosome over multiple randomized episodes.

        Returns a DEAP-compatible tuple: (cost,)
        """
        if not self.controller.requires_chromosome:
            raise ValueError("Hand-tuned fuzzy mode does not evaluate chromosomes")

        self.pop_evals += 1

        total_cost = 0.0

        for _ in range(self.training_samples):
            episode_cost = self.evaluate_one_episode(chromosome)
            total_cost += episode_cost

        average_cost = total_cost / self.training_samples

        print(f'average cost: {average_cost}')
        return (average_cost,)

    def evaluate_current_controller(self):
        """
        Evaluate the active controller over the configured sample count.
        """
        total_cost = 0.0

        for _ in range(self.training_samples):
            total_cost += self.evaluate_one_episode()

        average_cost = total_cost / self.training_samples
        print(f'average controller cost: {average_cost}')
        return average_cost

    def train_step(self):
        """
        Initialize GA on first call, then advance by one generation on later calls.
        """
        if not self.controller.requires_chromosome:
            raise ValueError("GA training requires controller_mode='genetic'")

        if not self.ga_initialized:
            initialize_ga(self)
            return None

        self.pop_evals = 0  #Does setting this 0 here create an issue?
        start_gen = time.perf_counter()

        best_individual, best_cost = step_generation(self)

        end_gen = time.perf_counter()

        print("\n")
        print(f"generation time: {abs(start_gen - end_gen)}")
        print("GENERATION:", self.generation + 1)
        print(f"Best Individual: {list(best_individual)}")
        print(f"best cost: {best_cost}")
        print("\n")

        self.generation += 1
        write_generation_cost(self.generation, best_cost)

        return best_individual, best_cost

    def play_current_controller(self, chromosome=None):
        """
        Run the game continuously using the active controller.
        """
        if self.controller.requires_chromosome and chromosome is None:
            raise ValueError("Genetic fuzzy controller requires a chromosome")

        self.game.reset_episode()
        self.reset_episode_tracking()

        while True:
            if self.game.peach is None:
                self.game.reset_episode()
                self.reset_episode_tracking()

            self.refresh_features()
            ship_actions, peach_actions = self.controller_step(chromosome)
            self.game.play_step(ship_actions, peach_actions)

            if self.game.current_life < 0 or self.game.ticks > TrainingConfig.PLAY_MAX_TICKS:
                self.game.reset_episode()
                self.reset_episode_tracking()

    def play_with_chromosome(self, chromosome):
        """
        Backward-compatible wrapper for genetic fuzzy playback.
        """
        self.play_current_controller(chromosome)
