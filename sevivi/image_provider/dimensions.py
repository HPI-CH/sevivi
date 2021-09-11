from dataclasses import dataclass
from typing import Generator


@dataclass
class Dimensions:
    """Used to store width and height of an image in a single object"""

    w: int
    """width in pixels"""
    h: int
    """height in pixels"""

    def __iter__(self) -> Generator[int, None, None]:
        """
        Iterate over width, height.
        Can be used to convert this into a (width, height) tuple by calling
        tuple(dimension)
        """
        yield self.w
        yield self.h
