from typing import Optional, List, Generator, Tuple

import pandas as pd


class VideoImageProvider:
    """VideoImageProviders"""

    def images(self) -> Generator[Tuple[pd.Timestamp, bytes], None, None]:
        """Generate the images to be shown together with their timestamps"""
        raise NotImplementedError(
            "images must be implemented by VideoImageProvider subclasses!"
        )

    def get_sync_dataframe(self, column_names: List[str]) -> Optional[pd.DataFrame]:
        raise NotImplementedError(
            "get_sync_dataframe must be implemented by VideoImageProvider subclasses!"
        )
