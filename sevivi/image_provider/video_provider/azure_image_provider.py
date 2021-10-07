from typing import List, Optional, Generator, Tuple
from collections import OrderedDict

import pandas as pd
import os
import cv2
import json

from .video_provider import VideoImageProvider
from ..dimensions import Dimensions


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
            pd.read_csv(joint_3d_df, sep=";").set_index("timestamp", drop=True)
        )

        if joint_2d_df is not None:
            self.__joint_df_2d = (
                self._drop_duplicate_body_indices_and_confidence_values(
                    pd.read_csv(joint_2d_df, sep=";").set_index("timestamp", drop=True)
                )
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

                # if self.__skeleton_definition is not None:
                #     skeleton_data = (
                #         self.__joint_df_2d.iloc[image_count, :]
                #         .to_numpy()
                #         .reshape(-1, 2)
                #     )

                yield pd.to_datetime(ts, unit="ms"), frame
                image_count += 1
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
