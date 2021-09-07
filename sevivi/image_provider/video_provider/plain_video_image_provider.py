import logging
from typing import Optional

import pandas as pd
import os
import cv2

from .video_provider import VideoImageProvider

logger = logging.getLogger("sevivi.plain_video_image_provider")


class PlainVideoImageProvider(VideoImageProvider):
    """The plain video image provider provides image from any video supported by openCV with manual synchronization."""

    def __init__(self, video_path: str, data: Optional[pd.DataFrame]):
        super().__init__(data)
        self.__video_capture = cv2.VideoCapture(video_path)

    def get_offset(self, graph_sync_df: pd.DataFrame) -> pd.Timedelta:
        if graph_sync_df is not None:
            logger.warning(
                "PlainVideoImageProvider can only be synced to manually. Ignoring input DataFrame."
            )
        return pd.Timedelta()

    def get_image_for_time_stamp(self, ts: pd.Timestamp):
        pass
