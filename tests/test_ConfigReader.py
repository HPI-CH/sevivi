from copy import deepcopy

import pytest

from sevivi.config.ConfigReader import ConfigReader, default_config


def test_default_config():
    assert ConfigReader.read_configs(()) == default_config, "default config should be used if no overwrites are given"


def test_missing_config_file():
    with pytest.raises(FileNotFoundError):
        ConfigReader.read_configs(("lnjaerovfgnaeorcin",))


def test_single_config():
    config = deepcopy(default_config)
    config["use_parallel_image_ingestion"] = not config["use_parallel_image_ingestion"]

    assert ConfigReader.read_configs()
