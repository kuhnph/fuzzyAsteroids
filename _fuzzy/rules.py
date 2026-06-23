"""
Fuzzy rule definitions.
"""


class FuzzyRule:
    def __init__(self, antecedents, consequents):
        """
        Parameters
        ----------
        antecedents : list[tuple[str, str]]
            Input conditions.

            Example:
            [
                ("heading_error", "left"),
                ("distance_error", "far")
            ]

        consequents : list[tuple[str, str]]
            Output commands.

            Example:
            [
                ("desired_turn_rate", "turn_left"),
                ("desired_speed", "slow")
            ]
        """
        self.antecedents = antecedents
        self.consequents = consequents

    def evaluate(self, fuzzified_inputs):
        """
        Compute the rule firing strength.

        Uses AND logic with min().

        Parameters
        ----------
        fuzzified_inputs : dict
            Example:
            {
                "heading_error": {
                    "left": 0.8,
                    "aligned": 0.2,
                },
                "distance_error": {
                    "near": 0.1,
                    "far": 0.9,
                }
            }

        Returns
        -------
        float
            Rule firing strength from 0 to 1.
        """
        strengths = []

        for variable_name, set_name in self.antecedents:
            strength = fuzzified_inputs[variable_name][set_name]
            strengths.append(strength)

        if not strengths:
            return 0.0

        return min(strengths)

    def __repr__(self):
        return (
            f"FuzzyRule("
            f"antecedents={self.antecedents}, "
            f"consequents={self.consequents}"
            f")"
        )