from sevivi.config.config_types.sensor_config import SensorConfig

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from .signal_processing import (
    resample_data,
    normalize_signal,
    calculate_magnitude,
    calculate_offset_in_seconds_using_cross_correlation,
    calculate_sampling_frequency_from_timestamps,
)


def get_synchronization_offset(
    video_sync_df: pd.DataFrame,
    sensor_sync_df: pd.DataFrame,
    use_gradient: bool,
    show_plots: bool = False,
) -> pd.Timedelta:
    """
    Get the temporal offset between the two given sensor dataframes.

    :param video_sync_df: the synchronization information from the video
    :param sensor_sync_df: the synchronization information from the sensor
    :param use_gradient: if true, the second derivation of the video synchronization data will be used. if false,
                         the raw data will be used.
    :param show_plots:  can enable debugging plots
    :return:
    """
    video_sf = calculate_sampling_frequency_from_timestamps(video_sync_df.index)
    sensor_sf = calculate_sampling_frequency_from_timestamps(sensor_sync_df.index)

    if use_gradient:
        video_acceleration = np.gradient(
            np.gradient(video_sync_df.to_numpy(), axis=0), axis=0
        )
    else:
        video_acceleration = video_sync_df.to_numpy()

    video_acceleration = resample_data(
        video_acceleration,
        current_sampling_rate=video_sf,
        new_sampling_rate=sensor_sf,
    )
    video_acceleration = normalize_signal(video_acceleration)
    video_acceleration = calculate_magnitude(video_acceleration)

    sensor_acceleration = normalize_signal(sensor_sync_df.to_numpy())
    sensor_acceleration = calculate_magnitude(sensor_acceleration)

    if show_plots:
        plt.close()
        plt.figure(1)
        plt.plot(video_acceleration, label="Kinect")
        plt.plot(sensor_acceleration, label="IMU")
        plt.xlabel("Time (s)")
        plt.ylabel("Acceleration Magnitude (normalized)")
        plt.legend()
        plt.show()

    shift = calculate_offset_in_seconds_using_cross_correlation(
        ref_signal=video_acceleration,
        target_signal=sensor_acceleration,
        sampling_frequency=sensor_sf,
    )

    if show_plots:
        plt.close()
        plt.figure(1)
        plt.plot(video_acceleration, label="Kinect")
        plt.plot(
            np.arange(len(sensor_acceleration)) + (sensor_sf * shift),
            sensor_acceleration,
            label="IMU",
        )
        plt.xlabel("Time (s)")
        plt.ylabel("Acceleration (normalized)")
        plt.legend()
        plt.show()

    return pd.Timedelta(seconds=shift)
