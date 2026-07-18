"""
Membership functions used by the fuzzy controller.
"""


class TriangularSet:
    def __init__(self, name, left, center, right):
        self.name = name
        self.left = left
        self.center = center
        self.right = right

    def membership(self, x):
        if x <= self.left or x >= self.right:
            return 0.0

        if x == self.center:
            return 1.0

        if x < self.center:
            return (x - self.left) / (self.center - self.left)

        return (self.right - x) / (self.right - self.center)


class LeftShoulderSet:
    def __init__(self, name, left, right):
        """
        Full membership to the left of `left`.
        Decreases linearly to zero at `right`.
        """
        self.name = name
        self.left = left
        self.right = right

    def membership(self, x):
        if x <= self.left:
            return 1.0

        if x >= self.right:
            return 0.0

        return (self.right - x) / (self.right - self.left)


class RightShoulderSet:
    def __init__(self, name, left, right):
        """
        Zero membership to the left of `left`.
        Increases linearly to full membership at `right`.
        """
        self.name = name
        self.left = left
        self.right = right

    def membership(self, x):
        if x <= self.left:
            return 0.0

        if x >= self.right:
            return 1.0

        return (x - self.left) / (self.right - self.left)