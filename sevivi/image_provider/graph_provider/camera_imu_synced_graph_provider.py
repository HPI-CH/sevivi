from typing import List, Union

import pandas as pd

from .graph_provider import GraphImageProvider


class CameraImuSyncedGraphProvider(GraphImageProvider):
    def __init__(self, data: pd.DataFrame, sync_columns: Union[str, List[str]]):
        super().__init__(data)
        self.__sync_columns = sync_columns

    def get_image_for_time_stamp(self, ts: pd.Timestamp):
        pass
