from typing import Callable

from .ConvertHandler.ConvertHandler import ConvertHandler


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
