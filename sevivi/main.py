import sys
from argparse import ArgumentParser
from typing import List

from sevivi.config import Config
from sevivi.config.config_reader import read_configs
from sevivi.video_renderer import video_renderer_from_csv_files


def parse_arguments(args: List[str]) -> Config:
    """Parse the config file locations from input args and return the specified configuration"""
    parser = ArgumentParser()
    parser.add_argument(
        "--output",
        dest="target_file_path",
        type=str,
        help="Set the output file. Overwrites config value.",
    )
    parser.add_argument(
        "config",
        nargs="+",
        help="Configuration files. Later files overwrite earlier ones. Only the last video section is used. "
        "All given sensor configs are interpreted as a list, rather than overwriting earlier configuration.",
    )
    args = parser.parse_args(args)
    result = read_configs(args.config)

    if "target_file_path" in args:
        result.render_config.target_file_path = args.target_file_path

    return result


if __name__ == "__main__":
    config = parse_arguments(sys.argv[1:])
    video_renderer = video_renderer_from_csv_files(config)
    video_renderer.render_video()
