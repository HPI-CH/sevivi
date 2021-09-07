"""Contains helpers to instantiate Video- and GraphImageProviders for the CLI"""

from typing import Dict

import pandas as pd

from sevivi.config import Config
from sevivi.config.config_types.sensor_config import (
    ManuallySynchronizedSensorConfig,
    ImuSynchronizedSensorConfig,
    JointSynchronizedSensorConfig,
    SensorConfig,
)
from sevivi.config.config_types.video_config import (
    CameraImuVideoConfig,
    KinectVideoConfig,
    RawVideoConfig,
    OpenPoseVideoConfig,
    VideoConfig,
)
from sevivi.image_provider import AzureProvider
from sevivi.image_provider.graph_provider import (
    CameraImuSyncedGraphProvider,
    JointSyncedGraphProvider,
    ManuallySyncedGraphProvider,
)
from sevivi.image_provider.graph_provider.graph_provider import GraphImageProvider
from sevivi.image_provider.video_provider.video_provider import VideoImageProvider
from sevivi.video_renderer.video_renderer import VideoRenderer


def video_renderer_from_csv_files(config: Config) -> VideoRenderer:
    """Instantiate a VideoRenderer for Configs where all data is stored as .csv or .csv.gz"""
    missing_files = config.get_missing_files()
    if len(missing_files) > 0:
        raise FileNotFoundError(
            f"Your configuration points to the following files that are not available: {missing_files}"
        )

    video_provider = instantiate_video_provider(config.video_config)
    graph_providers = instantiate_graph_providers(config.sensor_configs)
    return VideoRenderer(config.render_config, video_provider, graph_providers)


def instantiate_graph_providers(
    sensor_configs: Dict[str, SensorConfig]
) -> Dict[str, GraphImageProvider]:
    """
    Instantiate a the appropriate GraphImageProvider subclass for a given config.

    You must instantiate your GraphImageProviders manually if the data isn't stored as CSV or CSV.GZ where the
    first column is a DatetimeIndex
    """
    result = {}

    for name, sc in sensor_configs.items():
        if isinstance(sc, ManuallySynchronizedSensorConfig):
            result[name] = ManuallySyncedGraphProvider(None)
        elif isinstance(sc, ImuSynchronizedSensorConfig):
            result[name] = CameraImuSyncedGraphProvider(
                pd.read_csv(sc.path, index_col=0, parse_dates=True),
                sc.sensor_sync_column,
            )
        elif isinstance(sc, JointSynchronizedSensorConfig):
            result[name] = JointSyncedGraphProvider(
                pd.read_csv(sc.path, index_col=0, parse_dates=True),
                sc.sync_joint_name,
                sc.sensor_sync_axes,
                sc.joint_sync_axis,
            )
        else:
            raise RuntimeError(f"Unknown instance type of SensorConfig: {type(sc)}")

    return result


def instantiate_video_provider(video_config: VideoConfig) -> VideoImageProvider:
    """Instantiate the appropriate VideoImageProvider subclass for a given VideoConfig"""
    if isinstance(video_config, CameraImuVideoConfig):
        raise NotImplementedError("CameraImuVideoConfig Not Implemented")
    elif isinstance(video_config, KinectVideoConfig):
        return AzureProvider(video_config.path, video_config.skeleton_path)
    elif isinstance(video_config, RawVideoConfig):
        raise NotImplementedError("RawVideoConfig Not Implemented")
    elif isinstance(video_config, OpenPoseVideoConfig):
        raise NotImplementedError("OpenPoseVideoConfig Not Implemented")
    else:
        raise RuntimeError(
            f"Unknown instance type of VideoConfig: {type(video_config)}"
        )
