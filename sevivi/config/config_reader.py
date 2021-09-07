import collections
import logging
import os
from pprint import pformat
from typing import Tuple, Dict

import pandas as pd
import toml

from sevivi.config import PlottingMethod, Config, VideoConfig, RenderConfig
from sevivi.config.config_types.sensor_config import (
    SensorConfig,
    ManuallySynchronizedSensorConfig,
    JointSynchronizedSensorConfig,
    ImuSynchronizedSensorConfig,
)
from sevivi.config.config_types.stacking_direction import StackingDirection
from sevivi.config.config_types.video_config import (
    CameraImuVideoConfig,
    KinectVideoConfig,
    RawVideoConfig,
    OpenPoseVideoConfig,
)

logger = logging.getLogger("sevivi.config_reader")


def merge_config_files(config_file_paths: Tuple[str, ...]) -> Dict:
    config_dict = {}

    for path in config_file_paths:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing configuration file {path}")
        else:
            update = toml.load(path)

            # In theory we could manually merge the video configurations;
            # However, I can't really think of a use case. The behaviour for
            # sensors is to just add all configured sensors together, which
            # is not wanted for video config.
            if "video" in update and "video" in config_dict:
                logger.info("Only the latest video config is used")
                del config_dict["video"]

            deep_update(config_dict, update)
    return config_dict


def read_configs(config_file_paths: Tuple[str, ...]) -> Config:
    if config_file_paths is None or len(config_file_paths) == 0:
        raise ValueError(
            "At least one config file is required to set video and data sources"
        )

    config_dict = merge_config_files(config_file_paths)
    render_config = RenderConfig()

    if "target_file_path" in config_dict:
        render_config.target_file_path = config_dict["target_file_path"]
    if "draw_ticks" in config_dict:
        render_config.draw_ticks = get_bool(config_dict, "draw_ticks")
    if "add_magnitude" in config_dict:
        render_config.add_magnitude = get_bool(config_dict, "add_magnitude")
    if "use_parallel_image_ingestion" in config_dict:
        render_config.use_parallel_image_ingestion = get_bool(
            config_dict, "use_parallel_image_ingestion"
        )

    if "plotting_method" in config_dict:
        render_config.plotting_method = get_plotting_method(config_dict)
    if "stacking_direction" in config_dict:
        render_config.stacking_direction = get_stacking_direction(config_dict)

    config = Config()
    config.render_config = render_config

    if "video" in config_dict:
        config.video_config = get_video_config(config_dict)
    else:
        raise ValueError(
            "Missing video parameter. "
            "You need to supply a video to render the graphs next to."
        )

    if "sensor" in config_dict:
        config.sensor_configs = get_sensor_configs(config_dict)
    else:
        raise ValueError(
            "Missing sensor parameters. "
            "You need to supply at least one sensor to render next to the video."
        )

    return config


def deep_update(source, overrides):
    """
    Update a nested dictionary or similar mapping.
    Modify ``source`` in place.

    From Nate Glenn, user2709610, charlax, surjikal

    https://stackoverflow.com/a/18394648
    https://stackoverflow.com/a/30655448
    """
    for key, value in overrides.items():
        if isinstance(value, collections.Mapping) and value:
            returned = deep_update(source.get(key, {}), value)
            source[key] = returned
        elif isinstance(value, list):
            source[key] = source.get(key, []) + value
        else:
            source[key] = overrides[key]
    return source


def get_video_config(cfg: Dict) -> VideoConfig:
    try:
        cfg = cfg["video"][0]
        cfg_type = cfg["type"]
        if cfg_type == "imu":
            result = CameraImuVideoConfig()
            result.imu_path = cfg["imu_path"]
            result.camera_imu_sync_column = cfg["camera_imu_sync_column"]
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
    except KeyError as e:
        raise KeyError(f"Missing key '{e.args[0]}' in video config: {pformat(cfg)}")
    return result


def get_sensor_configs(config_dict: Dict) -> Dict[str, SensorConfig]:
    result_dict = {}
    i, cfg = None, None
    try:
        config_dict = config_dict["sensor"]
        for i, cfg in enumerate(config_dict):
            cfg_type = cfg["type"]
            if cfg_type == "manually-synced":
                result = ManuallySynchronizedSensorConfig()
                result.offset_seconds = cfg.get("offset_seconds", result.offset_seconds)
            elif cfg_type == "camera-imu-synced":
                result = ImuSynchronizedSensorConfig()
                result.sensor_sync_column = cfg["sensor_sync_column"]
            elif cfg_type == "joint-synced":
                result = JointSynchronizedSensorConfig()
                result.sync_joint_name = cfg["sync_joint_name"]
                result.sensor_sync_axes = cfg["sensor_sync_axes"]
                result.joint_sync_axis = cfg["joint_sync_axis"]
            else:
                raise ValueError(f"Unknown sensor config type {cfg_type}")

            if "start_time" in cfg:
                result.start_time = pd.to_datetime(cfg["start_time"])
            if "end_time" in cfg:
                result.end_time = pd.to_datetime(cfg["end_time"])

            result.path = cfg["path"]
            result_dict[str(i)] = result
    except KeyError as e:
        raise KeyError(
            f"Missing key '{e.args[0]}' in sensor config {i}: {pformat(cfg)}"
        )

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
