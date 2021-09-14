from typing import TypeVar, Generator, List, Tuple, Iterable

T = TypeVar("T")


def progress_bar(
    iterable: Iterable[T],
    total: int,
    prefix="",
    suffix="",
    decimals=1,
    length=100,
    fill="█",
) -> Generator[Tuple[int, T], None, None]:
    """
    Call in a loop to create terminal progress bar. Adapted from https://stackoverflow.com/a/34325723.
    Yields

    :param iterable:    - Required  : Items from this list will be yielded to the for-loop
    :param total:       - Required  : Number of items that will be yielded
    :param prefix:      - Optional  : prefix string (Str)
    :param suffix:      - Optional  : suffix string (Str)
    :param decimals:    - Optional  : positive number of decimals in percent complete (Int)
    :param length:      - Optional  : character length of bar (Int)
    :param fill:        - Optional  : bar fill character (Str)
    """

    # Progress Bar Printing Function
    def print_progress_bar(iteration):
        percent = ("{0:." + str(decimals) + "f}").format(
            100 * (iteration / float(total))
        )
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + "-" * (length - filledLength)
        print(f"\r{prefix} |{bar}| {percent}% {suffix}", end="\r")

    # Initial Call
    print_progress_bar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield i, item
        print_progress_bar(i + 1)
    # Print New Line on Complete
    print()
