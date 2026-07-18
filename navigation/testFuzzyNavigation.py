from fuzzy.sets import TriangularSet, LeftShoulderSet, RightShoulderSet
from fuzzy.variables import FuzzyVariable
from fuzzy.rules import FuzzyRule
from fuzzy.controller import FuzzyController
from fuzzy.defuzz import weighted_average
from game.settings import GameSettings
import math


# -------------------------
# Inputs
# -------------------------
maxDistance = math.hypot(GameSettings.SCREEN_WIDTH, GameSettings.SCREEN_HEIGHT)
target_distance = FuzzyVariable(
    name="target_distance",
    minimum=0,
    maximum=maxDistance,
    sets={
        "near": LeftShoulderSet("near", 0, maxDistance*0.2),
        "medium": TriangularSet("medium", maxDistance*0.15, maxDistance*0.4, maxDistance*0.65),
        "far": RightShoulderSet("far", maxDistance*0.55, maxDistance)
    },
)


# -------------------------
# Outputs
# -------------------------
maxLookAhead = 300
pseudo_target_distance = FuzzyVariable(
name="pseudo_target_distance",
    minimum=0,
    maximum=max_lookahead,
    sets={
        "short": LeftShoulderSet("short", 0, max_lookahead*0.35,),
        "medium": TriangularSet("medium", maxLookAhead*0.20, maxLookAhead*0.50, maxLookAhead*0.80),
        "long": RightShoulderSet("long", max_lookahead*0.65, max_lookahead)
    },
)


# -------------------------
# Rules
# -------------------------

rules = [
    FuzzyRule(
        antecedents=[("target_distance", "near")],
        consequents=[("pseudo_target_distance", "short")]),

    FuzzyRule(
        antecedents=[("target_distance", "medium")],
        consequents=[("pseudo_target_distance", "medium")]),

    FuzzyRule(
        antecedents=[("target_distance", "far")],
        consequents=[("pseudo_target_distance", "long")]),
]