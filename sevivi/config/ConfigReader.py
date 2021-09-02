import copy
import os
from typing import List, Tuple

import toml

default_config = {
    "show_peak_finding_plots": False,
    "stack_direction": "horizontal",
    "draw_ticks": False,
    "add_magnitude": False,
    "add_events": True,
    "add_gyroscope": True,
    "use_parallel_image_ingestion": True,
    "plotting_method": "MOVING_VERTICAL_LINE"
}


class ConfigReader:

    def __init__(self, config_file_paths: Tuple[str, ...]):
        self.config = ConfigReader.read_configs(config_file_paths)

    @staticmethod
    def read_configs(config_file_paths: Tuple[str, ...]):
        config = copy.deepcopy(default_config)

        for path in config_file_paths:
            if not os.path.exists(path):
                raise FileNotFoundError(f"Missing configuration file {path}")
            else:
                config.update(toml.load(path))
        return config
