from copy import deepcopy

import os
import pytest

from sevivi.config import ConfigReader, PlottingMethod, StackingDirection
from sevivi.config.config_reader import default_config


@pytest.fixture(scope="function")
def run_in_repo_root(request):
    if os.getcwd().endswith("tests"):
        os.chdir("..")
    yield
    os.chdir(request.config.invocation_dir)


def test_default_config():
    assert (
        ConfigReader.read_configs(()) == default_config
    ), "default config should be used if no overwrites are given"


def test_missing_config_file():
    with pytest.raises(FileNotFoundError):
        ConfigReader.read_configs(("lnjaerovfgnaeorcin",))


def test_single_config(run_in_repo_root):
    config = deepcopy(default_config)
    config["use_parallel_image_ingestion"] = not config["use_parallel_image_ingestion"]

    assert ConfigReader.read_configs(("test_files/configs/basic_config.toml",))


def test_get_bool(run_in_repo_root):
    assert ConfigReader().get_bool("use_parallel_image_ingestion")
    non_default_config = ("test_files/configs/bool_false.toml",)
    assert not ConfigReader(non_default_config).get_bool("use_parallel_image_ingestion")

    with pytest.raises(KeyError):
        ConfigReader().get_bool("N/A")


def test_plotting_method(run_in_repo_root):
    assert ConfigReader().get_plotting_method() == PlottingMethod.MOVING_VERTICAL_LINE
    non_default_config = ("test_files/configs/push_in_plotting_method.toml",)
    assert (
        ConfigReader(non_default_config).get_plotting_method() == PlottingMethod.PUSH_IN
    )


def test_stack_direction(run_in_repo_root):
    assert ConfigReader().get_stacking_direction() == StackingDirection.HORIZONTAL
    non_default_config = ("test_files/configs/vertical_stacking.toml",)
    assert (
        ConfigReader(non_default_config).get_stacking_direction()
        == StackingDirection.VERTICAL
    )
