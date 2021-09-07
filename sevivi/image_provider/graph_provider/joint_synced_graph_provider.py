from typing import Union, List

import pandas as pd

from sevivi.config.config_types.sensor_config import SyncJointAxis
from sevivi.image_provider import GraphImageProvider


class JointSyncedGraphProvider(GraphImageProvider):
    def __init__(
        self,
        data: pd.DataFrame,
        sync_joint_name: str,
        sensor_sync_axes: Union[str, List[str]],
        joint_sync_axis: SyncJointAxis,
    ):
        super().__init__(data)
        self.sync_joint_name = sync_joint_name
        self.sensor_sync_axes = sensor_sync_axes
        self.joint_sync_axis = joint_sync_axis

    def get_image_for_time_stamp(self, ts: pd.Timestamp):
        pass
