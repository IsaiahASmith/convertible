from typing import Callable

from .Convertible import Convertible
from .ignore_self import ignore_self
from .Convert.Convert import Convert
from .Convert.ConvertHandler.ConvertHandler import ConvertHandler


def convert(*args: Convertible, **kwargs: Convertible):
    """
    A decorator to automatically convert types with Convertibles.
    """

    convertable_args = args
    convertable_kwargs = kwargs

    @ignore_self
    def convert(func: Callable):
        """The middle wrapper for the decorator"""

        return Convert(func, ConvertHandler(*convertable_args, **convertable_kwargs))

    return convert
