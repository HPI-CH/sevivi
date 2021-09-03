from enum import Enum


class StackingDirection(Enum):
    """ How to stack plots and source video, i.e., to place graphs below or right and left of the source video. """
    HORIZONTAL = 0
    """Place graphs right and left of the source video"""
    VERTICAL = 1
    """Place graphs below source video."""
