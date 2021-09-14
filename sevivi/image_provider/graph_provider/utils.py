from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.lines import Line2D

from sevivi.log import logger

logger = logger.getChild("graph_provider")


def calculate_index(
    target_ts: pd.Timestamp, timestamps: pd.DatetimeIndex
) -> pd.Timestamp:
    """
    Return the first index value after the target timestamp if the exact timestamp is not available
    """
    # noinspection PyUnresolvedReferences
    target_beyond_available = (target_ts > timestamps).all()

    if target_beyond_available:
        return timestamps[-1]
    elif target_ts in timestamps:
        return target_ts
    else:
        return timestamps[timestamps > target_ts][0]


def epochize_index(input: pd.DataFrame) -> pd.DataFrame:
    """
    Put the first index value of the input dataframe exactly on the unix epoch.
    """
    if not isinstance(input.index, pd.DatetimeIndex):
        raise ValueError("All graph data must use a DatetimeIndex!")

    zeroed_index = input.index.view(np.int64)
    zeroed_index -= zeroed_index[0]
    input.index = pd.to_datetime(zeroed_index, unit="ns")
    return input


@dataclass
class RenderAxis:
    """Encapsulate all information about the axes of a GraphProvider needed for efficient drawing."""

    ax: Axes = None
    """The matplotlib axis to render to"""
    columns: List[str] = None
    """The columns of the dataframe plotted in this axis"""
    name: str = None
    """Human-readable title prefix of this axis"""
    vline: Optional[Line2D] = None
    """Vline artist"""
    bounding_boxes: Dict[str, Any] = field(default_factory=dict)
    """Maps all columns in this axis to a BufferRegion of the graphic inside their bounding box"""
