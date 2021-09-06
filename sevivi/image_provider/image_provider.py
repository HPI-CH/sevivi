import pandas as pd


class ImageProvider:
    def __init__(self, data: pd.DataFrame):
        self.__data = data

    def get_image_for_time_stamp(self):
        pass

    def get_sync_data_frame(self):
        return self.__data
