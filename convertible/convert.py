from typing import Callable, Optional

from .ignore_self import ignore_self, FunctionMethodAdaptor
from .Convert.Convert import Convert
from .Convert.ConvertHandler.ConvertHandler import ConvertHandler
from .Convert.ExceptionHandler.ExceptionHandler import ExceptionHandler


def convert(
    convert_handler: ConvertHandler, exception_handler: Optional[ExceptionHandler] = None
) -> Callable[[Callable], FunctionMethodAdaptor]:
    """
    A function to provide a descriptor of type Convert.
    Unlike if it was called normally, this function will strip the self argument off of classes called.

    Parameters
    ----------
    convert_handler : ConvertHandler
        The handler containing the Convertibles to automatically convert arguments.
    exception_handler : Optional[ExceptionHandler], optional
        The handler for any ConvertExceptions, by default None
        If None is provided, then no Exceptions will be caught automatically.

    Returns
    -------
    Callable[[Callable], Convert]
        A descriptor with the Convert instance, which will ignore the self argument of classes.
    """

    @ignore_self
    def convert(func: Callable) -> Convert:
        """The middle wrapper for the decorator"""

        return Convert(func, convert_handler, exception_handler)

    return convert
