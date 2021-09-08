import os
from dataclasses import dataclass
from typing import Union, List


@dataclass
class VideoConfig:
    """
    Base class for video configs.
    """

    path: str = None
    """Path to the video file. May be absolute or relative"""

    def get_missing_files(self) -> List[str]:
        """Returns a list of all missing files for this config"""
        if not os.path.isfile(self.path):
            return [self.path]
        return []


@dataclass
class RawVideoConfig(VideoConfig):
    """Can be used to fully configure raw video files."""


@dataclass
class KinectVideoConfig(VideoConfig):
    """Specify Kinect input video"""

    skeleton_path: str = None
    """Path to the skeleton extract from the kinect video"""

    def get_missing_files(self) -> List[str]:
        """Returns a list of all missing files for this config"""
        missing_files = super().get_missing_files()
        if not os.path.isfile(self.skeleton_path):
            missing_files.append(self.skeleton_path)
        return missing_files


@dataclass
class CameraImuVideoConfig(VideoConfig):
    """Specify camera IMU input video"""

    imu_path: str = None
    """Path to the IMU data corresponding to the camera"""

    def get_missing_files(self) -> List[str]:
        """Returns true if all files for this config exist"""
        missing_files = super().get_missing_files()
        if not os.path.isfile(self.imu_path):
            missing_files.append(self.imu_path)
        return missing_files


@dataclass
class OpenPoseVideoConfig(VideoConfig):
    """Specify OpenPose input video"""
