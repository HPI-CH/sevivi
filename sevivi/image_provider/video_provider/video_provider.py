from typing import Optional, List, Generator, Tuple

import numpy as np
import pandas as pd

from ..dimensions import Dimensions


class VideoImageProvider:
    """VideoImageProviders"""

    def images(self) -> Generator[Tuple[pd.Timestamp, np.ndarray], None, None]:
        """Generate the images to be shown together with their timestamps"""
        raise NotImplementedError(
            "images must be implemented by VideoImageProvider subclasses!"
        )

    def get_sync_dataframe(self, column_names: List[str]) -> Optional[pd.DataFrame]:
        raise NotImplementedError(
            "get_sync_dataframe must be implemented by VideoImageProvider subclasses!"
        )

    def get_image_count(self) -> int:
        raise NotImplementedError(
            "get_image_count must be implemented by VideoImageProvider subclasses!"
        )

    def get_dimensions(self) -> Dimensions:
        raise NotImplementedError(
            "get_dimensions must be implemented by VideoImageProvider subclasses!"
        )
