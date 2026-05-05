import time
from collections import deque

from game import SpaceRocks
from fuzzy import FuzzyController

from .features import extract_features
from .cost import compute_episode_cost
from .ga import initialize_ga, step_generation
from .logging import (
    write_generation_cost,
    write_velocity_sample,
    write_position_error_sample,
)


MAX_MEMORY = 100_000


class TrainingAgent:
    def __init__(self):
        self.n_games = 0
        self.memory = deque(maxlen=MAX_MEMORY)

        # GA state
        self.ga_initialized = False
        self.generation = 0

        self.INT_MIN = 0
        self.INT_MAX = 4
        self.TOURNSIZE = 7
        self.POPULATION_SIZE = 6
        self.CXPB = 0.6
        self.MUTPB = 0.2
        self.N = 52

        # Environment + controller
        self.game = SpaceRocks(user_input=False, enable_player=False)
        self.controller = FuzzyController()

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

    def controller_step(self, chromosome):
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

        ship_actions, peach_actions = self.controller.evaluate(
            chromosome=chromosome,
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

    def evaluate_chromosome(self, chromosome):
        """
        Evaluate one chromosome over a single episode.

        Returns a DEAP-compatible tuple: (cost,)
        """
        self.pop_evals += 1
        self.game.reset_episode()
        self.reset_episode_tracking()

        velocity_sum = 0.0
        velocity_count = 0
        heading_sum = 0

        while True:
            if self.game.peach is None:
                # Peach died. End the episode harshly.
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
            final_position_error = 1e6

        reached_capture_phase = self.game.current_life < self.game.START_CAPTURE_LIFE

        average_velocity = velocity_sum / velocity_count if velocity_count > 0 else 0.0

        average_heading = heading_sum/velocity_count if velocity_count > 0 else 0.0

        cost = compute_episode_cost(self.game,
            overshoot_error=self.overshoot_error,
            average_velocity=average_velocity,
        )


        return (cost,)

    def train_step(self):
        """
        Initialize GA on first call, then advance by one generation on later calls.
        """
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

    def play_with_chromosome(self, chromosome):
        """
        Run the game continuously using a fixed chromosome.
        """
        self.game.reset_episode()
        self.reset_episode_tracking()

        while True:
            if self.game.peach is None:
                self.game.reset_episode()
                self.reset_episode_tracking()

            self.refresh_features()
            ship_actions, peach_actions = self.controller_step(chromosome)
            self.game.play_step(ship_actions, peach_actions)

            if self.game.current_life < 0 or self.game.ticks > 1000:
                self.game.reset_episode()
                self.reset_episode_tracking()