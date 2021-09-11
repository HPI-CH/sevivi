"""VideoImageProviders provide the video aroud which the data graphs are rendered"""

from typing import Optional, List, Generator, Tuple

import numpy as np
import pandas as pd

from ..dimensions import Dimensions


class VideoImageProvider:
    """VideoImageProviders provide the video aroud which the data graphs are rendered"""

    def images(self) -> Generator[Tuple[pd.Timestamp, np.ndarray], None, None]:
        """Generate the images to be shown together with their timestamps"""
        raise NotImplementedError(
            "images must be implemented by VideoImageProvider subclasses!"
        )

    def get_sync_dataframe(self, column_names: List[str]) -> Optional[pd.DataFrame]:
        """
        Get a dataframe that can be used to synchronize graph data against this video.
        The given column names can be provided by GraphImageProviders to select specific
        synchronization targets, e.g., the acceleration of a specific joint.
        """
        raise NotImplementedError(
            "get_sync_dataframe must be implemented by VideoImageProvider subclasses!"
        )

    def get_image_count(self) -> int:
        """Get the number of images that will be rendered"""
        raise NotImplementedError(
            "get_image_count must be implemented by VideoImageProvider subclasses!"
        )

    def get_dimensions(self) -> Dimensions:
        """Get the dimensions of the source video in pixels."""
        raise NotImplementedError(
            "get_dimensions must be implemented by VideoImageProvider subclasses!"
        )
