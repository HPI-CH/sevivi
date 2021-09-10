import logging
from typing import Optional, List, Generator, Tuple

import pandas as pd
import cv2

from .video_provider import VideoImageProvider
from ..dimensions import Dimensions

from sevivi.log import logger

logger = logger.getChild("plain_video_image_provider")


class PlainVideoImageProvider(VideoImageProvider):
    """The plain video image provider provides image from any video supported by openCV with manual synchronization."""

    def __init__(self, video_path: str):
        self.__video = cv2.VideoCapture(video_path)

    def get_sync_dataframe(self, column_names: List[str]) -> None:
        logger.warning(
            "PlainVideoImageProvider can only be synced to manually. Ignoring get_sync_dataframe."
        )
        return None

    def images(self) -> Generator[Tuple[pd.Timestamp, bytes], None, None]:
        while self.__video.isOpened():
            frame_exists, frame = self.__video.read()
            if frame_exists:
                ts = self.__video.get(cv2.CAP_PROP_POS_MSEC)
                yield pd.to_datetime(ts, unit="ms"), frame
            else:
                break

    def get_image_count(self) -> int:
        return int(self.__video.get(cv2.CAP_PROP_FRAME_COUNT))

    def get_dimensions(self) -> Dimensions:
        return Dimensions(
            w=int(self.__video.get(cv2.CAP_PROP_FRAME_WIDTH)),
            h=int(self.__video.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        )
