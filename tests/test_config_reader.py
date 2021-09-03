from copy import deepcopy

import os
import pytest
from sevivi.config import config_reader, Config


@pytest.fixture(scope="function")
def run_in_repo_root(request):
    if os.getcwd().endswith("tests"):
        os.chdir("..")
    yield
    os.chdir(request.config.invocation_dir)


def test_default_config():
    with pytest.raises(ValueError):
        config_reader.read_configs()


def test_missing_config_file():
    with pytest.raises(FileNotFoundError):
        config_reader.read_configs(("lnjaerovfgnaeorcin",))


def test_single_config(run_in_repo_root):
    assert config_reader.read_configs(("test_files/configs/basic_config.toml",)) is not None


def test_get_bool(run_in_repo_root):
    assert config_reader.get_bool("use_parallel_image_ingestion")
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
