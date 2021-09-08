import pandas as pd


class ImageProvider:
    def get_image_for_time_stamp(self, ts: pd.Timestamp):
        raise NotImplementedError(
            "ImageProvider subclasses need to provide images for TS!"
        )
