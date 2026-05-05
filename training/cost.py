from .features import extract_features

def compute_episode_cost(game, overshoot_error, average_velocity):
    """
    Compute the episode cost using the later agent_final.py behavior.
    """

    X = extract_features(game)

    SCREEN_WIDTH = X['game_variables'][0]
    SCREEN_HEIGHT = X['game_variables'][1]
    SCREEN_DIAG = int((SCREEN_WIDTH**2+SCREEN_HEIGHT**2)**.5)
    overshoot_cost = overshoot_error / SCREEN_DIAG
    undershoot_cost = X['relative_states'][0] / SCREEN_DIAG

    if average_velocity < .1:
        no_speed_cost = 1
    else:
        no_speed_cost = 0

    time_cost = game.ticks / game.max_train_ticks

    cost = overshoot_cost*12 + no_speed_cost*.2 + undershoot_cost*.2 + time_cost*.4

    reached_capture_phase = game.current_life < game.START_CAPTURE_LIFE
    if not reached_capture_phase:
        cost = cost + 1
    
    print(f'overshoot cost: {overshoot_cost} | speed cost: {no_speed_cost} | Undershoot cost: {undershoot_cost} | time cost:{time_cost}')
    print(f'total cost: {cost}\n')
    return cost