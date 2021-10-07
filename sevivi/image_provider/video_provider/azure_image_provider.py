from typing import List, Optional, Generator, Tuple

import pandas as pd
import os
import cv2

from .video_provider import VideoImageProvider
from ..dimensions import Dimensions


class AzureProvider(VideoImageProvider):
    """The Azure Provider provides images from a video or path with images along"""

    def __init__(
        self,
        video_path: str,
        joint_3d_df: str,
        joint_2d_df: str = None,
        sync_joint_name: str = None,
    ):
        if not os.path.exists(video_path):
            raise Exception(f"File {video_path} not found!")

        self.__video = cv2.VideoCapture(video_path)
        self.__sync_joint_name = sync_joint_name
        self.__joint_df_3d = self._drop_duplicate_body_indices_and_confidence_values(
            pd.read_csv(joint_3d_df, sep=";").set_index("timestamp", drop=True)
        )

        if joint_2d_df is not None:
            self.__joint_df_2d = (
                self._drop_duplicate_body_indices_and_confidence_values(
                    pd.read_csv(joint_2d_df, sep=";").set_index("timestamp", drop=True)
                )
            )
        else:
            self.__joint_df_2d = None

    @staticmethod
    def _drop_duplicate_body_indices_and_confidence_values(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        df = df[[c for c in df.columns if "(c)" not in c]]
        body_idx_c = df["body_idx"].value_counts()
        df = df[df["body_idx"] == body_idx_c.index[body_idx_c.argmax()]]
        df = df.drop("body_idx", axis=1)
        return df

    def images(self) -> Generator[Tuple[pd.Timestamp, bytes], None, None]:
        while self.__video.isOpened():
            frame_exists, frame = self.__video.read()
            if frame_exists:
                ts = self.__video.get(cv2.CAP_PROP_POS_MSEC)
                yield pd.to_datetime(ts, unit="ms"), frame
            else:
                break

    def get_sync_dataframe(self, column_names: List[str]) -> Optional[pd.DataFrame]:
        if type(column_names) is str:
            if column_names not in self.__joint_df_3d.columns:
                raise Exception(
                    f"Sync joint name {column_names} not in Kinect dataframe."
                )
            else:
                return self.__joint_df_3d[column_names]

        if type(column_names) is list:
            valid = all(elem in self.__joint_df_3d.columns for elem in column_names)
            if not valid:
                raise Exception(f"Missing sync joints in Dataframe: {column_names}")
            return self.__joint_df_3d[
                [col for col in column_names if col in self.__joint_df_3d.columns]
            ]

        raise Exception(f"Wrong type given: {type(column_names)}, expected: List[str]")

    def get_image_count(self) -> int:
        return int(self.__video.get(cv2.CAP_PROP_FRAME_COUNT))

    def get_dimensions(self) -> Dimensions:
        return Dimensions(
            w=int(self.__video.get(cv2.CAP_PROP_FRAME_WIDTH)),
            h=int(self.__video.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        )
