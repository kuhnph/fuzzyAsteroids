from game import SpaceRocks
from controllers.testControl import TestControl


def main():
    user_input = False
    game = SpaceRocks(user_input=user_input, enable_player=False)
    controller = TestControl(game)
    state = game.get_entity_states()
    peach = state['peach']
    target = state['target']
    position_error = (abs(peach['position'][0] - target['position'][0])**2 + (peach['position'][1] - target['position'][1])**2)**.5
    while True:
        if user_input == True:
            game.play_step()
        else:
            controller.control_step()


if __name__ == "__main__":
    main()
