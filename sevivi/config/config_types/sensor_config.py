import os
from dataclasses import dataclass
from typing import Optional, Union, List

import pandas as pd


@dataclass
class SensorConfig:
    """
    SensorConfig instances allow specifying the data taken and synchronized from sensors.
    """

    path: str = None
    """Path to the sensor data csv"""
    start_time: Optional[pd.Timestamp] = None
    """Start time of the sensor data. This is useful to select a portion of data from a longer recording"""
    end_time: Optional[pd.Timestamp] = None
    """End time of the sensor data. This is useful to select a portion of data from a longer recording"""
    graph_groups: Optional[List[str]] = None
    """List of in/pre/postfixes that select a number of columns to be graphed in the same axis."""

    def get_missing_files(self) -> List[str]:
        """Returns a list of all missing files for this config"""
        if not os.path.isfile(self.path):
            return [self.path]
        return []


@dataclass
class ManuallySynchronizedSensorConfig(SensorConfig):
    """
    This SensorConfig provides the information necessary to synchronize a sensor manually
    """

    offset_seconds: float = 0.0
    """Offset the select data chunk, or the entire graph data, by this number of seconds"""


@dataclass
class JointSynchronizedSensorConfig(SensorConfig):
    """
    This SensorConfig provides the information necessary to synchronize by using a number of columns from the sensor data
    to align to axes from a specific joint.

    :Example:
    path: /tmp/my_ankle_imu.csv.gz
    start_time: 00:00:00.000000
    sync_joint_name: ANKLE_RIGHT
    sensor_sync_column_selection: ["AX", "accel Y", "ACCELERATION_Z"]
    camera_joint_sync_column_selection: ACCELERATION_MAG
    """

    camera_joint_sync_column_selection: Union[str, List[str]] = None
    """Source columns from the camera skeleton to synchronize to"""
    sensor_sync_column_selection: Union[str, List[str]] = None
    """Columns from the sensor data to synchronize to"""


@dataclass
class ImuSynchronizedSensorConfig(SensorConfig):
    """This SensorConfig provides the information necessary to synchronize data to a video by camera IMU."""

    sensor_sync_column_selection: Union[str, List[str]] = None
    """
    Name of the column or list of the columns that contain the IMU data to synchronize with the camera IMU.
    This allows to e.g., select the acceleration columns from your sensor. The names of these columns coming from the
    camera IMU are configured using CameraImuVideoConfig.
    """

    camera_imu_sync_column_selection: Union[str, List[str]] = None
    """Source columns from the camera IMU to synchronize to"""
