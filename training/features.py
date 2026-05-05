import math
import numpy as np


def _compute_heading(direction_vector):
    """
    Reproduce the heading conversion logic from the original project.
    """
    heading = math.atan2(direction_vector[0], direction_vector[1])

    if 0 < heading >= np.pi / 2:
        heading = heading - np.pi / 2
    elif heading < 0:
        heading = heading + 2 * np.pi - np.pi / 2
    else:
        heading = heading + 3 * np.pi / 2

    return heading


def extract_features(game):
    """
    Extract the state/features used by the fuzzy controller and trainer.

    Returns
    -------
    dict
        {
            "states": [...],
            "relative_states": [...],
            "game_time": int,
            "speed": float,
            "position_error": float,
            "heading_error": float,
            "target_angle": float,
        }
    """
    if game.peach is None:
        raise ValueError("Cannot extract features: Peach no longer exists.")

    # Peach states
    x1 = game.peach.position[0]
    y1 = game.peach.position[1]
    u1 = game.peach.velocity[0]
    v1 = game.peach.velocity[1]

    heading = _compute_heading(game.peach.direction)

    # Asteroid states
    xa = [asteroid.position[0] for asteroid in game.asteroids]
    ya = [asteroid.position[1] for asteroid in game.asteroids]
    ua = [asteroid.velocity[0] for asteroid in game.asteroids]
    va = [asteroid.velocity[1] for asteroid in game.asteroids]

    # Target state
    xt = game.target.position[0]
    yt = game.target.position[1]

    states = [
        x1,   # peach x position
        y1,   # peach y position
        u1,   # peach x velocity
        v1,   # peach y velocity
        xa,   # asteroid x positions
        ya,   # asteroid y positions
        ua,   # asteroid x velocities
        va,   # asteroid y velocities
        xt,   # target x
        yt,   # target y
    ]

    # Relative position from Peach to target
    dx_peach_target = xt - x1
    dy_peach_target = yt - y1

    position_error = math.sqrt(dx_peach_target**2 + dy_peach_target**2)

    angle_peach_target = math.atan2(-dy_peach_target, dx_peach_target)
    if angle_peach_target < 0:
        angle_peach_target += 2 * np.pi

    heading_error = angle_peach_target - heading
    if heading_error < -np.pi:
        heading_error += 2 * np.pi
    elif heading_error > np.pi:
        heading_error -= 2 * np.pi

    relative_positions_asteroids = []
    for asteroid_x, asteroid_y in zip(xa, ya):
        dx_peach_asteroid = asteroid_x - x1
        dy_peach_asteroid = asteroid_y - y1
        magnitude = math.sqrt(dx_peach_asteroid**2 + dy_peach_asteroid**2)
        angle = math.atan2(dy_peach_asteroid, dx_peach_asteroid)
        relative_positions_asteroids.append((magnitude, angle))

    relative_states = [
        position_error,
        angle_peach_target,
        relative_positions_asteroids,
        heading_error,
    ]

    speed = (u1**2 + v1**2) ** 0.5

    game_variables = [game.SCREEN_HEIGHT, game.SCREEN_WIDTH]

    return {
        "states": states,
        "relative_states": relative_states,
        "game_time": game.ticks,
        "speed": speed,
        "position_error": position_error,
        "heading_error": heading_error,
        "target_angle": angle_peach_target,
        "game_variables": game_variables
    }