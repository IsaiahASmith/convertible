from typing import Type, Callable, Dict

from .ConvertException import ConvertException


class ExceptionHandler:
    def __init__(self, handlers: Dict[Type[Exception], Callable]):
        self.handlers = handlers

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.handlers})"

    def __call__(self, exception: ConvertException):
        if (type_ := type(exception)) in self.handlers.keys():
            self.handlers[type_](exception.convert, exception.argument)
        else:
            raise exception
