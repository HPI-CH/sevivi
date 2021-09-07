import pandas as pd

from sevivi.image_provider import ImageProvider
from sevivi.image_provider.graph_provider.graph_provider import GraphImageProvider


class VideoImageProvider(ImageProvider):
    def __init__(self, data: pd.DataFrame):
        super().__init__(data)

    def get_offset(self, graph_image_provider: GraphImageProvider):
        raise NotImplementedError(
            "get_offset must be implemented by VideoImageProvider subclasses!"
        )
