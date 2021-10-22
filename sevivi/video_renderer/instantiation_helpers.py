"""Contains helpers to instantiate Video- and GraphImageProviders for the CLI"""

from typing import Dict, List

import pandas as pd

from sevivi.config import (
    CameraImuVideoConfig,
    VideoImuCaptureAppVideoConfig,
    KinectVideoConfig,
    RawVideoConfig,
    OpenPoseVideoConfig,
    VideoConfig,
    Config,
    RenderConfig,
    SensorConfig,
)
from sevivi.image_provider import (
    AzureProvider,
    GraphImageProvider,
    ImuCameraImageProvider,
    VideoImageProvider,
    PlainVideoImageProvider,
    VideoImuCaptureAppImageProvider,
)
from .video_renderer import VideoRenderer


def video_renderer_from_csv_files(config: Config) -> VideoRenderer:
    """Instantiate a VideoRenderer for Configs where all data is stored as .csv or .csv.gz"""
    missing_files = config.get_missing_files()
    if len(missing_files) > 0:
        raise FileNotFoundError(
            f"Your configuration points to the following files that are not available: {missing_files}"
        )

    video_provider = instantiate_video_provider(config.video_config)
    graph_providers = instantiate_graph_providers(
        config.sensor_configs, config.render_config
    )
    return VideoRenderer(config.render_config, video_provider, graph_providers)


def instantiate_graph_providers(
    sensor_configs: Dict[str, SensorConfig], render_config: RenderConfig
) -> List[GraphImageProvider]:
    """
    Instantiate a GraphImageProvider for each config.

    You must instantiate your GraphImageProviders manually if the data isn't stored as CSV or CSV.GZ where the
    first column is a DatetimeIndex
    """
    result = []

    for sc in sensor_configs.values():
        data = pd.read_csv(sc.path, index_col=0, parse_dates=True)
        result.append(GraphImageProvider(data, render_config, sc))

    return result


def instantiate_video_provider(video_config: VideoConfig) -> VideoImageProvider:
    """Instantiate the appropriate VideoImageProvider subclass for a given VideoConfig"""
    if isinstance(video_config, VideoImuCaptureAppVideoConfig):
        return VideoImuCaptureAppImageProvider(video_config.path, video_config.imu_path)
    elif isinstance(video_config, CameraImuVideoConfig):
        return ImuCameraImageProvider(video_config.path, video_config.imu_path)
    elif isinstance(video_config, KinectVideoConfig):
        return AzureProvider(
            video_config.path,
            video_config.skeleton_path_3d,
            video_config.skeleton_path_2d,
        )
    elif isinstance(video_config, RawVideoConfig):
        return PlainVideoImageProvider(video_config.path)
    elif isinstance(video_config, OpenPoseVideoConfig):
        raise NotImplementedError("OpenPoseVideoConfig Not Implemented")
    else:
        raise RuntimeError(
            f"Unknown instance type of VideoConfig: {type(video_config)}"
        )
