from dataclasses import dataclass, field
from typing import List

from sevivi.config import PlottingMethod, VideoConfig
from sevivi.config.config_types.sensor_config import SensorConfig
from sevivi.config.config_types.stacking_direction import StackingDirection


@dataclass
class Config:
    """Typed configuration for the entire tool."""
    video_config: VideoConfig = None
    data_configs: List[SensorConfig] = field(default_factory=list)
    stacking_direction: StackingDirection = StackingDirection.HORIZONTAL
    plotting_method: PlottingMethod = PlottingMethod.MOVING_VERTICAL_LINE
    parallel_image_ingestion: bool = False
    add_magnitude: bool = False
    draw_ticks: bool = False
