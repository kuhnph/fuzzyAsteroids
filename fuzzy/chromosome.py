import numpy as np

from .membership import triangular


def map_value(value, from_low, from_high, to_low, to_high):
    """
    Linearly map a value from one range into another.
    """
    if from_high == from_low:
        raise ValueError("from_high and from_low must be different")

    normalized = (value - from_low) / (from_high - from_low)
    return normalized * (to_high - to_low) + to_low


def decode_input_membership(value, chromosome, map_min, map_max, n_sets=5):
    """
    Decode 8 chromosome values into 5 triangular input membership functions.

    This mirrors your original layout:
        set1 uses gene[0]
        set2 uses gene[1], gene[2]
        set3 uses gene[3], gene[4]
        set4 uses gene[5], gene[6]
        set5 uses gene[7]
    """
    if len(chromosome) != 8:
        raise ValueError("Input membership decoder expects exactly 8 genes")

    widths = [
        map_value(gene, 0, n_sets - 1, map_min, map_max / n_sets)
        for gene in chromosome
    ]

    centers = np.linspace(map_min, map_max, n_sets)

    x1 = triangular(value, centers[0], centers[0], centers[0] + widths[0])
    x2 = triangular(value, centers[1] - widths[1], centers[1], centers[1] + widths[2])
    x3 = triangular(value, centers[2] - widths[3], centers[2], centers[2] + widths[4])
    x4 = triangular(value, centers[3] - widths[5], centers[3], centers[3] + widths[6])
    x5 = triangular(value, centers[4] - widths[7], centers[4], centers[4])

    return [x1, x2, x3, x4, x5]


def decode_output_membership(chromosome, map_min, map_max, n_sets=5):
    """
    Decode 8 chromosome values into 5 triangular output membership functions.

    Returns a list of triangles:
        [left, center, right]
    """
    if len(chromosome) != 8:
        raise ValueError("Output membership decoder expects exactly 8 genes")

    widths = [
        map_value(gene, 0, n_sets - 1, map_min, map_max / n_sets)
        for gene in chromosome
    ]

    centers = np.linspace(map_min, map_max, n_sets)

    z1 = [centers[0], centers[0], centers[0] + widths[0]]
    z2 = [centers[1] - widths[1], centers[1], centers[1] + widths[2]]
    z3 = [centers[2] - widths[3], centers[2], centers[2] + widths[4]]
    z4 = [centers[3] - widths[5], centers[3], centers[3] + widths[6]]
    z5 = [centers[4] - widths[7], centers[4], centers[4]]

    return [z1, z2, z3, z4, z5]


def decode_rules(x_memberships, y_memberships, chromosome, n_rules=5):
    """
    Decode a 2-input fuzzy rule table from chromosome genes.

    Each gene assigns the rule activation min(x_i, y_j) into one of the
    output buckets 0..n_rules-1.
    """
    expected_rules = len(x_memberships) * len(y_memberships)
    if len(chromosome) != expected_rules:
        raise ValueError(
            f"Rule decoder expected {expected_rules} genes, got {len(chromosome)}"
        )

    memberships = [[] for _ in range(n_rules)]

    gene_index = 0
    for x_val in x_memberships:
        for y_val in y_memberships:
            output_bucket = chromosome[gene_index]
            memberships[output_bucket].append(min(x_val, y_val))
            gene_index += 1

    return memberships