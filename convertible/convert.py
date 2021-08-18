from typing import Callable
from functools import wraps

from .Convertible import Convertible
from .ignore_self import ignore_self


def convert(*args: Convertible, **kwargs: Convertible):
    """
    A decorator to automatically convert types with Convertibles.
    """

    convertable_args = args
    convertable_kwargs = kwargs

    @ignore_self
    def convert(func: Callable):
        """The middle wrapper for the decorator"""

        @wraps(func)
        def convert(*args, **kwargs):
            """
            For each argument provided, we will try to find a convertible.
            If none are found, then we will just pass the value provided.
            """

            new_args, new_kwargs = [], {}
            for idx, arg in enumerate(args):
                try:
                    new_args.append(convertable_args[idx].convert(arg))
                except IndexError:
                    new_args.append(arg)
            for idx, (key, value) in enumerate(kwargs.items()):
                try:
                    new_kwargs.update({key: convertable_kwargs[key].convert(value)})
                except KeyError:
                    new_kwargs.update({key: value})
            return func(*new_args, **new_kwargs)

        return convert

    return convert
