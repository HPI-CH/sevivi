import pandas as pd

from sevivi.image_provider import ImageProvider


class GraphImageProvider(ImageProvider):
    def __init__(self, data: pd.DataFrame):
        super().__init__(data)
        if data is not None and not isinstance(data.index, pd.DatetimeIndex):
            raise ValueError("All graph data must use a DatetimeIndex!")

    def get_image_for_time_stamp(self, ts: pd.Timestamp):
        raise NotImplementedError(
            "GraphImageProvider subclasses need to provide images for TS!"
        )

    def set_offset(self, offset: pd.Timedelta):
        if self.__data is not None:
            self.__data.index += offset

    def get_sync_data_frame(self):
        return self.__data
