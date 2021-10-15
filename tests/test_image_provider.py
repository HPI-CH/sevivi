import pandas as pd

from sevivi import video_renderer_from_csv_files, read_configs

import pytest


def test_get_sync_dataframe_wrong_type(run_in_repo_root):
    config = read_configs(("test_files/test-data-configs/kinect_sync_walking.toml",))
    ap = video_renderer_from_csv_files(config).video_provider

    with pytest.raises(TypeError):
        ap.get_sync_dataframe(5)


def test_get_sync_dataframe_wrong_joint(run_in_repo_root):
    config = read_configs(("test_files/test-data-configs/kinect_sync_walking.toml",))
    ap = video_renderer_from_csv_files(config).video_provider

    with pytest.raises(KeyError):
        ap.get_sync_dataframe("Unknown_Joint")


def test_get_sync_dataframe_wrong_joint_in_list(run_in_repo_root):
    config = read_configs(("test_files/test-data-configs/kinect_sync_walking.toml",))
    ap = video_renderer_from_csv_files(config).video_provider

    with pytest.raises(KeyError):
        ap.get_sync_dataframe(["PELVIS (x)", "UNKNOWN_JOINT"])


def test_get_sync_dataframe_result_from_list(run_in_repo_root):
    config = read_configs(("test_files/test-data-configs/kinect_sync_walking.toml",))
    ap = video_renderer_from_csv_files(config).video_provider
    sync_axes = ["PELVIS (x)", "PELVIS (y)", "PELVIS (z)"]

    df = ap.get_sync_dataframe(sync_axes)
    assert isinstance(df, pd.DataFrame)
    assert len(df.columns) == 3
    assert all(elem in df.columns for elem in sync_axes)


def test_get_sync_dataframe_result_from_str(run_in_repo_root):
    config = read_configs(("test_files/test-data-configs/kinect_sync_walking.toml",))
    ap = video_renderer_from_csv_files(config).video_provider

    sync_joint = "PELVIS (x)"
    df = ap.get_sync_dataframe(sync_joint)
    assert isinstance(df, pd.DataFrame)
    assert len(df.columns) == 1
    assert df.columns[0] == sync_joint
