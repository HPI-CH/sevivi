from dataclasses import dataclass

from .stacking_direction import StackingDirection
from .plotting_method import PlottingMethod


@dataclass
class RenderConfig:
    """Contains configuration relevant for rendering"""

    stacking_direction: StackingDirection = StackingDirection.HORIZONTAL
    """Should the plots be next to or below the input video?"""
    plotting_method: PlottingMethod = PlottingMethod.MOVING_VERTICAL_LINE
    """The plotting method to use, i.e., how should changes in time be shown?"""
    target_file_path: str = "sevivi.avi"
    """Path where the resulting video file should be stored"""
    fourcc_codec: str = "MJPG"
    """Fourcc (check OpenCV docs) codec of the resulting video"""
    plot_column_count = 2
    """Number of columns to use in the plots. Should be divisible by 2 for StackingDirection.HORIZONTAL"""
