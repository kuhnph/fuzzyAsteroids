from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar


@dataclass
class NavigationSettings:
    MAX_AVOIDANCE_DISTANCE = 400