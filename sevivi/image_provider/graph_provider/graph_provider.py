import pandas as pd

from sevivi.image_provider import ImageProvider


class GraphImageProvider(ImageProvider):
    def __init__(self, data: pd.DataFrame):
        super().__init__(data)
        if data is not None and not isinstance(data.index, pd.DatetimeIndex):
            raise ValueError("All graph data must use a DatetimeIndex!")

    def set_offset(self, offset: pd.Timedelta):
        if super().get_sync_data_frame() is not None:
            super().get_sync_data_frame().index += offset
