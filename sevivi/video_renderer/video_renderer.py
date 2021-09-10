import logging
from collections import defaultdict
from math import ceil
from typing import Dict, Tuple, Optional, List

import cv2
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.axis import Axis
from matplotlib.figure import Figure

from sevivi.config import (
    RenderConfig,
    JointSynchronizedSensorConfig,
    ImuSynchronizedSensorConfig,
    ManuallySynchronizedSensorConfig,
    StackingDirection,
    PlottingMethod,
    SensorConfig,
)
from sevivi.image_provider import GraphImageProvider, VideoImageProvider, Dimensions
from sevivi.synchronizer.synchronizer import get_synchronization_offset
from .progress_bar import progress_bar

from sevivi.log import logger

logger = logger.getChild("video_renderer")

DPI = 100


class VideoRenderer:
    """
    Renders a number of graphs by the GraphImageProviders next to a video from the
    VideoImageProvider as specified by the given RenderConfig
    """

    def __init__(
        self,
        render_config: RenderConfig,
        video_provider: VideoImageProvider,
        graph_providers: List[GraphImageProvider],
    ):
        self.render_config = render_config
        self.video_provider = video_provider
        self.graph_providers = graph_providers

        self._graph_count = sum([gp.get_graph_count() for gp in self.graph_providers])
        self.__src_vid_dims = self.video_provider.get_dimensions()
        self._plot_dims, self.__tgt_vid_dims = self._prepare_dimensions()
        self._fig, self._axs = self._prepare_figure()
        self._prepare_graph_providers()

    def _prepare_dimensions(self) -> Tuple[Dimensions, Dimensions]:
        src_vid_dim = self.__src_vid_dims
        if self.render_config.stacking_direction == StackingDirection.VERTICAL:
            plot_w, plot_h = src_vid_dim.w, 200 * self._graph_count
            video_w, video_h = src_vid_dim.w, src_vid_dim.h + plot_h
        else:
            plot_w, plot_h = src_vid_dim.w, src_vid_dim.h
            video_w, video_h = src_vid_dim.w // 2 + plot_w, src_vid_dim.h
        return Dimensions(plot_w, plot_h), Dimensions(video_w, video_h)

    def _prepare_figure(self) -> Tuple[Figure, np.ndarray]:
        graph_rows = ceil(self._graph_count / self.render_config.plot_column_count)
        graph_cols = self.render_config.plot_column_count

        figsize = self._plot_dims.w / DPI, self._plot_dims.h / DPI
        fig, axs = plt.subplots(
            graph_rows,
            graph_cols,
            figsize=figsize,
            squeeze=False,
            dpi=DPI,
        )
        plt.tight_layout()

        return fig, axs.ravel()

    def _prepare_graph_providers(self):
        """Set offsets to graph providers"""
        assigned_axis_count = 0
        for gp in self.graph_providers:
            gp.set_offset(self._calc_offset(gp))

            axis_idx_limit = assigned_axis_count + gp.get_graph_count()
            gp.set_axs(self._fig, self._axs[assigned_axis_count:axis_idx_limit])
            logger.debug(
                f"Assigned axis {assigned_axis_count}:{axis_idx_limit} to GP {gp.sensor_config.name}"
            )
            assigned_axis_count += gp.get_graph_count()

    def _calc_offset(
        self, graph_provider: GraphImageProvider
    ) -> Optional[pd.Timedelta]:
        config = graph_provider.sensor_config

        if isinstance(config, ManuallySynchronizedSensorConfig):
            return None
        elif isinstance(config, JointSynchronizedSensorConfig):
            video_sync_cols = config.camera_joint_sync_column_selection
        elif isinstance(config, ImuSynchronizedSensorConfig):
            video_sync_cols = config.camera_imu_sync_column_selection
        else:
            raise RuntimeError(f"Unknown sensor cfg type: {type(config)}")

        video_sync_df = self.video_provider.get_sync_dataframe(video_sync_cols)
        graph_sync_df = graph_provider.get_sync_dataframe()
        offset = get_synchronization_offset(video_sync_df, graph_sync_df, config)

        logger.debug(f"Graph {graph_provider.sensor_config.name} gets offset {offset}")

    def stitch_plot_image(self, ts: pd.Timestamp) -> np.ndarray:
        # self.graph_providers["1"].render_graph_axes(self._fig, ts)
        for gp in self.graph_providers:
            gp.render_graph_axes(self._fig, ts)

        canvas_buffer = self._fig.canvas.buffer_rgba()
        return cv2.cvtColor(np.asarray(canvas_buffer), cv2.COLOR_RGBA2BGR)

    def render_video(self):
        """Renders the video from given VideoImageProvider and GraphImageProviders using the given RenderConfig."""
        src_vid_dim = self.__src_vid_dims
        image = np.empty(
            (self.__tgt_vid_dims.h, self.__tgt_vid_dims.w, 3), dtype=np.uint8
        )

        writer = cv2.VideoWriter(
            self.render_config.target_file_path,
            cv2.VideoWriter_fourcc(*self.render_config.fourcc_codec),
            32,
            tuple(self.__tgt_vid_dims),
        )

        video_provider = self.video_provider
        images, image_count = video_provider.images(), video_provider.get_image_count()
        for index, (ts, src_image) in progress_bar(images, image_count):
            plot_image = self.stitch_plot_image(ts)

            if self.render_config.stacking_direction == StackingDirection.VERTICAL:
                # add the original video image
                image[: src_vid_dim.h, :, :] = src_image
                below_src_vid = slice(src_vid_dim.h, src_vid_dim.h + self._plot_dims.h)
                image[below_src_vid, :, :] = plot_image
            else:
                # add the center half of the original video image
                plot_center = self._plot_dims.w // 2
                tgt_vid_left = slice(0, plot_center)
                tgt_vid_center = slice(plot_center, plot_center + src_vid_dim.w // 2)
                tgt_vid_right = slice(src_vid_dim.w // 2 + plot_center, None, None)

                source_video_half = slice(src_vid_dim.w // 4, 3 * src_vid_dim.w // 4)

                image[:, tgt_vid_left, :] = plot_image[:, tgt_vid_left, :]
                image[:, tgt_vid_center, :] = src_image[:, source_video_half, :]
                image[:, tgt_vid_right, :] = plot_image[:, plot_center:, :]

            writer.write(image)
        writer.release()
