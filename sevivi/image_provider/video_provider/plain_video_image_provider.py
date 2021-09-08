import logging
from typing import Optional, List, Generator, Tuple

import pandas as pd
import os
import cv2

from .video_provider import VideoImageProvider

logger = logging.getLogger("sevivi.plain_video_image_provider")


class PlainVideoImageProvider(VideoImageProvider):
    """The plain video image provider provides image from any video supported by openCV with manual synchronization."""

    def __init__(self, video_path: str):
        self.__video_capture = cv2.VideoCapture(video_path)

    def get_sync_dataframe(self, column_names: List[str]) -> Optional[pd.DataFrame]:
        logger.warning(
            "PlainVideoImageProvider can only be synced to manually. Ignoring get_sync_dataframe."
        )
        return None

    def get_image_for_time_stamp(self, ts: pd.Timestamp):
        pass

    def images(self) -> Generator[Tuple[pd.Timestamp, bytes], None, None]:
        pass
