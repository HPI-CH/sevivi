from enum import Enum


class PlottingMethod(Enum):
    """The plotting method to use"""

    MOVING_VERTICAL_LINE = 0
    """
    The MOVING_VERTICAL_LINE plotting method is the fastest.
    The entire graph is shown for the entire video.
    A vertical line is moved through the graph to show the current moment in time.
    """
    PUSH_IN = 1
    """
    The PUSH_IN plotting method adds new sensor data on the right edge of the graph.
    This compresses the data on the left. The most recent data is always on the rightmost edge.
    """
