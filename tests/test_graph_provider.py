from datetime import datetime

import pandas as pd
import pytest

from sevivi.image_provider.graph_provider.graph_provider import GraphImageProvider


def test_get_image_for_time_stamp():
    dti = pd.to_datetime(
        [datetime(2018, 1, 3), datetime(2018, 1, 2), datetime(2018, 1, 1)]
    )
    df = pd.DataFrame(data={"A": [1, 2, 3]}, index=dti)
    graph_image_provider = GraphImageProvider(df)
    with pytest.raises(NotImplementedError):
        # noinspection PyTypeChecker
        graph_image_provider.get_image_for_time_stamp(None)


def test_set_offset_positive():
    dti = pd.to_datetime(
        [datetime(2018, 1, 3), datetime(2018, 1, 2), datetime(2018, 1, 1)]
    )
    df = pd.DataFrame(data={"A": [1, 2, 3]}, index=dti)
    graph_image_provider = GraphImageProvider(df)
    graph_image_provider.set_offset(pd.Timedelta(days=1))
    new_index = graph_image_provider.get_sync_data_frame().index
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
    graph_image_provider = GraphImageProvider(df)
    graph_image_provider.set_offset(pd.Timedelta(days=-1))
    new_index = graph_image_provider.get_sync_data_frame().index
    # noinspection PyUnresolvedReferences
    assert (
        new_index
        == pd.to_datetime(
            [datetime(2018, 1, 2), datetime(2018, 1, 1), datetime(2018, 1, 3)]
        )
    ).all()


def test_get_sync_data_frame():
    dti = pd.to_datetime(
        [datetime(2018, 1, 1), datetime(2018, 1, 2), datetime(2018, 1, 3)]
    )
    df = pd.DataFrame(data={"A": [1, 2, 3]}, index=dti)
    graph_image_provider = GraphImageProvider(df)
    assert df is graph_image_provider.get_sync_data_frame()


def test_get_sync_data_frame_bad_index():
    with pytest.raises(ValueError):
        GraphImageProvider(pd.DataFrame())
