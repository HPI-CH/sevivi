"""The IMU video image provider provides images from a camera with an integrated IMU together with the IMU data."""
from typing import List, Generator, Tuple

import cv2
import pandas as pd

from sevivi.log import logger
from .video_provider import VideoImageProvider
from ..dimensions import Dimensions

logger = logger.getChild("plain_video_image_provider")


class ImuCameraImageProvider(VideoImageProvider):
    """The IMU video image provider provides images from a camera with an integrated IMU together with the IMU data."""

    def __init__(self, video_path: str, imu_df_path: str):
        self.__video = cv2.VideoCapture(video_path)
        self.data: pd.DataFrame = pd.read_csv(imu_df_path)

    def get_sync_dataframe(self, column_names: List[str]) -> pd.DataFrame:
        """
        Returns the selected portion of the IMU data.
        """
        return self.data[column_names]

    def images(self) -> Generator[Tuple[pd.Timestamp, bytes], None, None]:
        """Generate the images to be shown together with their timestamps"""
        while self.__video.isOpened():
            frame_exists, frame = self.__video.read()
            if frame_exists:
                ts = self.__video.get(cv2.CAP_PROP_POS_MSEC)
                yield pd.to_datetime(ts, unit="ms"), frame
            else:
                break

    def get_image_count(self) -> int:
        """Get the number of images that will be rendered"""
        return int(self.__video.get(cv2.CAP_PROP_FRAME_COUNT))

    def get_dimensions(self) -> Dimensions:
        """Get the dimensions of the source video in pixels."""
        return Dimensions(
            w=int(self.__video.get(cv2.CAP_PROP_FRAME_WIDTH)),
            h=int(self.__video.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        )
