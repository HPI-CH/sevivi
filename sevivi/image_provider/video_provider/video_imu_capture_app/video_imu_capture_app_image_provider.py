"""The IMU video image provider provides images from a camera with an integrated IMU together with the IMU data."""
from typing import List, Generator, Tuple

import cv2
import pandas as pd
from read_protobuf import ProtobufReader

from sevivi.image_provider.video_provider.video_imu_capture_app import recording_pb2
from sevivi.log import logger
from sevivi.image_provider.video_provider.video_provider import VideoImageProvider
from sevivi.image_provider.dimensions import Dimensions
from sevivi.config import find_matching_columns

logger = logger.getChild("plain_video_image_provider")


class VideoImuCaptureAppImageProvider(VideoImageProvider):
    """
    The VideoImuCaptureAppImageProvider directly supports the VideoIMUCapture-Android app available at
    https://github.com/DavidGillsjo/VideoIMUCapture-Android/. You can use this app to create a video file with
    associated IMU data.

    By shaking both the sensors and the smartphone before and after you record data, you can introduce markers for
    the correlation-based synchronization to work. If synchronization doesn't work, you should provide a custom
    synchronizer implementation.
    """

    def __init__(self, video_path: str, imu_pb_path: str):
        self.__video = cv2.VideoCapture(video_path)

        try:
            with open(imu_pb_path, "rb") as f:
                message_data = f.read()
            message = recording_pb2.VideoCaptureData.FromString(message_data)
            data = ProtobufReader().interpret_message(message)
        except Exception as e:
            raise RuntimeError(
                f"Could not read protobuf file {imu_pb_path}. Is it from VideoIMUCapture_v0.12.apk?"
            ) from e

        timestamps = [item["time_ns"] for item in data["imu"]]
        imu_accel_data = [item["accel"] for item in data["imu"]]
        self.data: pd.DataFrame = pd.DataFrame(
            imu_accel_data,
            index=timestamps,
            columns=["ACCELERATION_X", "ACCELERATION_Y", "ACCELERATION_Z"],
        )

        # noinspection PyTypeChecker
        self.data.index = pd.to_datetime(self.data.index, unit="ns")

    def get_sync_dataframe(self, column_names: List[str]) -> pd.DataFrame:
        """
        Returns the selected portion of the IMU data.
        """
        matching_columns = find_matching_columns(self.data, column_names)
        return self.data[matching_columns]

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
