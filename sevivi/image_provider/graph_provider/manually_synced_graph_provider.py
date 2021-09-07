import pandas as pd

from .graph_provider import GraphImageProvider


class ManuallySyncedGraphProvider(GraphImageProvider):
    """The manually synced graph provider relies on the supplied manual offset to be synchronous to the video."""

    def __init__(self, data: pd.DataFrame, manual_offset: pd.Timedelta):
        super().__init__(data)
        super().set_offset(manual_offset)

    def get_image_for_time_stamp(self, ts: pd.Timestamp):
        pass

    def set_offset(self, offset: pd.Timedelta):
        """
        Calls to ManuallySyncedGraphProvider.set_offset are ignored; a manual offset is used for this GraphProvider.
        """
        pass
