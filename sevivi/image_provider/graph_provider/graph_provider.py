from typing import List, Optional

import pandas as pd
from matplotlib.axis import Axis

from sevivi.config import (
    RenderConfig,
    find_matching_columns,
    SensorConfig,
    ManuallySynchronizedSensorConfig,
    JointSynchronizedSensorConfig,
    ImuSynchronizedSensorConfig,
    get_graph_groups,
)


class GraphImageProvider:
    """
    A GraphImageProvider has some data with a DatetimeIndex to display.
    An offset to that data can be set to synchronize the data with the video.
    Groups of axes that should be rendered together can be set in the config
    """

    axes: List[Axis] = None
    """The axes that this GraphImageProvider can draw to"""

    def __init__(
        self,
        data: pd.DataFrame,
        render_config: RenderConfig,
        sensor_config: SensorConfig,
    ):
        self._data = data
        self.render_config = render_config
        self.sensor_config = sensor_config
        if not isinstance(data.index, pd.DatetimeIndex):
            raise ValueError("All graph data must use a DatetimeIndex!")

        self._graph_groups = get_graph_groups(data, sensor_config.graph_groups)

    def get_sync_dataframe(self) -> Optional[pd.DataFrame]:
        conf = self.sensor_config
        if isinstance(conf, ManuallySynchronizedSensorConfig):
            return None
        elif isinstance(conf, ImuSynchronizedSensorConfig) or isinstance(
            conf, JointSynchronizedSensorConfig
        ):
            matching_columns = find_matching_columns(
                self._data, conf.sensor_sync_column_selection
            )
            return self._data[matching_columns]
        else:
            raise ValueError("Cannot get sync DF for unknown sensor config type")

    def get_graph_count(self) -> int:
        return len(self._graph_groups)

    def render_graph_axes(self, ts: pd.Timestamp):
        raise NotImplementedError("render_graph_axes is not yet implemented")

    def set_offset(self, offset: pd.Timedelta):
        self._data.index += offset
