import numpy as np


def triangular(x, a, b, c):
    """
    Triangular fuzzy membership function.

    Parameters
    ----------
    x : float or np.ndarray
        Input value(s).
    a : float
        Left support point.
    b : float
        Peak point.
    c : float
        Right support point.

    Returns
    -------
    float or np.ndarray
        Membership value(s).
    """
    if isinstance(x, (int, float)):
        if x <= a or x > c:
            return 0.0
        elif a < x <= b:
            denom = (b - a)
            return 0.0 if denom == 0 else (x - a) / denom
        else:
            denom = (c - b)
            return 0.0 if denom == 0 else (c - x) / denom

    x = np.asarray(x, dtype=float)
    result = np.zeros_like(x, dtype=float)

    left_mask = (a < x) & (x <= b)
    right_mask = (b < x) & (x <= c)

    if b != a:
        result[left_mask] = (x[left_mask] - a) / (b - a)
    if c != b:
        result[right_mask] = (c - x[right_mask]) / (c - b)

    return result


def left_shoulder(x, a, b):
    """
    Left-shoulder fuzzy membership function.
    """
    if isinstance(x, (int, float)):
        if x < a:
            return 0.0
        elif x < b:
            denom = (b - a)
            return 0.0 if denom == 0 else (x - a) / denom
        else:
            return 1.0

    x = np.asarray(x, dtype=float)
    if b == a:
        return np.where(x < a, 0.0, 1.0)

    return np.where(x < a, 0.0, np.where(x < b, (x - a) / (b - a), 1.0))


def right_shoulder(x, a, b):
    """
    Right-shoulder fuzzy membership function.
    """
    if isinstance(x, (int, float)):
        if x <= a:
            return 1.0
        elif x < b:
            denom = (b - a)
            return 0.0 if denom == 0 else (b - x) / denom
        else:
            return 0.0

    x = np.asarray(x, dtype=float)
    if b == a:
        return np.where(x <= a, 1.0, 0.0)

    return np.where(x <= a, 1.0, np.where(x < b, (b - x) / (b - a), 0.0))