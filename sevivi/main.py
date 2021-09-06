from argparse import ArgumentParser

from sevivi.config import Config
from sevivi.config.config_reader import read_configs


def parse_arguments() -> Config:
    """Parse the config file locations from input args and return the specified configuration"""
    parser = ArgumentParser()
    parser.add_argument("config", nargs="+")
    args = parser.parse_args()
    return read_configs(args.config)


if __name__ == "__main__":
    config = parse_arguments()
