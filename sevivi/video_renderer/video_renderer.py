import logging
from typing import Dict

from sevivi.config import RenderConfig
from sevivi.image_provider.graph_provider import (
    GraphImageProvider,
)
from sevivi.image_provider.video_provider.video_provider import VideoImageProvider

logger = logging.getLogger("sevivi.video_renderer")


class VideoRenderer:
    def __init__(
        self,
        render_config: RenderConfig,
        video_provider: VideoImageProvider,
        graph_providers: Dict[str, GraphImageProvider],
    ):
        self.render_config = render_config
        self.video_provider = video_provider
        self.graph_providers = graph_providers

    def render_video(self):
        logger.error(
            f"NOT IMPLEMENTED: rendering video to {self.render_config.target_file_path}"
        )
