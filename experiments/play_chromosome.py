from training import TrainingAgent


BEST_CHROMOSOME = [
    # ------------------------------------------------------------
    # Position-error input membership genes
    # Used by:
    #   chromosome[0:8]
    #
    # Purpose:
    #   These 8 genes shape the 5 fuzzy sets for position_error.
    #
    # Range mapped over:
    #   POSITION_ERROR_MIN = 0.0
    #   POSITION_ERROR_MAX = 2203.0
    #
    # Interpreted as:
    #   position_error memberships, likely something like:
    #     Set 0 = very close / very small error
    #     Set 1 = close
    #     Set 2 = medium
    #     Set 3 = far
    #     Set 4 = very far
    # ------------------------------------------------------------
    0, 4, 4, 1, 3, 3, 3, 0,

    # ------------------------------------------------------------
    # UNUSED gene
    # Original implementation skips chromosome[8].
    # This gene currently has no effect.
    # ------------------------------------------------------------
    1,

    # ------------------------------------------------------------
    # Speed input membership genes
    # Used by:
    #   chromosome[9:17]
    #
    # Purpose:
    #   These 8 genes shape the 5 fuzzy sets for current speed.
    #
    # Range mapped over:
    #   SPEED_MIN = -0.01
    #   SPEED_MAX = 2.5
    #
    # Interpreted as:
    #   speed memberships, likely something like:
    #     Set 0 = stopped / very slow
    #     Set 1 = slow
    #     Set 2 = medium
    #     Set 3 = fast
    #     Set 4 = very fast
    # ------------------------------------------------------------
    3, 4, 2, 0, 0, 0, 1, 4,

    # ------------------------------------------------------------
    # UNUSED gene
    # Original implementation skips chromosome[17].
    # This gene currently has no effect.
    # ------------------------------------------------------------
    1,

    # ------------------------------------------------------------
    # Speed-command rule table genes
    # Used by:
    #   chromosome[18:43]
    #
    # Purpose:
    #   These 25 genes define a 5x5 fuzzy rule table.
    #
    # Inputs:
    #   rows    = position-error fuzzy set index
    #   columns = speed fuzzy set index
    #
    # Each gene selects one speed-output fuzzy set:
    #   0 = output set 0, likely very low / no acceleration desire
    #   1 = output set 1, likely low
    #   2 = output set 2, likely medium
    #   3 = output set 3, likely high
    #   4 = output set 4, likely very high
    #
    # Rule meaning:
    #   IF position_error is row_i AND speed is col_j
    #   THEN speed_command is output_set_gene
    # ------------------------------------------------------------

    # Position-error set 0 rules across speed sets 0..4
    # IF position_error is set 0 AND speed is set 0..4
    2, 3, 3, 2, 0,

    # Position-error set 1 rules across speed sets 0..4
    1, 1, 3, 0, 2,

    # Position-error set 2 rules across speed sets 0..4
    1, 1, 4, 1, 2,

    # Position-error set 3 rules across speed sets 0..4
    2, 0, 1, 4, 3,

    # Position-error set 4 rules across speed sets 0..4
    2, 0, 2, 0, 2,

    # ------------------------------------------------------------
    # UNUSED gene
    # Original implementation skips chromosome[43].
    # This gene currently has no effect.
    # ------------------------------------------------------------
    3,

    # ------------------------------------------------------------
    # Speed-output membership genes
    # Used by:
    #   chromosome[44:52]
    #
    # Purpose:
    #   These 8 genes shape the 5 fuzzy output sets for speed_value.
    #
    # Range mapped over:
    #   map_min = 0
    #   map_max = 2.5
    #
    # Interpreted as:
    #   speed command / acceleration desire output memberships:
    #     Set 0 = very low command
    #     Set 1 = low command
    #     Set 2 = medium command
    #     Set 3 = high command
    #     Set 4 = very high command
    #
    # The defuzzified result becomes speed_value.
    # Current movement decision:
    #   peach_move = "accelerate" if speed_value > speed else "not"
    # ------------------------------------------------------------
    2, 3, 4, 0, 1, 0, 4, 4,
]

BEST_CHROMOSOME = [3, 4, 2, 2, 3, 3, 4, 0, 1, 4, 3, 0, 2, 2, 2, 0, 0, 0, 1, 1, 2, 2, 1, 2, 3, 3, 0, 1, 0, 3, 1, 1, 3, 1, 3, 2, 0, 2, 3, 0, 2, 4, 4, 0, 0, 3, 4, 1, 2, 3, 2, 4]

def main():
    agent = TrainingAgent()
    agent.play_with_chromosome(BEST_CHROMOSOME)


if __name__ == "__main__":
    main()