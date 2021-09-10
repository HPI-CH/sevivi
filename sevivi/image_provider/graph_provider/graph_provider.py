import logging
from collections import defaultdict
from pprint import pformat
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

from sevivi.log import logger

logger = logger.getChild("graph_provider")


def calculate_index(
    target_ts: pd.Timestamp, timestamps: pd.DatetimeIndex
) -> pd.Timestamp:
    """
    Return the first index value after the target timestamp if the exact timestamp is not available
    """
    # noinspection PyUnresolvedReferences
    target_beyond_available = (target_ts > timestamps).all()

    if target_beyond_available:
        return timestamps[-1]
    elif target_ts in timestamps:
        return target_ts
    else:
        return timestamps[timestamps > target_ts][0]


def epochize_index(input: pd.DataFrame) -> pd.DataFrame:
    if not isinstance(input.index, pd.DatetimeIndex):
        raise ValueError("All graph data must use a DatetimeIndex!")

    zeroed_index = input.index.view(np.int64)
    zeroed_index -= zeroed_index[0]
    input.index = pd.to_datetime(zeroed_index, unit="ns")
    return input


class GraphImageProvider:
    """
    A GraphImageProvider has some data with a DatetimeIndex to display.
    An offset to that data can be set to synchronize the data with the video.
    Groups of axes that should be rendered together can be set in the config
    """

    group_line_colors = [f"C{i}" for i in range(10)]

    @property
    def name(self) -> str:
        return self.sensor_config.name

    def __init__(
        self,
        data: pd.DataFrame,
        render_config: RenderConfig,
        sensor_config: SensorConfig,
    ):
        self._data = epochize_index(data)
        self.render_config = render_config
        self.sensor_config = sensor_config

        self.__axs: Dict[int, Tuple[Axis, List[str], str]] = {}
        self.__lines: Dict[int, Dict[str, Any]] = defaultdict(dict)
        self.__bboxes: Dict[int, Dict[str, Any]] = defaultdict(dict)
        self.__vlines: Dict[int, Any] = defaultdict(dict)

        self._graph_groups = get_graph_groups(data, sensor_config.graph_groups)
        logger.debug(
            f"Got groups {pformat(self._graph_groups)} "
            f"for columns {list(data.columns)} "
            f"and graph_groups {sensor_config.graph_groups}"
        )

    def set_axs(self, figure: Figure, axes: List[Axis]):
        for axis_idx, (title, cols) in enumerate(self._graph_groups.items()):
            self.__axs[axis_idx] = (axes[axis_idx], cols, title)

        for axis_idx, (axis, cols, title) in self.__axs.items():
            axis.set_ylim(self.get_ylimits(axis_idx))
            axis.set_title(title)
            if self.sensor_config.name != "":
                axis.set_title(f"{self.sensor_config.name}: {title}")

            axis.set_xlim(self.get_xlimits())

            for col_idx, col in enumerate(cols):
                self.__lines[axis_idx][col] = axis.plot(
                    self._data.index,
                    self._data[col],
                    color=self.group_line_colors[col_idx],
                )[0]
            self.__vlines[axis_idx] = axis.axvline(0, color="grey")

        # draw once to cache renderers
        figure.canvas.draw()

        for axis_idx, (axis, cols, title) in self.__axs.items():
            for col_idx, line in self.__lines[axis_idx].items():
                line_clipbox = figure.canvas.copy_from_bbox(line.clipbox)
                self.__bboxes[axis_idx][col_idx] = line_clipbox

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
        return self._data.index[0], self._data.index[-1]

    def get_graph_count(self) -> int:
        return len(self._graph_groups)

    def render_graph_axes(self, figure: Figure, ts: pd.Timestamp):
        if self.render_config.plotting_method == PlottingMethod.MOVING_VERTICAL_LINE:
            self._render_vline(figure, ts)
        else:
            raise NotImplementedError("Only VLINE implemented so far")

    def _render_vline(self, figure: Figure, ts: pd.Timestamp):
        for axis_idx, (axis, cols, title) in self.__axs.items():

            for col in cols:
                figure.canvas.restore_region(self.__bboxes[axis_idx][col])

            # noinspection PyTypeChecker
            vline_position = calculate_index(ts, self._data.index)
            self.__vlines[axis_idx].set_xdata([vline_position, vline_position])
            axis.draw_artist(self.__vlines[axis_idx])
            # logger.debug(f"{self.sensor_config.name} rendered vline for axis{axis_idx} to {vline_position}")

    def set_offset(self, offset: pd.Timedelta):
        if isinstance(self.sensor_config, ManuallySynchronizedSensorConfig):
            offset = pd.to_timedelta(self.sensor_config.offset_seconds, unit="s")

        self._data.index += offset
