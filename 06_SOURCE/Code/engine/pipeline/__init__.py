"""Compatibility import surface for maintained Blue Line helpers.

Production detector modules use flat sibling imports; expose that directory
before importing their package-wrapped API. The normal Bridge path is unchanged.
"""

import sys
from pathlib import Path

_pipeline_dir = str(Path(__file__).resolve().parent)
if _pipeline_dir not in sys.path:
    sys.path.insert(0, _pipeline_dir)

from .blue_line_detector import (
    BlueLine,
    ScaleStrike,
    count_scale_strikes,
    detect_blue_lines,
    fibonacci_level,
)

__all__ = [
    "BlueLine",
    "ScaleStrike",
    "count_scale_strikes",
    "detect_blue_lines",
    "fibonacci_level",
]
