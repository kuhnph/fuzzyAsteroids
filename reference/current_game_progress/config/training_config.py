from dataclasses import dataclass

@dataclass
class TrainingConfig:
    max_train_ticks: int = 1000
    training_samples: int = 30
    max_memory: int = 100_000

    TOURNSIZE: int = 7
    POPULATION_SIZE: int = 6
    CXPB: float = 0.6
    MUTPB: float = 0.2
    MUTATION_INDPB: float = 0.1
    GENERATIONS_PER_STEP: int = 1
    HALL_OF_FAME_SIZE: int = 1

    PLAY_MAX_TICKS: int = 1000
    LOST_AGENT_COST: float = 1e6
    NO_CAPTURE_COST: float = 1e6

    GENERATION_COST_FILE: str = "generation_cost.txt"
    VELOCITY_LOG_FILE: str = "velocity_time.txt"
    POSITION_ERROR_LOG_FILE: str = "positionError_time.txt"
