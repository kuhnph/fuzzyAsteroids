from fuzzy.sets import TriangularSet, LeftShoulderSet, RightShoulderSet
from fuzzy.variables import FuzzyVariable
from fuzzy.rules import FuzzyRule
from fuzzy.controller import FuzzyController
from fuzzy.defuzz import weighted_average



# -------------------------
# Inputs
# -------------------------

heading_error = FuzzyVariable(
    name="heading_error",
    minimum=-180,
    maximum=180,
    sets={
        "hard_left": LeftShoulderSet("hard_left", -180, -60),
        "left": TriangularSet("left", -120, -45, 0),
        "aligned": TriangularSet("aligned", -15, 0, 15),
        "right": TriangularSet("right", 0, 45, 120),
        "hard_right": RightShoulderSet("hard_right", 60, 180),
    },
)

distance_error = FuzzyVariable(
    name="distance_error",
    minimum=0,
    maximum=250,
    sets={
        "here": LeftShoulderSet("near", 0, 5),
        "near": LeftShoulderSet("near", 0, 50),
        "medium": TriangularSet("medium", 50, 100, 150),
        "far": RightShoulderSet("far", 125, 250),
    },
)

speed = FuzzyVariable(
    name="speed",
    minimum=0,
    maximum=5,
    sets={
        "slow": LeftShoulderSet("slow", 0, 1.5),
        "medium": TriangularSet("medium", 1.0, 2.5, 4.0),
        "fast": RightShoulderSet("fast", 3.0, 5.0),
    },
)


# -------------------------
# Outputs
# -------------------------

desired_turn_rate = FuzzyVariable(
    name="desired_turn_rate",
    minimum=-180,
    maximum=180,
    sets={
        "hard_left": TriangularSet("hard_left", -180, -180, -90),
        "left": TriangularSet("left", -140, -70, 0),
        "zero": TriangularSet("zero", -20, 0, 20),
        "right": TriangularSet("right", 0, 70, 140),
        "hard_right": TriangularSet("hard_right", 90, 180, 180),
    },
)

desired_speed = FuzzyVariable(
    name="desired_speed",
    minimum=0,
    maximum=5,
    sets={
        "stop": LeftShoulderSet("stop", 0, .5),
        "slow": TriangularSet("slow", 0.2, 1.5, 2.5),
        "medium": TriangularSet("medium", 2.0, 3.0, 4.0),
        "fast": TriangularSet("fast", 3.5, 5.0, 5.0),
    },
)


# -------------------------
# Rules
# -------------------------

rules = [
    # Turning
    FuzzyRule(
        antecedents=[("heading_error", "hard_left")],
        consequents=[("desired_turn_rate", "hard_left")],
    ),
    FuzzyRule(
        antecedents=[("heading_error", "left")],
        consequents=[("desired_turn_rate", "left")],
    ),
    FuzzyRule(
        antecedents=[("heading_error", "aligned")],
        consequents=[("desired_turn_rate", "zero")],
    ),
    FuzzyRule(
        antecedents=[("heading_error", "right")],
        consequents=[("desired_turn_rate", "right")],
    ),
    FuzzyRule(
        antecedents=[("heading_error", "hard_right")],
        consequents=[("desired_turn_rate", "hard_right")],
    ),

    # Speed
    FuzzyRule(
        antecedents=[
            ("heading_error", "aligned"),
            ("distance_error", "far"),
        ],
        consequents=[("desired_speed", "fast")],
    ),
    FuzzyRule(
        antecedents=[
            ("heading_error", "aligned"),
            ("distance_error", "medium"),
        ],
        consequents=[("desired_speed", "medium")],
    ),
    FuzzyRule(
        antecedents=[
            ("distance_error", "near"),
        ],
        consequents=[("desired_speed", "slow")],
    ),
    FuzzyRule(
        antecedents=[
            ("distance_error", "here"),
        ],
        consequents=[("desired_speed", "stop")],
    ),
    FuzzyRule(
        antecedents=[
            ("heading_error", "hard_left"),
        ],
        consequents=[("desired_speed", "slow")],
    ),
    FuzzyRule(
        antecedents=[
            ("heading_error", "hard_right"),
        ],
        consequents=[("desired_speed", "slow")],
    ),
]


# -------------------------
# Controller
# -------------------------

vehicle_controller = FuzzyController(
    input_variables=[
        heading_error,
        distance_error,
        speed,
    ],
    output_variables=[
        desired_turn_rate,
        desired_speed,
    ],
    rules=rules,
    defuzzifier=weighted_average,
)
