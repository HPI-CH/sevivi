import pytest

from sevivi.image_provider.video_provider.video_provider import VideoImageProvider


def test_get_offset():
    with pytest.raises(NotImplementedError):
        # noinspection PyTypeChecker
        VideoImageProvider(None).get_offset(None)
