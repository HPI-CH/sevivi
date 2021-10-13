from typing import List, Optional, Generator, Tuple
from collections import OrderedDict

import pandas as pd
import numpy as np
import matplotlib.colors
import os
import cv2
import json

from .video_provider import VideoImageProvider
from ..dimensions import Dimensions


def get_hsv_color(cur_value: float, max_value: float) -> np.ndarray:
    return matplotlib.colors.hsv_to_rgb([cur_value / max_value, 1, 1]) * 255


class AzureProvider(VideoImageProvider):
    """The Azure Provider provides images from a video or path with images along"""

    def __init__(
        self,
        video_path: str,
        joint_3d_df: str,
        joint_2d_df: str = None,
    ):
        if not os.path.exists(video_path):
            raise Exception(f"File {video_path} not found!")

        self.__video = cv2.VideoCapture(video_path)
        self.__joint_df_3d = self._drop_duplicate_body_indices_and_confidence_values(
            pd.read_csv(joint_3d_df, sep=";", index_col=0)
        )
        self.__joint_df_3d.index = pd.to_datetime(
            self.__joint_df_3d.index / 1e6, unit="s"
        )

        if joint_2d_df is not None:
            self.__joint_df_2d = (
                self._drop_duplicate_body_indices_and_confidence_values(
                    pd.read_csv(joint_2d_df, sep=";", index_col=0)
                )
            )
            self.__joint_df_2d.index = pd.to_datetime(
                self.__joint_df_2d.index / 1e6, unit="s"
            )
            self.__skeleton_definition = self._read_skeleton_definition_as_tuple(
                self.__joint_df_2d
            )
        else:
            self.__joint_df_2d = None
            self.__skeleton_definition = None

    @staticmethod
    def _drop_duplicate_body_indices_and_confidence_values(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        df = df[[c for c in df.columns if "(c)" not in c]]
        body_idx_c = df["body_idx"].value_counts()
        df = df[df["body_idx"] == body_idx_c.index[body_idx_c.argmax()]]
        df = df.drop("body_idx", axis=1)
        return df

    @staticmethod
    def _read_skeleton_definition_as_tuple(df: pd.DataFrame) -> List[Tuple[int, int]]:
        json_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "azure.json"
        )
        joints = AzureProvider.get_joints_as_list(df)
        with open(json_file) as f:
            connections = json.load(f)

        skeleton = []
        for j1, j2 in connections:
            if j1 not in joints or j2 not in joints:
                continue
            skeleton.append((joints.index(j1), joints.index(j2)))

        return skeleton

    @staticmethod
    def get_joints_as_list(df: pd.DataFrame) -> List[str]:
        columns = [
            column.replace(column[column.find(" (") : column.find(")") + 1], "")
            for column in df.columns
        ]
        return list(OrderedDict.fromkeys(columns))

    def images(self) -> Generator[Tuple[pd.Timestamp, bytes], None, None]:
        image_count = 0
        while self.__video.isOpened():
            frame_exists, frame = self.__video.read()
            if frame_exists:
                ts = self.__video.get(cv2.CAP_PROP_POS_MSEC)

                if self.__skeleton_definition is not None and image_count < len(
                    self.__joint_df_2d
                ):
                    skeleton_data = (
                        self.__joint_df_2d.iloc[image_count, :]
                        .to_numpy()
                        .reshape(-1, 2)
                    )
                    for joint_count, (j1, j2) in enumerate(self.__skeleton_definition):
                        p1 = tuple(int(x) for x in skeleton_data[j1])
                        p2 = tuple(int(x) for x in skeleton_data[j2])
                        color = get_hsv_color(joint_count, self.__joint_df_2d.shape[1])
                        frame = cv2.line(frame, p1, p2, color=color, thickness=9)

                yield pd.to_datetime(ts, unit="ms"), frame
                image_count += 1
            else:
                break

    def get_sync_dataframe(self, column_names: List[str]) -> Optional[pd.DataFrame]:
        if type(column_names) is str:
            if column_names not in self.__joint_df_3d.columns:
                raise KeyError(
                    f"Sync joint name {column_names} not in Kinect dataframe."
                )
            else:
                return self.__joint_df_3d[column_names]

        if type(column_names) is list:
            if not all(elem in self.__joint_df_3d.columns for elem in column_names):
                raise KeyError(f"Missing sync joints in Dataframe: {column_names}.")
            return self.__joint_df_3d[
                [col for col in column_names if col in self.__joint_df_3d.columns]
            ]

        raise TypeError(f"Wrong type given: {type(column_names)}, expected: List[str]")

    def get_image_count(self) -> int:
        return int(self.__video.get(cv2.CAP_PROP_FRAME_COUNT))

    def get_dimensions(self) -> Dimensions:
        return Dimensions(
            w=int(self.__video.get(cv2.CAP_PROP_FRAME_WIDTH)),
            h=int(self.__video.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        )
