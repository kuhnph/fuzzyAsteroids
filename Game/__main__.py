from game import SpaceRocks

if __name__ == "__main__":    
    space_rocks = SpaceRocks(user_input=True)
    while True:
        space_rocks.play_step()
