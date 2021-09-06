import pytest

from sevivi.config import Config
from sevivi.main import parse_arguments


def test_parse_arguments_empty():
    with pytest.raises(SystemExit):
        parse_arguments([])


def test_parse_arguments_missing_config_file():
    with pytest.raises(FileNotFoundError):
        parse_arguments(["amrnvo;eurnvf"])


def test_parse_arguments_single(run_in_repo_root):
    isinstance(parse_arguments(["test_files/test-data-configs/imu_sync.toml"]), Config)


def test_parse_arguments_multiple(run_in_repo_root):
    isinstance(
        parse_arguments(
            [
                "test_files/test-data-configs/imu_sync.toml",
                "test_files/configs/vertical_stacking.toml",
            ]
        ),
        Config,
    )
