from game import SpaceRocks
from controllers.testControl import TestControl


def main():
    user_input = False
    freeze = 1

    game = SpaceRocks(user_input=user_input, enable_player=False)
    controller = TestControl(game)
    while True:
        if user_input == True:
            game.play_step()
        else:
            controller.control_step()
            if freeze == 1:
                freeze = input()


if __name__ == "__main__":
    main()
