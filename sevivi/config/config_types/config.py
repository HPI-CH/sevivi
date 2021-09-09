from dataclasses import dataclass, field
from typing import List, Dict

from .video_config import VideoConfig
from .render_config import RenderConfig
from .sensor_config import SensorConfig


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
