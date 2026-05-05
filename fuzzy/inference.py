import numpy as np


def sum_list_of_lists(values):
    total = 0.0
    for sublist in values:
        for value in sublist:
            total += value
    return total


def scaled_output_centroid(rule_memberships, output_sets):
    """
    Defuzzify using the same scaled-area approach used in your original code.

    Parameters
    ----------
    rule_memberships : list[list[float]]
        Membership activations grouped by output set.
    output_sets : list[list[float]]
        Each output set is [left, center, right].

    Returns
    -------
    float
        Crisp output value.
    """
    areas = [[] for _ in range(len(rule_memberships))]

    for set_index in range(len(rule_memberships)):
        left, center, right = output_sets[set_index]
        base_width = right - left

        for mu in rule_memberships[set_index]:
            areas[set_index].append(0.5 * mu * base_width)

    union_area = sum_list_of_lists(areas)

    if union_area == 0:
        return 0.0

    numerator = 0.0
    for set_index, area_list in enumerate(areas):
        center_value = output_sets[set_index][1]
        for area in area_list:
            numerator += area * center_value

    result = numerator / union_area

    if np.isnan(result):
        return 0.0

    return float(result)
