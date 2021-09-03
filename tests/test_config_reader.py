import os
import pytest
from sevivi.config import config_reader, PlottingMethod, StackingDirection
from sevivi.config.config_reader import deep_update


@pytest.fixture(scope="function")
def run_in_repo_root(request):
    if os.getcwd().endswith("tests"):
        os.chdir("..")
    yield
    os.chdir(request.config.invocation_dir)


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
    assert config_reader.merge_config_files(("test_files/configs/basic_config.toml",)) is not None


def test_multi_config(run_in_repo_root):
    config = config_reader.merge_config_files(("test_files/configs/basic_config.toml",))
    config_multi = config_reader.merge_config_files((
        "test_files/configs/basic_config.toml",
        "test_files/configs/basic_config.toml",
    ))
    assert config == config_multi

    config_parallel_ingest = config_reader.merge_config_files((
        "test_files/configs/basic_config.toml",
        "test_files/configs/use_parallel_ingestion.toml",
    ))
    assert config_parallel_ingest["use_parallel_image_ingestion"] is True


def test_get_bool(run_in_repo_root):
    config = config_reader.merge_config_files((
        "test_files/configs/basic_config.toml",
        "test_files/configs/use_parallel_ingestion.toml",
    ))
    assert config_reader.get_bool(config, "use_parallel_image_ingestion") is True


def test_plotting_method(run_in_repo_root):
    config = config_reader.merge_config_files(("test_files/configs/basic_config.toml",))
    assert config_reader.get_plotting_method(config) == PlottingMethod.MOVING_VERTICAL_LINE
    config = config_reader.merge_config_files(("test_files/configs/push_in_plotting_method.toml",))
    assert config_reader.get_plotting_method(config) == PlottingMethod.PUSH_IN


def test_stack_direction(run_in_repo_root):
    config = config_reader.merge_config_files(("test_files/configs/basic_config.toml",))
    assert config_reader.get_stacking_direction(config) == StackingDirection.HORIZONTAL
    config = config_reader.merge_config_files(("test_files/configs/vertical_stacking.toml",))
    assert config_reader.get_stacking_direction(config) == StackingDirection.VERTICAL


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
