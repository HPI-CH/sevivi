from typing import List, Generator, Tuple

import pandas as pd

from .video_provider import VideoImageProvider


class ImuCameraImageProvider(VideoImageProvider):
    """VideoImageProviders"""

    def __init__(self, video_path, imu_df_path: str):
        self.data: pd.DataFrame = imu_df_path
        self.video = video_path

    def images(self) -> Generator[Tuple[pd.Timestamp, bytes], None, None]:
        """Generate the images to be shown together with their timestamps"""
        raise NotImplementedError(
            "images must be implemented by VideoImageProvider subclasses!"
        )

    def get_sync_dataframe(self, sync_columns: List[str]) -> pd.DataFrame:
        return self.data[sync_columns]
