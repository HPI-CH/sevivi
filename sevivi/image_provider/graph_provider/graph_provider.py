from abc import ABC

import pandas as pd

from sevivi.image_provider import ImageProvider


class GraphImageProvider(ImageProvider, ABC):
    def __init__(self, data: pd.DataFrame):
        super().__init__(data)
        if not isinstance(data.index, pd.DatetimeIndex):
            raise ValueError("All graph data must use a DatetimeIndex!")

    def set_offset(self, offset: pd.Timedelta):
        super().get_sync_data_frame().index += offset
