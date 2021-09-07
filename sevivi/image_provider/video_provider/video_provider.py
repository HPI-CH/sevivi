from abc import ABC
from typing import Optional

import pandas as pd

from sevivi.image_provider import ImageProvider


class VideoImageProvider(ImageProvider, ABC):
    """VideoImageProviders"""

    def __init__(self, data: Optional[pd.DataFrame]):
        super().__init__(data)

    def get_offset(self, graph_sync_df: pd.DataFrame) -> pd.Timedelta:
        """Get the offset required to synchronize the given dataframe to the video"""
        raise NotImplementedError(
            "get_offset must be implemented by VideoImageProvider subclasses!"
        )
