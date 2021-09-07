from typing import Optional

import pandas as pd

from sevivi.image_provider import GraphImageProvider


class ManuallySyncedGraphProvider(GraphImageProvider):
    def __init__(self, data: Optional[pd.DataFrame]):
        super().__init__(data)

    def get_image_for_time_stamp(self, ts: pd.Timestamp):
        pass
