from scipy import signal
from scipy import interpolate

import numpy as np
import pandas as pd


def normalize_signal(data: np.ndarray) -> np.ndarray:
    """Normalize a signal to have zero mean and unit variance"""
    return (data - data.mean()) / data.std()


def resample_data(
        data: np.ndarray,
        current_sampling_rate: int,
        new_sampling_rate: int,
        mode="cubic"
) -> np.ndarray:
    """Resamples a signal to the desired new sampling frequency"""
    frames, features = data.shape
    x = np.arange(len(data)) / current_sampling_rate
    num = int(x[-1] * new_sampling_rate)  # Define new constant sampling points
    xx = np.linspace(x[0], x[-1], num)

    result = []
    for feature in range(features):
        y = data[:, feature]
        f = interpolate.interp1d(x, y, kind=mode)
        result.append(f(xx))

    return np.array(result).T


def calculate_magnitude(data: np.ndarray) -> np.ndarray:
    """Calculates the magnitude for given (x,y,z) axes stored in numpy array"""
    assert data.shape[1] == 3, f"Numpy array should have 3 axes, got {data.shape[1]}"
    return np.sqrt(np.square(data).sum(axis=1))


def calculate_offset_in_seconds_using_cross_correlation(
        ref_signal: np.ndarray,
        target_signal: np.ndarray,
        sampling_frequency: int
) -> float:
    """Calculates the temporal offset between the two given numpa arrays"""
    corr = signal.correlate(ref_signal, target_signal)
    shift_in_samples = np.argmax(corr) - len(target_signal) - 1
    return shift_in_samples / sampling_frequency


def calculate_sampling_frequency_from_timestamps(timestamps: pd.DatetimeIndex) -> int:
    """Calculates the sampling frequency from the timestamp column in dataframe"""
    ts_data_ns = timestamps.astype(np.uint64).to_numpy()
    deltas = np.diff(ts_data_ns) / 1e9
    sampling_freq = 1 / deltas.mean()
    return round(sampling_freq)
