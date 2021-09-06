import pandas as pd

from sevivi.image_provider import ImageProvider


class VideoImageProvider(ImageProvider):
    def __init__(self, data: pd.DataFrame):
        super().__init__(data)
