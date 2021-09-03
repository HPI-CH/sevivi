import os
from typing import Dict, List

import pandas as pd
import pytest
from sevivi.config import config_reader, PlottingMethod, StackingDirection, VideoConfig
from sevivi.config.config_reader import deep_update
from sevivi.config.config_types.sensor_config import SensorConfig, ManuallySynchronizedSensorConfig, \
    JointSynchronizedSensorConfig, ImuSynchronizedSensorConfig
from sevivi.config.config_types.video_config import CameraImuVideoConfig, KinectVideoConfig, OpenPoseVideoConfig, \
    RawVideoConfig


@pytest.fixture(scope="function")
def run_in_repo_root(request):
    if os.getcwd().endswith("tests"):
        os.chdir("..")
    yield
    os.chdir(request.config.invocation_dir)


def test_combination(run_in_repo_root):
    config = config_reader.read_configs((
        "test_files/configs/basic_config.toml",
        "test_files/configs/video_configs/kinect.toml",
        "test_files/configs/sensor_configs/camera_imu_synchronization.toml",
        "test_files/configs/sensor_configs/joint_synchronization.toml",
        "test_files/configs/sensor_configs/manual_synchronization.toml",
    ))
    print(config)


def test_zero_config():
    with pytest.raises(ValueError):
        # noinspection PyTypeChecker
        config_reader.read_configs(None)
    with pytest.raises(ValueError):
        config_reader.read_configs(())


def test_missing_config_file():
    with pytest.raises(FileNotFoundError):
        config_reader.merge_config_files(("lnjaerovfgnaeorcin",))
    with pytest.raises(FileNotFoundError):
        config_reader.read_configs(("lnjaerovfgnaeorcin",))


def test_single_config_file(run_in_repo_root):
    assert _conf_dict("basic_config") is not None


def test_multi_config(run_in_repo_root):
    config = _conf_dict("basic_config")
    config_multi = _conf_dict("basic_config", "basic_config")
    assert config == config_multi

    config_parallel_ingest = _conf_dict("basic_config", "use_parallel_ingestion")
    assert config_parallel_ingest["use_parallel_image_ingestion"] is True


def test_get_bool(run_in_repo_root):
    config = _conf_dict("basic_config", "use_parallel_ingestion")
    assert config_reader.get_bool(config, "use_parallel_image_ingestion") is True

    with pytest.raises(ValueError):
        config_reader.get_bool(config, "stacking_direction")


def test_plotting_method(run_in_repo_root):
    config = _conf_dict("basic_config")
    assert config_reader.get_plotting_method(config) == PlottingMethod.MOVING_VERTICAL_LINE

    config = _conf_dict("push_in_plotting_method")
    assert config_reader.get_plotting_method(config) == PlottingMethod.PUSH_IN

    with pytest.raises(KeyError):
        config_reader.get_plotting_method(_conf_dict("bad_plotting_method"))


def test_stack_direction(run_in_repo_root):
    config = _conf_dict("basic_config")
    assert config_reader.get_stacking_direction(config) == StackingDirection.HORIZONTAL

    config = _conf_dict("vertical_stacking")
    assert config_reader.get_stacking_direction(config) == StackingDirection.VERTICAL

    with pytest.raises(KeyError):
        config_reader.get_stacking_direction(_conf_dict("bad_stacking"))


def test_read_imu_video_config(run_in_repo_root):
    imu_conf = _vid_conf("imu")
    assert imu_conf.path == "test_files/kinect.mkv"
    assert isinstance(imu_conf, CameraImuVideoConfig)
    assert imu_conf.imu_path == "test_files/kinect_imu.csv.gz"
    assert imu_conf.camera_imu_sync_column == ["AX", "Accel Y"]


def test_read_kinect_video_config(run_in_repo_root):
    imu_conf = _vid_conf("kinect")
    assert imu_conf.path == "test_files/kinect.mkv"
    assert isinstance(imu_conf, KinectVideoConfig)
    assert imu_conf.skeleton_path == "test_files/kinect.csv.gz"


def test_read_openpose_video_config(run_in_repo_root):
    imu_conf = _vid_conf("openpose")
    assert imu_conf.path == "test_files/openpose.mkv"
    assert isinstance(imu_conf, OpenPoseVideoConfig)


def test_read_raw_video_config(run_in_repo_root):
    imu_conf = _vid_conf("raw")
    assert imu_conf.path == "test_files/raw.mkv"
    assert isinstance(imu_conf, RawVideoConfig)


def test_dual_imu(run_in_repo_root):
    conf = _sensor_conf("dual_imu_base")
    assert len(conf) == 2


