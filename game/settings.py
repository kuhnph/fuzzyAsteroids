from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar


@dataclass
class GameSettings:
    SCREEN_WIDTH: int = int(1920 / 1.5)
    SCREEN_HEIGHT: int = int(1080 / 1.5)
    WINDOW_CAPTION: str = "Space Rocks"
    DEFAULT_FPS: int = 1000/10

    MIN_ASTEROID_DISTANCE: int = 250
    START_CAPTURE_LIFE: int = 10
    CAPTURE_DECREMENT: float = 0.1

    INITIAL_ASTEROID_COUNT: int = 4
    POSITION_MARGIN: int = 200
    RANDOM_POSITION_MARGIN: int = 80
    RANDOM_AWAY_MIN_DISTANCE: int = 200
    RANDOM_AWAY_MAX_ATTEMPTS: int = 100
    PLAYER_START_POSITION: tuple[int, int] = (400, 300)

    SPACESHIP_MANEUVERABILITY: float = 5
    SPACESHIP_ACCELERATION: float = 0.1
    SPACESHIP_BULLET_SPEED: float = 3
    SPACESHIP_DAMPENING: float = 0.01

    PEACH_MANEUVERABILITY: float = 2.5
    PEACH_ACCELERATION: float = 0.05
    PEACH_DAMPENING: float = 0.01

    ASTEROID_MIN_SPEED: int = 1
    ASTEROID_MAX_SPEED: int = 3
    ASTEROID_START_SIZE: int = 2
    ASTEROID_SPLIT_COUNT: int = 2
    ASTEROID_SIZE_TO_SCALE: ClassVar[dict[int, float]] = {
        3: 1.0,
        2: 0.5,
        1: 0.25,
    }

    TARGET_SCALE: float = 0.5
    TARGET_LABEL_OFFSET_Y: int = 20

    FONT_PATH: str = "assets/fonts/ubuntu.mono.ttf"
    FONT_SIZE: int = 20
    FONT_COLOR: str = "white"

    MAX_TICKS: int = 1000


@dataclass
class ActionSettings:
    shoot_action: str = "shooting"
    clockwise_action: str = "clockWise"
    counter_clockwise_action: str = "counterWise"
    accelerate_action: str = "accelerate"
