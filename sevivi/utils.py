from typing import List, Tuple

from sevivi.config import Config


def get_missing_files(config: Config) -> List[str]:
    """Returns a list of missing files. If no files are missing, the list is empty"""
    missing_files = config.video_config.get_missing_files()
    for sensor_config in config.sensor_configs:
        missing_files.extend(sensor_config.get_missing_files())
    return missing_files
