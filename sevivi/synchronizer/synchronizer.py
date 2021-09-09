import pandas as pd

from sevivi.config.config_types.sensor_config import SensorConfig


def get_synchronization_offset(
    video_sync_df: pd.DataFrame,
    sensor_sync_df: pd.DataFrame,
    sensor_config: SensorConfig,
) -> pd.Timedelta:
    return pd.Timedelta(seconds=0)
