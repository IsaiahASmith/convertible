from typing import Callable, Optional

from .ConvertHandler.ConvertHandler import ConvertHandler
from .ExceptionHandler.ExceptionHandler import ExceptionHandler
from .ExceptionHandler.ConvertException import ConvertException


class Convert:
    __slots__ = ("function", "convert_handler", "exception_handler")

    def __init__(
        self, function: Callable, convert_handler: ConvertHandler, exception_handler: Optional[ExceptionHandler] = None
    ):
        """
        Initializes the Convert class, which acts as a callable descriptor.

        Parameters
        ----------
        function : Callable
            The function we are decorating.
        convert_handler : ConvertHandler
            The convert handler provided.
            This manages the many Convertibles for arguments and keyword arguments, respectively.
        exception_handler : Optional[ExceptionHandler], optional
            The manager for any exceptions, by default None
            This will be called if a ConvertHandler raises a ConvertException.
            If None is provided, the ConvertExceptions will leak passed the Convert class.
        """
        self.function = function
        self.convert_handler = convert_handler
        self.exception_handler = exception_handler or ExceptionHandler({})

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.function}, {self.convert_handler}, {self.exception_handler})"

    def __get__(self, obj, type):
        if obj is None:
            return self
        return self.function

    def __call__(self, *args, **kwargs):
        """
        The true decorator of the descriptor.  Everything must go through here.
        """
        try:
            _args, _kwargs = self.convert_handler(*args, **kwargs)
        except ConvertException as exception:
            self.exception_handler(exception)
            return
        return self.function(*_args, **_kwargs)
