"""
Fuzzy input/output variable definitions.
"""


class FuzzyVariable:
    def __init__(self, name, minimum, maximum, sets):
        """
        Parameters
        ----------
        name : str
            Variable name.

        minimum : float
            Minimum valid value.

        maximum : float
            Maximum valid value.

        sets : dict
            Dictionary of membership functions.

            Example:
            {
                "slow": SlowSet,
                "medium": MediumSet,
                "fast": FastSet
            }
        """
        self.name = name
        self.minimum = minimum
        self.maximum = maximum
        self.sets = sets

    def fuzzify(self, value):
        """
        Calculate membership in every set.

        Returns
        -------
        dict

        Example:
        {
            "slow": 0.2,
            "medium": 0.8,
            "fast": 0.0
        }
        """
        memberships = {}

        for set_name, fuzzy_set in self.sets.items():
            memberships[set_name] = fuzzy_set.membership(value)

        return memberships

    def __repr__(self):
        return (
            f"FuzzyVariable("
            f"name='{self.name}', "
            f"min={self.minimum}, "
            f"max={self.maximum}, "
            f"sets={list(self.sets.keys())}"
            f")"
        )