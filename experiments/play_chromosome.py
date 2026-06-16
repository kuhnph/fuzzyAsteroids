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

BEST_CHROMOSOME = [19, 17, 19, 11, 19, 19, 8, 17, 19, 17, 15, 9, 5, 2, 9, 0, 13, 14, 13, 3, 8, 6, 5, 15, 1, 14, 9, 8, 9, 7, 15, 8, 3, 12, 3, 10, 17, 18, 9, 11, 13, 11, 16, 6, 10, 17, 4, 13, 3, 18, 9, 18, 5, 6, 0, 8, 3, 9, 8, 3, 16, 10, 2, 8, 3, 7, 4, 18, 1, 13, 2, 10, 11, 1, 15, 18, 18, 3, 12, 0, 11, 7, 2, 5, 13, 7, 16, 15, 10, 5, 17, 1, 8, 12, 2, 11, 6, 0, 5, 3, 19, 4, 17, 18, 15, 16, 4, 1, 16, 7, 14, 6, 8, 15, 12, 13, 0, 11, 1, 0, 1, 10, 13, 3, 17, 18, 7, 4, 11, 3, 4, 17, 4, 17, 15, 18, 1, 10, 8, 8, 19, 17, 15, 16, 7, 15, 10, 14, 8, 16, 1, 13, 17, 12, 7, 17, 9, 2, 0, 13, 2, 13, 19, 4, 2, 10, 12, 16, 4, 14, 2, 7, 17, 17, 8, 11, 16, 5, 5, 9, 8, 12, 10, 7, 12, 2, 7, 15, 16, 15, 8, 9, 12, 9, 13, 7, 8, 15, 4, 17, 16, 7, 3, 7, 3, 3, 17, 10, 10, 9, 11, 9, 7, 15, 9, 1, 4, 12, 0, 11, 8, 6, 13, 12, 9, 2, 3, 5, 1, 6, 2, 5, 11, 17, 7, 19, 17, 9, 16, 17, 18, 18, 10, 4, 10, 19, 7, 16, 3, 11, 12, 8, 1, 14, 8, 7, 17, 11, 16, 17, 7, 12, 16, 4, 3, 17, 16, 8, 1, 18, 6, 15, 11, 1, 17, 8, 2, 15, 14, 6, 7, 10, 19, 17, 13, 8, 7, 2, 14, 11, 12, 13, 13, 6, 14, 13, 4, 11, 11, 18, 16, 13, 12, 4, 19, 13, 13, 1, 19, 19, 11, 10, 4, 7, 8, 11, 2, 4, 0, 17, 10, 12, 2, 10, 4, 17, 10, 6, 15, 8, 8, 15, 16, 17, 9, 5, 0, 10, 9, 7, 7, 17, 15, 10, 17, 15, 1, 19, 14, 3, 14, 8, 18, 9, 11, 4, 0, 8, 10, 19, 1, 13, 16, 12, 13, 17, 12, 11, 18, 14, 15, 7, 1, 8, 16, 2, 4, 0, 4, 0, 2, 19, 10, 15, 4, 11, 17, 0, 10, 4, 15, 11, 16, 4, 19, 15, 17, 10, 11, 5, 7, 4, 5, 15, 19, 18, 8, 14, 14, 4, 6, 19, 9, 10, 12, 15, 17, 0, 17, 19, 4, 2, 15, 11, 18, 7, 8, 8, 15, 2, 6, 0, 8, 1, 1, 15, 1, 6, 2, 15, 8, 12, 15, 1, 3, 8, 18, 11, 17, 4, 18, 18, 17, 1, 10, 19, 5, 10, 1, 16, 2, 7, 3, 2, 19, 8, 2, 11, 1, 1, 15, 18, 0, 5, 8, 13, 1, 19, 4, 3, 1, 14, 11, 11, 2, 5, 6, 12, 0, 4, 16, 14, 7, 6, 7, 17, 9, 11, 1, 17, 2, 1, 5, 7, 3, 4, 12, 1, 17, 9, 15, 8, 1, 4]
agent = TrainingAgent(render=True)
agent.play_with_chromosome(BEST_CHROMOSOME)


if __name__ == "__main__":
    main()