from dataclasses import dataclass
from typing import Union, List


@dataclass
class VideoConfig:
    """
    Base class for video configs.
    """

    path: str = None
    """Path to the video file. May be absolute or relative"""


@dataclass
class RawVideoConfig(VideoConfig):
    """Can be used to fully configure raw video files."""


@dataclass
class KinectVideoConfig(VideoConfig):
    """Specify Kinect input video"""

    skeleton_path: str = None
    """Path to the skeleton extract from the kinect video"""


@dataclass
class CameraImuVideoConfig(VideoConfig):
    """Specify camera IMU input video"""

    imu_path: str = None
    """Path to the IMU data corresponding to the camera"""

    camera_imu_sync_column: Union[str, List[str]] = None
    """
    Name of the columns or list of the columns that contain the IMU data to synchronize with.
    If a list given, the magnitude of the listed columns will be used.
    All of the sensors will be synchronized to these columns.
    """


@dataclass
class OpenPoseVideoConfig(VideoConfig):
    """Specify OpenPose input video"""