def test_base_imu(run_in_repo_root):
    conf = _sensor_conf("single_imu_base")
    assert len(conf) == 1
    conf = conf["0"]
    assert isinstance(conf, ManuallySynchronizedSensorConfig)
    assert conf.offset_seconds == 0.0


def test_manual_sync_imu(run_in_repo_root):
    conf = _sensor_conf("manual_synchronization")
    assert len(conf) == 1
    conf = conf["0"]
    assert isinstance(conf, ManuallySynchronizedSensorConfig)
    assert conf.offset_seconds == 123.4


def test_joint_sync_imu(run_in_repo_root):
    conf = _sensor_conf("joint_synchronization")
    assert len(conf) == 1
    conf = conf["0"]
    assert isinstance(conf, JointSynchronizedSensorConfig)
    assert conf.sync_joint_name == "ANKLE"
    assert conf.sensor_sync_axes == ["AccX", "Accel Y", "ACC Z"]
    assert conf.joint_sync_axis == "ACCELERATION_MAG"


def test_camera_sync_imu(run_in_repo_root):
    conf = _sensor_conf("camera_imu_synchronization")
    assert len(conf) == 1
    conf = conf["0"]
    assert isinstance(conf, ImuSynchronizedSensorConfig)
    assert conf.sensor_sync_column == ['AccX', 'Accel Y']
    assert conf.path == "test_files/camera_imu.csv.gz"


def test_camera_sync_imu_single_col(run_in_repo_root):
    conf = _sensor_conf("camera_imu_synchronization_single_col")
    assert len(conf) == 1
    conf = conf["0"]
    assert isinstance(conf, ImuSynchronizedSensorConfig)
    assert conf.sensor_sync_column == "AccX"
    assert conf.path == "test_files/camera_imu.csv.gz"


def test_imu_merging(run_in_repo_root):
    conf = _sensor_conf("single_imu_base", "single_imu_base")
    assert len(conf) == 2
    assert conf["0"] == conf["1"]


def test_sensor_with_end_time(run_in_repo_root):
    conf = _sensor_conf("end_time")
    assert len(conf) == 1
    conf = conf["0"]
    assert isinstance(conf.end_time, pd.Timestamp)


def test_sensor_with_start_time(run_in_repo_root):
    conf = _sensor_conf("start_time")
    assert len(conf) == 1
    conf = conf["0"]
    assert isinstance(conf.start_time, pd.Timestamp)


def test_sensor_with_start_and_end_time(run_in_repo_root):
    conf = _sensor_conf("start_end_time")
    assert len(conf) == 1
    conf = conf["0"]
    assert isinstance(conf.start_time, pd.Timestamp)
    assert isinstance(conf.end_time, pd.Timestamp)


def test_sensor_missing_attributes(run_in_repo_root):
    with pytest.raises(KeyError):
        _sensor_conf("missing_attributes")


def test_video_missing_attributes(run_in_repo_root):
    with pytest.raises(KeyError):
        _vid_conf("missing_attributes")


def _vid_conf(*names: str) -> VideoConfig:
    files = [f"test_files/configs/video_configs/{name}.toml" for name in names]
    return config_reader.get_video_config(config_reader.merge_config_files(tuple(files)))


def _sensor_conf(*names: str) -> Dict[str, SensorConfig]:
    files = [f"test_files/configs/sensor_configs/{name}.toml" for name in names]
    return config_reader.get_sensor_configs(config_reader.merge_config_files(tuple(files)))


def _conf_dict(*names: str) -> Dict:
    files = [f"test_files/configs/{name}.toml" for name in names]
    return config_reader.merge_config_files(tuple(files))


def test_deep_update():
    """
    Mostly from charlax, surjikal

    https://stackoverflow.com/a/18394648
    https://stackoverflow.com/a/30655448
    """
    source = {'hello1': 1}
    overrides = {'hello2': 2}
    deep_update(source, overrides)
    assert source == {'hello1': 1, 'hello2': 2}

    source = {'hello': 'to_override'}
    overrides = {'hello': 'over'}
    deep_update(source, overrides)
    assert source == {'hello': 'over'}

    source = {'hello': {'value': 'to_override', 'no_change': 1}}
    overrides = {'hello': {'value': 'over'}}
    deep_update(source, overrides)
    assert source == {'hello': {'value': 'over', 'no_change': 1}}

    source = {'hello': {'value': 'to_override', 'no_change': 1}}
    overrides = {'hello': {'value': {}}}
    deep_update(source, overrides)
    assert source == {'hello': {'value': {}, 'no_change': 1}}

    source = {'hello': {'value': {}, 'no_change': 1}}
    overrides = {'hello': {'value': 2}}
    deep_update(source, overrides)
    assert source == {'hello': {'value': 2, 'no_change': 1}}
