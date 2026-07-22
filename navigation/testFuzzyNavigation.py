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

maxDistance = math.hypot(
    GameSettings.SCREEN_WIDTH,
    GameSettings.SCREEN_HEIGHT
)

target_distance = FuzzyVariable(
    name="target_distance",
    minimum=1,
    maximum=maxDistance,
    sets={
        "near": LeftShoulderSet("near",1,maxDistance*0.20,),
        "medium": TriangularSet("medium",maxDistance*0.15,maxDistance*0.40,maxDistance*0.65,),
        "far": RightShoulderSet("far",maxDistance*0.55,maxDistance,)
    }
)


max_avoidance_distance = 400

asteroid_clearance = FuzzyVariable(
    name="asteroid_clearance",
    minimum=0,
    maximum=max_avoidance_distance,
    sets={
        "critical": LeftShoulderSet("critical",0,max_avoidance_distance*0.20,),
        "near": TriangularSet("near",max_avoidance_distance*0.10,max_avoidance_distance*0.35,max_avoidance_distance*0.60,),
        "far": RightShoulderSet("far",max_avoidance_distance*0.45,max_avoidance_distance,)
    }
)


asteroid_bearing = FuzzyVariable(
    name="asteroid_bearing",
    minimum=-180,
    maximum=180,
    sets={
        "behind_left": LeftShoulderSet("behind_left",-180,-120,),
        "left": TriangularSet("left",-160,-75,-15,),
        "ahead": TriangularSet("ahead",-35,0,35,),
        "right": TriangularSet("right",15,75,160,),
        "behind_right": RightShoulderSet("behind_right",120,180,)
    }
)


# -------------------------
# Outputs
# -------------------------

maxLookAhead = 10

pseudo_target_distance = FuzzyVariable(
    name="pseudo_target_distance",
    minimum=1,
    maximum=maxLookAhead,
    sets={
        "short": LeftShoulderSet("short",1,maxLookAhead*0.35,),
        "medium": TriangularSet("medium",maxLookAhead*0.20,maxLookAhead*0.50,maxLookAhead*0.80,),
        "long": RightShoulderSet("long",maxLookAhead*0.65,maxLookAhead,)
    }
)


avoidance_offset = FuzzyVariable(
    name="avoidance_offset",
    minimum=-90,
    maximum=90,
    sets={
        "hard_left": LeftShoulderSet("hard_left",-90,-45,),
        "left": TriangularSet("left",-60,-30,0,),
        "zero": TriangularSet("zero",-10,0,10,),
        "right": TriangularSet("right",0,30,60,),
        "hard_right": RightShoulderSet("hard_right",45,90,)
    }
)


avoidance_rules = [
    # Ignore asteroids behind Peach
    FuzzyRule(
        antecedents=[("asteroid_bearing","behind_left")],
        consequents=[("avoidance_offset","zero")]),
    FuzzyRule(
        antecedents=[("asteroid_bearing","behind_right")],
        consequents=[("avoidance_offset","zero")]),
    # Asteroid is off to one side
    FuzzyRule(
        antecedents=[("asteroid_bearing","left")],
        consequents=[("avoidance_offset","right")]),
    FuzzyRule(
        antecedents=[("asteroid_bearing","right")],
        consequents=[("avoidance_offset","left")]),
    # Directly ahead
    FuzzyRule(
        antecedents=[("asteroid_bearing","ahead")],
        consequents=[("avoidance_offset","hard_right")]),
    # Far away -> don't avoid
    FuzzyRule(
        antecedents=[("asteroid_clearance","far")],
        consequents=[("avoidance_offset","zero")]),
]

lookahead_rules = [
    FuzzyRule(
        antecedents=[("target_distance","near")],
        consequents=[("pseudo_target_distance","short")]),
    FuzzyRule(
        antecedents=[("target_distance","medium")],
        consequents=[("pseudo_target_distance","medium")]),
    FuzzyRule(
        antecedents=[("target_distance","far")],
        consequents=[("pseudo_target_distance","long")]),
    # Obstacle nearby -> shorten the waypoint
    FuzzyRule(
        antecedents=[("asteroid_clearance","near")],
        consequents=[("pseudo_target_distance","short")]),
    FuzzyRule(
        antecedents=[("asteroid_clearance","critical")],
        consequents=[("pseudo_target_distance","short")]),
]

look_ahead = FuzzyController(
    input_variables=[
        target_distance,
        asteroid_clearance
    ],
    output_variables=[
        pseudo_target_distance
    ],
    rules=lookahead_rules,
    defuzzifier=weighted_average,
)

avoidance = FuzzyController(
    input_variables=[
        asteroid_bearing,
        asteroid_clearance
    ],
    output_variables=[
        avoidance_offset
    ],
    rules=avoidance_rules,
    defuzzifier=weighted_average,
)