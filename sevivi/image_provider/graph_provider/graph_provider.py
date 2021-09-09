from collections import defaultdict
from typing import List, Optional, Tuple, Dict, Any

import numpy as np
import pandas as pd
from matplotlib.axis import Axis
from matplotlib.figure import Figure

from sevivi.config import (
    RenderConfig,
    find_matching_columns,
    SensorConfig,
    ManuallySynchronizedSensorConfig,
    JointSynchronizedSensorConfig,
    ImuSynchronizedSensorConfig,
    get_graph_groups,
    PlottingMethod,
)


def calculate_index(
    target_ts: pd.Timestamp, timestamps: pd.DatetimeIndex
) -> pd.Timestamp:
    """
    Return the first index value after the target timestamp if the exact timestamp is not available
    """
    if target_ts > timestamps:
        return timestamps[-1]
    elif target_ts in timestamps:
        return target_ts
    else:
        return timestamps[timestamps > target_ts][0]


class GraphImageProvider:
    """
    A GraphImageProvider has some data with a DatetimeIndex to display.
    An offset to that data can be set to synchronize the data with the video.
    Groups of axes that should be rendered together can be set in the config
    """

    __axs: Dict[int, Tuple[Axis, List[str], str]] = {}
    __lines: Dict[int, Dict[str, Any]] = defaultdict(dict)
    __bboxes: Dict[int, Dict[str, Any]] = defaultdict(dict)
    __vlines: Dict[int, Any] = defaultdict(dict)
    group_line_colors = [f"C{i}" for i in range(10)]

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

    def set_axs(self, figure: Figure, axes: List[Axis]):
        for axis_idx, (name, cols) in enumerate(self._graph_groups.items()):
            self.__axs[axis_idx] = (axes[axis_idx], cols, name)

        for axis_idx, (axis, cols, title) in self.__axs:
            axis.set_ylim(self.get_ylimits(axis_idx))
            axis.set_title(title)
            axis.set_xlim(self.get_xlimits())
            axis.set_xticks(self.get_xtick_locations(axis_idx))

            for col_idx, col in enumerate(cols):
                self.__lines[axis_idx][col] = axis.plot(
                    self._data.index,
                    self._data[col],
                    color=self.group_line_colors[col_idx],
                )[0]
            self.__vlines[axis_idx] = axis.axvline(0, color="grey")

        # draw once to cache renderers
        figure.canvas.draw()

        for axis_idx, (axis, cols, title) in self.__axs:
            for col_idx, line in self.__lines[axis_idx].items():
                self.__bboxes[axis_idx][col_idx] = figure.canvas.copy_from_bbox(
                    line.clipbox
                )

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

    def get_ylimits(self, axis: int) -> Tuple[float, float]:
        axis_cols = self.__axs[axis][1]
        cols = self._data[axis_cols]
        min_ = cols.min().min()
        max_ = cols.max().max()
        return min_, max_

    def get_title(self, axis: int) -> str:
        return self.__axs[axis][2]

    def get_xlimits(self):
        pass

    def get_xtick_locations(self, axis: int):
        pass

    def get_graph_count(self) -> int:
        return len(self._graph_groups)

    def render_graph_axes(self, figure: Figure, ts: pd.Timestamp):
        if self.render_config.plotting_method == PlottingMethod.MOVING_VERTICAL_LINE:
            self._render_vline(figure, ts)
        else:
            raise NotImplementedError("Only VLINE implemented so far")

    def _render_vline(self, figure: Figure, ts: pd.Timestamp):
        for axis_idx, (axis, cols, title) in self.__axs:

            for col in cols:
                figure.canvas.restore_region(self.__bboxes[axis_idx][col])

            # noinspection PyTypeChecker
            vline_position = calculate_index(ts, self._data.index)
            self.__vlines[axis_idx].set_xdata([vline_position, vline_position])
            axis.draw_artist(self.__vlines[axis_idx])

    def set_offset(self, offset: pd.Timedelta):
        self._data.index += offset
