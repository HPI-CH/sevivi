import logging
from typing import Dict

from sevivi.config import (
    RenderConfig,
    JointSynchronizedSensorConfig,
    ImuSynchronizedSensorConfig,
    ManuallySynchronizedSensorConfig,
)
from sevivi.image_provider import GraphImageProvider, VideoImageProvider
from sevivi.synchronizer.synchronizer import get_synchronization_offset

logger = logging.getLogger("sevivi.video_renderer")


class VideoRenderer:
    """
    Renders a number of graphs by the GraphImageProviders next to a video from the
    VideoImageProvider as specified by the given RenderConfig
    """

    def __init__(
        self,
        render_config: RenderConfig,
        video_provider: VideoImageProvider,
        graph_providers: Dict[str, GraphImageProvider],
    ):
        self.render_config = render_config
        self.video_provider = video_provider
        self.graph_providers = graph_providers

        self._prepare_graph_providers()

    def _prepare_graph_providers(self):
        """Prepare the graph providers so that their get_image_for_time_stamp can be used."""
        for name, gp in self.graph_providers.items():
            sensor_conf = gp.sensor_config
            if not isinstance(sensor_conf, ManuallySynchronizedSensorConfig):
                if isinstance(sensor_conf, JointSynchronizedSensorConfig):
                    video_sync_cols = sensor_conf.camera_joint_sync_column_selection
                elif isinstance(sensor_conf, ImuSynchronizedSensorConfig):
                    video_sync_cols = sensor_conf.camera_imu_sync_column_selection
                else:
                    raise RuntimeError(f"Unknown sensor cfg type: {type(sensor_conf)}")
                video_sync_df = self.video_provider.get_sync_dataframe(video_sync_cols)

                offset = get_synchronization_offset(
                    video_sync_df, gp.get_sync_dataframe(), gp.sensor_config
                )
                # support sync dataframes with columns specified in sensors' config
                logger.debug(f"Graph {name} gets offset {offset}")
                gp.set_offset(offset)

    def render_video(self):
        """Renders the video from given VideoImageProvider and GraphImageProviders using the given RenderConfig."""
        logger.error(
            f"NOT IMPLEMENTED: rendering video to {self.render_config.target_file_path}"
        )
