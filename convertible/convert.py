from typing import Callable, Tuple, Dict, List, Any

from .Convertible import Convertible
from .ignore_self import ignore_self


class ConvertHandler:
    def __init__(self, *args: Convertible, **kwargs: Convertible):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs) -> Tuple[List[Any], Dict[str, Any]]:
        """
        For each argument provided, we will try to find a convertible.
        If none are found, then we will just pass the value provided.
        """
        new_args, new_kwargs = [], {}
        for idx, arg in enumerate(args):
            try:
                new_args.append(self.args[idx].convert(arg))
            except IndexError:
                new_args.append(arg)
        for idx, (key, value) in enumerate(kwargs.items()):
            try:
                new_kwargs.update({key: self.kwargs[key].convert(value)})
            except KeyError:
                new_kwargs.update({key: value})
        return new_args, new_kwargs


class Convert:
    def __init__(self, function: Callable, handler: ConvertHandler):
        self.function = function
        self.handler = handler

    def __get__(self, obj, type):
        if obj is None:
            return self
        return self.function

    def __call__(self, *args, **kwargs):
        new_args, new_kwargs = self.handler(*args, **kwargs)
        return self.function(*new_args, **new_kwargs)


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
