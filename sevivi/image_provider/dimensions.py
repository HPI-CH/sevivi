from dataclasses import dataclass
from typing import Generator


@dataclass
class Dimensions:
    w: int
    """width in pixels"""
    h: int
    """height in pixels"""

    def __iter__(self) -> Generator[int, None, None]:
        yield self.w
        yield self.h
