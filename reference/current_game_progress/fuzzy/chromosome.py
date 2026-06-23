import numpy as np
from dataclasses import dataclass

from .membership import triangular
from config.fuzzy_config import ChromosomeConfig


def genes_needed_for_memberships(n_sets):
    return 2 * n_sets - 2


def map_value(value, from_low, from_high, to_low, to_high):
    """
    Linearly map a value from one range into another.
    """
    if from_high == from_low:
        raise ValueError("from_high and from_low must be different")

    normalized = (value - from_low) / (from_high - from_low)
    return normalized * (to_high - to_low) + to_low


def decode_chromosome(chromosome, config: ChromosomeConfig):
    """
    Split one full chromosome into its major sections.

    Returns
    -------
    position_genes
    speed_genes
    rule_genes
    output_genes
    """
    if len(chromosome) != config.length:
        raise ValueError(
            f"Expected chromosome length {config.length}, got {len(chromosome)}"
        )

    i = 0

    position_genes = chromosome[i:i + config.position_gene_count]
    i += config.position_gene_count

    speed_genes = chromosome[i:i + config.speed_gene_count]
    i += config.speed_gene_count

    rule_genes = chromosome[i:i + config.rule_gene_count]
    i += config.rule_gene_count

    output_genes = chromosome[i:i + config.output_gene_count]


    return position_genes, speed_genes, rule_genes, output_genes


def decode_triangular_sets(chromosome, map_min, map_max, n_sets):
    """
    Decode chromosome genes into triangular/shoulder fuzzy sets.

    For n_sets fuzzy sets, this expects:

        genes = 2*n_sets - 2

    The first and last sets are shoulders:

        first set: [center, center, right]
        middle sets: [left, center, right]
        last set: [left, center, center]

    Returns
    -------
    sets : list[list[float]]
        Each set is [left, center, right].
    """
    required_genes = genes_needed_for_memberships(n_sets)

    if len(chromosome) != required_genes:
        raise ValueError(
            f"Expected {required_genes} genes for {n_sets} sets, "
            f"got {len(chromosome)}"
        )

    centers = np.linspace(map_min, map_max, n_sets)
    max_width = (map_max - map_min) / n_sets

    widths = [
        map_value(
            value=gene,
            from_low=0,
            from_high=n_sets - 1,
            to_low=0,
            to_high=max_width,
        )
        for gene in chromosome
    ]

    sets = []
    gene_index = 0

    for set_index in range(n_sets):
        center = centers[set_index]

        if set_index == 0:
            left = center
            right = center + widths[gene_index]
            gene_index += 1

        elif set_index == n_sets - 1:
            left = center - widths[gene_index]
            right = center
            gene_index += 1

        else:
            left = center - widths[gene_index]
            gene_index += 1

            right = center + widths[gene_index]
            gene_index += 1

        sets.append([left, center, right])

    return sets


def decode_input_membership(value, chromosome, map_min, map_max, n_sets):
    """
    Decode chromosome genes into fuzzy input membership values.

    Returns
    -------
    memberships : list[float]
        Degree of membership for each fuzzy set.
    """
    sets = decode_triangular_sets(
        chromosome=chromosome,
        map_min=map_min,
        map_max=map_max,
        n_sets=n_sets,
    )

    return [
        triangular(value, left, center, right)
        for left, center, right in sets
    ]


def decode_output_membership(chromosome, map_min, map_max, n_sets):
    """
    Decode chromosome genes into fuzzy output sets.

    Returns
    -------
    output_sets : list[list[float]]
        Each output set is [left, center, right].
    """
    return decode_triangular_sets(
        chromosome=chromosome,
        map_min=map_min,
        map_max=map_max,
        n_sets=n_sets,
    )


def decode_rules(x_memberships, y_memberships, chromosome, n_sets):
    """
    Decode a 2-input fuzzy rule table.

    Each rule gene assigns the activation:

        min(x_i, y_j)

    into one output bucket.
    """
    expected_rules = len(x_memberships) * len(y_memberships)

    if len(chromosome) != expected_rules:
        raise ValueError(
            f"Rule decoder expected {expected_rules} genes, "
            f"got {len(chromosome)}"
        )

    memberships = [[] for _ in range(n_sets)]

    gene_index = 0

    for x_val in x_memberships:
        for y_val in y_memberships:
            output_bucket = chromosome[gene_index]

            if output_bucket < 0 or output_bucket >= n_sets:
                raise ValueError(
                    f"Rule gene {gene_index} has invalid output bucket "
                    f"{output_bucket}. Expected 0 to {n_sets - 1}."
                )

            memberships[output_bucket].append(min(x_val, y_val))
            gene_index += 1

    return memberships
