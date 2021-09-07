import pytest

from sevivi.config import config_reader
from sevivi.config.config_types.sensor_config import (
    ManuallySynchronizedSensorConfig,
    ImuSynchronizedSensorConfig,
    JointSynchronizedSensorConfig,
    SensorConfig,
)
from sevivi.config.config_types.video_config import (
    CameraImuVideoConfig,
    KinectVideoConfig,
    RawVideoConfig,
    OpenPoseVideoConfig,
)
from sevivi.image_provider import AzureProvider
from sevivi.video_renderer import VideoRenderer
from sevivi.video_renderer.instantiation_helpers import (
    instantiate_video_provider,
    instantiate_graph_providers,
    video_renderer_from_csv_files,
)


def test_instantiate_cam_imu_video_provider():
    with pytest.raises(NotImplementedError):
        instantiate_video_provider(CameraImuVideoConfig())


def test_instantiate_kinect_video_provider(run_in_repo_root):
    assert isinstance(
        instantiate_video_provider(
            KinectVideoConfig(
                path="test_files/videos/joint_synchronization_squatting.mp4",
                skeleton_path="test_files/skeletons/joint_synchronization_squatting/positions_3d.csv.gz",
            )
        ),
        AzureProvider,
    )


def test_instantiate_raw_video_provider():
    with pytest.raises(NotImplementedError):
        instantiate_video_provider(RawVideoConfig())


def test_instantiate_openpose_video_provider():
    with pytest.raises(NotImplementedError):
        instantiate_video_provider(OpenPoseVideoConfig())


def test_instantiate_unknown_video_provider():
    with pytest.raises(RuntimeError):
        # noinspection PyTypeChecker
        instantiate_video_provider(3)


def test_instantiate_unknown_graph_provider_config(run_in_repo_root):
    with pytest.raises(RuntimeError):
        # noinspection PyTypeChecker
        instantiate_graph_providers(
            {"1": SensorConfig("test_files/sensors/imu_synchronization/LF.csv.gz")}
        )


def test_instantiate_graph_providers(run_in_repo_root):
    # noinspection PyTypeChecker
    configs = {
        "1": ManuallySynchronizedSensorConfig(
            path="test_files/sensors/imu_synchronization/LF.csv.gz"
        ),
        "2": ImuSynchronizedSensorConfig(
            path="test_files/sensors/imu_synchronization/LF.csv.gz"
        ),
        "3": JointSynchronizedSensorConfig(
            path="test_files/sensors/joint_synchronization_squatting/LF.csv.gz"
        ),
    }
    result = instantiate_graph_providers(configs)
    assert len(result) == 3


def test_video_renderer_from_csv_files(run_in_repo_root):
    config = config_reader.read_configs(
        (
            "test_files/configs/basic_config.toml",
            "test_files/test-data-configs/kinect_sync_3d_hand_movement.toml",
        )
    )
    result = video_renderer_from_csv_files(config)
    assert isinstance(result, VideoRenderer)
