import logging
from typing import Dict

from sevivi.config import RenderConfig
from sevivi.image_provider.graph_provider.graph_provider import GraphImageProvider
from sevivi.image_provider.video_provider.video_provider import VideoImageProvider

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
            sync_df = gp.get_sync_data_frame()
            offset = self.video_provider.get_offset(sync_df)
            logger.debug(f"Graph {name} gets offset {offset}")
            gp.set_offset(offset)

    def render_video(self):
        """Renders the video from given VideoImageProvider and GraphImageProviders using the given RenderConfig."""
        logger.error(
            f"NOT IMPLEMENTED: rendering video to {self.render_config.target_file_path}"
        )
