from game import SpaceRocks


def main():
    game = SpaceRocks(user_input=True, enable_player=False)

    while True:
        game.play_step()


if __name__ == "__main__":
    main()
