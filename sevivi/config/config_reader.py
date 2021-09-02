import copy
import os
from typing import List, Tuple, Optional

import toml

from sevivi.config import PlottingMethod, StackingDirection

default_config = {
    "show_peak_finding_plots": False,
    "stacking_direction": "horizontal",
    "draw_ticks": False,
    "add_magnitude": False,
    "add_events": True,
    "add_gyroscope": True,
    "use_parallel_image_ingestion": True,
    "plotting_method": "MOVING_VERTICAL_LINE"
}


class ConfigReader:

    def __init__(self, config_file_paths: Optional[Tuple[str, ...]] = None):
        self.config = ConfigReader.read_configs(config_file_paths)

    @staticmethod
    def read_configs(config_file_paths: Optional[Tuple[str, ...]] = None):
        config = copy.deepcopy(default_config)

        if config_file_paths is None:
            config_file_paths = ()

        for path in config_file_paths:
            if not os.path.exists(path):
                raise FileNotFoundError(f"Missing configuration file {path}")
            else:
                config.update(toml.load(path))
        return config

    def get_bool(self, key_name: str) -> bool:
        value = self.config[key_name]
        if isinstance(value, bool):
            return value
        else:
            raise ValueError(f"Configuration value {value} for key {key_name} is not a boolean")

    def get_plotting_method(self) -> PlottingMethod:
        config_plotting_method = self.config.get('plotting_method', "N/A")
        try:
            return PlottingMethod[config_plotting_method.upper()]
        except KeyError:
            raise KeyError(f"Could not parse plotting_method {config_plotting_method}")

    def get_stacking_direction(self) -> StackingDirection:
        config_stacking_direction = self.config.get('stacking_direction', "N/A")
        try:
            return StackingDirection[config_stacking_direction.upper()]
        except KeyError:
            raise KeyError(f"Could not parse stacking_direction {config_stacking_direction}")
