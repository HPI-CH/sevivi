from dataclasses import dataclass, field
from typing import List, Dict

from sevivi.config import PlottingMethod, VideoConfig
from sevivi.config.config_types.sensor_config import SensorConfig
from sevivi.config.config_types.stacking_direction import StackingDirection


@dataclass
class RenderConfig:
    """Contains configuration relevant for rendering"""

    stacking_direction: StackingDirection = StackingDirection.HORIZONTAL
    plotting_method: PlottingMethod = PlottingMethod.MOVING_VERTICAL_LINE
    parallel_image_ingestion: bool = False
    add_magnitude: bool = False
    draw_ticks: bool = False
    target_file_path: str = "sevivi.mp4"


@dataclass
class Config:
    """Typed configuration for the CLI. Contains render configuration as well as video and sensor config."""

    video_config: VideoConfig = None
    sensor_configs: Dict[str, SensorConfig] = field(default_factory=dict)
    render_config: RenderConfig = None

    def get_missing_files(self) -> List[str]:
        """
        Returns a list of missing files in this config.
        If no files are missing, the list is empty
        """
        missing_files = self.video_config.get_missing_files()
        for sensor_config in self.sensor_configs.values():
            missing_files.extend(sensor_config.get_missing_files())
        return missing_files
