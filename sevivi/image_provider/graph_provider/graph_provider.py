from abc import ABC

import pandas as pd

from sevivi.image_provider import ImageProvider


class GraphImageProvider(ImageProvider, ABC):
    """
    A GraphImageProvider always has some data with a DatetimeIndex to display. An offset to that data can be
    set to synchronize the data with the video.
    """

    def __init__(self, data: pd.DataFrame):
        super().__init__(data)
        if not isinstance(data.index, pd.DatetimeIndex):
            raise ValueError("All graph data must use a DatetimeIndex!")

    def set_offset(self, offset: pd.Timedelta):
        super().get_sync_data_frame().index += offset
