from typing import List, Optional, Generator, Tuple

import pandas as pd
import os
import cv2

from .video_provider import VideoImageProvider


class AzureProvider(VideoImageProvider):
    def __init__(self, video_path: str, data: str):
        if not os.path.exists(video_path):
            raise Exception(f"File {video_path} not found!")

        self.__video_capture = cv2.VideoCapture(video_path)

        df = pd.read_csv(data, sep=";")
        subjects = pd.unique(df["body_idx"])
        print(subjects)
        print(df)

        length = int(self.__video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        print(length)

    def images(self) -> Generator[Tuple[pd.Timestamp, bytes], None, None]:
        pass

    def get_sync_dataframe(self, column_names: List[str]) -> Optional[pd.DataFrame]:
        pass
