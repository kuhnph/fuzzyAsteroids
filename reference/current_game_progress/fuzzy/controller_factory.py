from .controller import FuzzyController
from .hand_tuned_controller import HandTunedFuzzyController


def build_controller(fuzzy_config):
    if fuzzy_config.controller_mode == fuzzy_config.genetic_controller_mode:
        return FuzzyController(fuzzy_config)

    if fuzzy_config.controller_mode == fuzzy_config.hand_tuned_controller_mode:
        return HandTunedFuzzyController(fuzzy_config)

    raise ValueError(
        f"Unknown fuzzy controller mode: {fuzzy_config.controller_mode}. "
        f"Expected {fuzzy_config.genetic_controller_mode!r} or "
        f"{fuzzy_config.hand_tuned_controller_mode!r}."
    )
