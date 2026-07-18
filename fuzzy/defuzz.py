"""
Defuzzification methods.
"""


def weighted_average(output_variable, activations):
    """
    Defuzzify using weighted average of output set centers.

    Parameters
    ----------
    output_variable : FuzzyVariable
        Output variable containing fuzzy sets.

    activations : dict
        Output set activation strengths.

        Example:
        {
            "slow": 0.2,
            "medium": 0.8,
            "fast": 0.0
        }

    Returns
    -------
    float
        Crisp output value.
    """
    numerator = 0.0
    denominator = 0.0

    for set_name, strength in activations.items():
        fuzzy_set = output_variable.sets[set_name]

        # Assumes every output set has a center value.
        center = fuzzy_set.center

        numerator += strength * center
        denominator += strength

    if denominator == 0.0:
        return 0.0

    return numerator / denominator