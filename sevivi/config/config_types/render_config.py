from dataclasses import dataclass

from .stacking_direction import StackingDirection
from .plotting_method import PlottingMethod


@dataclass
class RenderConfig:
    """Contains configuration relevant for rendering"""

    stacking_direction: StackingDirection = StackingDirection.HORIZONTAL
    plotting_method: PlottingMethod = PlottingMethod.MOVING_VERTICAL_LINE
    parallel_image_ingestion: bool = False
    add_magnitude: bool = False
    draw_ticks: bool = False
    target_file_path: str = "sevivi.mp4"
    plot_column_count = 2
    """Number of columns to use in the plots. Should be divisible by 2 for StackingDirection.HORIZONTAL"""
