import collections
import os
from typing import Tuple, Optional, Dict

import pandas as pd
import toml

from sevivi.config import PlottingMethod, Config, VideoConfig
from sevivi.config.config_types.sensor_config import SensorConfig, ManuallySynchronizedSensorConfig, \
    JointSynchronizedSensorConfig
from sevivi.config.config_types.stacking_direction import StackingDirection
from sevivi.config.config_types.video_config import CameraImuVideoConfig, KinectVideoConfig, RawVideoConfig, \
    OpenPoseVideoConfig


def merge_config_files(config_file_paths: Optional[Tuple[str, ...]] = None) -> Dict:
    config_dict = {}

    if config_file_paths is None:
        config_file_paths = ()

    for path in config_file_paths:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing configuration file {path}")
        else:
            deep_update(config_dict, toml.load(path))
    return config_dict


def read_configs(config_file_paths: Optional[Tuple[str, ...]] = None) -> Config:
    config_dict = merge_config_files(config_file_paths)
    config = Config()

    if "draw_ticks" in config_dict:
        config.draw_ticks = get_bool(config_dict, "draw_ticks")
    if "add_magnitude" in config_dict:
        config.add_magnitude = get_bool(config_dict, "add_magnitude")
    if "use_parallel_image_ingestion" in config_dict:
        config.use_parallel_image_ingestion = get_bool(config_dict, "use_parallel_image_ingestion")

    if "plotting_method" in config_dict:
        config.plotting_method = get_plotting_method(config_dict)
    if "stacking_direction" in config_dict:
        config.stacking_direction = get_stacking_direction(config_dict)

    if "video" in config_dict:
        config.video_config = get_video_config(config_dict)
    else:
        raise ValueError("Missing video parameter. You need to supply a video to render next to.")

    if "data" in config_dict:
        config.data_configs = get_data_config(config_dict)
    else:
        raise ValueError("Missing Video parameter. You need to supply a video to render next to.")

    return config


def deep_update(source, overrides):
    """
    Update a nested dictionary or similar mapping.
    Modify ``source`` in place.

    From Nate Glenn, user2709610, charlax, surjikal

    https://stackoverflow.com/a/18394648
    https://stackoverflow.com/a/30655448
    """
    for key, value in overrides.iteritems():
        if isinstance(value, collections.Mapping) and value:
            returned = deep_update(source.get(key, {}), value)
            source[key] = returned
        elif isinstance(value, list):
            source[key] = (source.get(key, []) + value)
        else:
            source[key] = overrides[key]
    return source


def get_video_config(cfg: Dict) -> VideoConfig:
    cfg_type = cfg["type"]
    if cfg_type == "imu":
        result = CameraImuVideoConfig()
        result.imu_path = cfg["imu_path"]
        result.sync_column = cfg["sync_column"]
    elif cfg_type == "kinect":
        result = KinectVideoConfig()
        result.skeleton_path = cfg["skeleton_path"]
    elif cfg_type == "raw":
        result = RawVideoConfig()
    elif cfg_type == "openpose":
        result = OpenPoseVideoConfig()
    else:
        raise ValueError(f"Unknown video config type {cfg_type}")

    result.path = cfg["path"]
    return result


def get_data_config(config_dict: Dict) -> Dict[str, SensorConfig]:
    result_dict = {}

    for name, cfg in config_dict.items():
        cfg_type = cfg["type"]
        if cfg_type == "manually-synced":
            result = ManuallySynchronizedSensorConfig()
            result.offset_seconds = cfg.get("offset_seconds", result.offset_seconds)
        elif cfg_type == "camera-imu-synced":
            result = CameraImuVideoConfig()
            result.imu_path = cfg["imu_path"]
            result.sync_column = cfg["sync_column"]
        elif cfg_type == "joint-synced":
            result = JointSynchronizedSensorConfig()
            result.sync_joint_name = cfg["sync_joint_name"]
            result.sync_axis_column = cfg["sync_axis_column"]
            result.joint_sync_axis = cfg["joint_sync_axis"]
        else:
            raise ValueError(f"Unknown sensor config type {cfg_type}")

        if "start_time" in cfg:
            result.start_time = pd.to_datetime(cfg["start_time"])
        if "end_time" in cfg:
            result.end_time = pd.to_datetime(cfg["end_time"])

        result_dict[name] = result

    return result_dict


def get_bool(config_dict: Dict, key_name: str) -> bool:
    value = config_dict[key_name]
    if isinstance(value, bool):
        return value
    else:
        raise ValueError(
            f"Configuration value {value} for key {key_name} is not a boolean"
        )


def get_plotting_method(config_dict: Dict) -> PlottingMethod:
    config_plotting_method = config_dict.get("plotting_method", "N/A")
    try:
        return PlottingMethod[config_plotting_method.upper()]
    except KeyError:
        raise KeyError(f"Could not parse plotting_method {config_plotting_method}")


def get_stacking_direction(config_dict: Dict) -> StackingDirection:
    config_stacking_direction = config_dict.get("stacking_direction", "N/A")
    try:
        return StackingDirection[config_stacking_direction.upper()]
    except KeyError:
        raise KeyError(
            f"Could not parse stacking_direction {config_stacking_direction}"
        )
