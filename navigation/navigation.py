from pygame.math import Vector2
from game.settings import GameSettings

class Navigation:
    def __init__(self):
        self.position = (0,0)

    def choose_pseudo_target(self, game_state):
        """
        Choose a navigation target from a read-only entity-state snapshot.
        """
        # The first navigation strategy remains a fixed map position. Accepting
        # the snapshot now keeps navigation independent from the mutable game.
        self.position = (GameSettings.SCREEN_WIDTH/2, GameSettings.SCREEN_HEIGHT/2)
