from pygame.math import Vector2

class Navigation:
    def choose_pseudo_target(
        self,
        game_state,
    ):
        """
        Return the desired navigation target position.
        """
        manual_position = (0, 0)
        return Vector2(manual_position)
