from datetime import datetime

import pandas as pd
import pytest

from sevivi.config import (
    RenderConfig,
    SensorConfig,
    ImuSynchronizedSensorConfig,
    ManuallySynchronizedSensorConfig,
    JointSynchronizedSensorConfig,
    find_matching_columns,
    get_graph_groups,
)
from sevivi.image_provider import GraphImageProvider


def test_graph_count():
    dti = pd.to_datetime([datetime(2018, 1, 3)])
    df = pd.DataFrame(data={"A_x": [1], "A_y": [1], "A_z": [1], "G_x": [1]}, index=dti)
    assert (
        GraphImageProvider(
            df, RenderConfig(), SensorConfig(graph_groups=["A_"])
        ).get_graph_count()
        == 1
    )
    assert (
        GraphImageProvider(
            df, RenderConfig(), SensorConfig(graph_groups=["A_", "G_"])
        ).get_graph_count()
        == 2
    )
    assert (
        GraphImageProvider(
            df, RenderConfig(), SensorConfig(graph_groups=["_"])
        ).get_graph_count()
        == 1
    )


def test_get_sync_dataframe_cam_imu():
    dti = pd.to_datetime([datetime(2018, 1, 3)])
    df = pd.DataFrame(data={"A_x": [1], "A_y": [1], "A_z": [1], "G_x": [1]}, index=dti)
    gip = GraphImageProvider(df, RenderConfig(), SensorConfig())

    gip.sensor_config = ImuSynchronizedSensorConfig(sensor_sync_column_selection="A_")
    assert gip.get_sync_dataframe().columns.tolist() == ["A_x", "A_y", "A_z"]

    gip.sensor_config = ImuSynchronizedSensorConfig(
        sensor_sync_column_selection=["A_x"]
    )
    assert gip.get_sync_dataframe().columns.tolist() == ["A_x"]

    gip.sensor_config = ImuSynchronizedSensorConfig(
        sensor_sync_column_selection=["N/A"]
    )
    with pytest.raises(ValueError):
        gip.get_sync_dataframe()


def test_get_sync_dataframe_joints():
    dti = pd.to_datetime([datetime(2018, 1, 3)])
    df = pd.DataFrame(data={"A_x": [1], "A_y": [1], "A_z": [1], "G_x": [1]}, index=dti)
    gip = GraphImageProvider(df, RenderConfig(), SensorConfig())

    gip.sensor_config = JointSynchronizedSensorConfig(sensor_sync_column_selection="A_")
    assert gip.get_sync_dataframe().columns.tolist() == ["A_x", "A_y", "A_z"]

    gip.sensor_config = JointSynchronizedSensorConfig(
        sensor_sync_column_selection=["A_x"]
    )
    assert gip.get_sync_dataframe().columns.tolist() == ["A_x"]

    gip.sensor_config = JointSynchronizedSensorConfig(
        sensor_sync_column_selection=["N/A"]
    )
    with pytest.raises(ValueError):
        gip.get_sync_dataframe()


def test_get_sync_data_frame_manual():
    dti = pd.to_datetime(
        [datetime(2018, 1, 1), datetime(2018, 1, 2), datetime(2018, 1, 3)]
    )
    df = pd.DataFrame(data={"A": [1, 2, 3]}, index=dti)
    gip = GraphImageProvider(df, RenderConfig(), ManuallySynchronizedSensorConfig())
    assert gip.get_sync_dataframe() is None


def test_render_graph_axes():
    dti = pd.to_datetime(
        [datetime(2018, 1, 3), datetime(2018, 1, 2), datetime(2018, 1, 1)]
    )
    df = pd.DataFrame(data={"A": [1, 2, 3]}, index=dti)
    graph_image_provider = GraphImageProvider(df, RenderConfig(), SensorConfig())
    graph_image_provider.render_graph_axes(None, None)


def test_set_offset_positive():
    dti = pd.to_datetime(
        [datetime(2018, 1, 3), datetime(2018, 1, 2), datetime(2018, 1, 1)]
    )
    df = pd.DataFrame(data={"A": [1, 2, 3]}, index=dti)
    graph_image_provider = GraphImageProvider(
        df, RenderConfig(), ManuallySynchronizedSensorConfig()
    )
    graph_image_provider.set_offset(pd.Timedelta(days=1))
    new_index = graph_image_provider._data.index
    # noinspection PyUnresolvedReferences
    assert (
        new_index
        == pd.to_datetime(
            [datetime(2018, 1, 4), datetime(2018, 1, 3), datetime(2018, 1, 2)]
        )
    ).all()


def test_set_offset_negative():
    dti = pd.to_datetime(
        [datetime(2018, 1, 3), datetime(2018, 1, 2), datetime(2018, 1, 4)]
    )
    df = pd.DataFrame(data={"A": [1, 2, 3]}, index=dti)
    graph_image_provider = GraphImageProvider(
        df, RenderConfig(), ManuallySynchronizedSensorConfig()
    )
    graph_image_provider.set_offset(pd.Timedelta(days=-1))
    new_index = graph_image_provider._data.index
    # noinspection PyUnresolvedReferences
    assert (
        new_index
        == pd.to_datetime(
            [datetime(2018, 1, 2), datetime(2018, 1, 1), datetime(2018, 1, 3)]
        )
    ).all()


def test_get_sync_data_frame_bad_index():
    with pytest.raises(ValueError):
        GraphImageProvider(pd.DataFrame(), RenderConfig(), SensorConfig())


def test_get_graph_groups():
    df = pd.DataFrame(
        data={"A_x": [1], "A_y": [1], "A_z": [1], "G_x": [1]},
        index=pd.to_datetime([datetime(2018, 1, 3)]),
    )
    assert get_graph_groups(df, ["A_"]) == {"A_": ["A_x", "A_y", "A_z"]}
    assert get_graph_groups(df, ["A_", "G_"]) == {
        "A_": ["A_x", "A_y", "A_z"],
        "G_": ["G_x"],
    }
    assert get_graph_groups(df, ["_"]) == {"_": ["A_x", "A_y", "A_z", "G_x"]}
    assert get_graph_groups(df, ["A_x"]) == {"A_x": ["A_x"]}


def test_find_matching_columns():
    df = pd.DataFrame(
        data={"A_x": [1], "A_y": [1], "A_z": [1], "G_x": [1]},
        index=pd.to_datetime([datetime(2018, 1, 3)]),
    )
    assert find_matching_columns(df, "A_") == ["A_x", "A_y", "A_z"]
    assert find_matching_columns(df, ["A_x"]) == ["A_x"]

    with pytest.raises(ValueError):
        find_matching_columns(df, ["N/A"])
