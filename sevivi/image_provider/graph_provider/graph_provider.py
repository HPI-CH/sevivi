from pprint import pformat
from typing import List, Optional

import pandas as pd
from matplotlib.axes import SubplotBase, Axes
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
from .utils import epochize_index, calculate_index, RenderAxis

logger = logger.getChild("graph_provider")


class GraphImageProvider:
    """
    A GraphImageProvider has some data with a DatetimeIndex to display.
    An offset to that data can be set to synchronize the data with the video.
    Groups of axes that should be rendered together can be set in the config
    """

    group_line_colors = [f"C{i}" for i in range(10)]
    """
    Provide the default matplotlib color cycle for 10 dimensions.
    Overwrite with a bigger color cycle if you have more dimensions
    in a single graph, or want different colors.
    """

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

        self.__axs: List[RenderAxis] = []

        self._graph_groups = get_graph_groups(data, sensor_config.graph_groups)
        logger.debug(
            f"Got groups {pformat(self._graph_groups)} "
            f"for columns {list(data.columns)} "
            f"and graph_groups {sensor_config.graph_groups}"
        )

    def set_axs(self, figure: Figure, axes: List[Axes]):
        """Assign the axes that this graph provider may draw to."""
        for axis_idx, (title, cols) in enumerate(self._graph_groups.items()):
            ax = axes[axis_idx]
            ax.set_xlim(self._data.index[0], self._data.index[-1])
            ax.set_ylim(self._data[cols].min().min(), self._data[cols].max().max())

            if self.sensor_config.name != "":
                title = f"{self.sensor_config.name}: {title}"
            ax.set_title(title)

            render_axis = RenderAxis(ax, cols, title)
            for col_idx, col in enumerate(cols):
                color = self.group_line_colors[col_idx]
                line = ax.plot(
                    self._data.index,
                    self._data[col],
                    color=color,
                )[0]

                # draw to cache renderers
                figure.canvas.draw()

                bbox_copy = figure.canvas.copy_from_bbox(line.clipbox)
                render_axis.bounding_boxes[col] = bbox_copy

            render_axis.vline = ax.axvline(0, color="grey")

            self.__axs.append(render_axis)

    def get_sync_dataframe(self) -> Optional[pd.DataFrame]:
        """
        Return a dataframe that can be used to synchronize this GraphDataProvider to a video.
        When an offset between the video data and the data from this graph provider has been
        calculated, the set_offset function can be used to apply the offset.
        """
        is_imu_cam = isinstance(self.sensor_config, ImuSynchronizedSensorConfig)
        is_joint_cam = isinstance(self.sensor_config, JointSynchronizedSensorConfig)
        is_manual_cam = isinstance(self.sensor_config, ManuallySynchronizedSensorConfig)

        if is_manual_cam:
            return None
        elif is_imu_cam or is_joint_cam:
            # noinspection PyUnresolvedReferences
            sync_cols = self.sensor_config.sensor_sync_column_selection
            matching_columns = find_matching_columns(self._data, sync_cols)
            return self._data[matching_columns]
        else:
            raise ValueError("Cannot get sync DF for unknown sensor config type")

    def get_graph_count(self) -> int:
        """
        Get the number of axes this GraphProvider needs to render all its graphs.
        """
        return len(self._graph_groups)

    def render_graph_axes(self, figure: Figure, ts: pd.Timestamp):
        """
        Render to the axes this graph provider has been assigned.
        Figure must be the same figure the axes instances are from.
        Data will be rendered for the given timestamp.
        """
        if self.render_config.plotting_method == PlottingMethod.MOVING_VERTICAL_LINE:
            for render_axis in self.__axs:

                for bbox in render_axis.bounding_boxes.values():
                    figure.canvas.restore_region(bbox)

                # noinspection PyTypeChecker
                vline_position = calculate_index(ts, self._data.index)
                # noinspection PyTypeChecker
                render_axis.vline.set_xdata([vline_position, vline_position])
                render_axis.ax.draw_artist(render_axis.vline)
        else:
            raise NotImplementedError("Only VLINE implemented so far")

    def set_offset(self, offset: pd.Timedelta):
        """
        Apply an offset to the data of this graph provider.
        Positive and negative offsets are supported.
        GraphProvider instances for ManuallySynchronizedSensorConfigs ignore the provided
        argument and instead add the manually configured offset.
        """
        if isinstance(self.sensor_config, ManuallySynchronizedSensorConfig):
            offset = pd.to_timedelta(self.sensor_config.offset_seconds, unit="s")

        self._data.index += offset
