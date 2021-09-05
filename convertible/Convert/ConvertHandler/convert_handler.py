from typing import Callable

from convertible.Convertible.Convertible import Convertible

from .ConvertHandler import ConvertHandler
from .FunctionHandler.ConvertibleCallable import ConvertibleCallable


def convert_handler(*args: Convertible, **kwargs: Convertible):
    """
    A decorator to help instantiate the ConvertHandler without before the function is created.

    Parameters
        ----------
        convertible_callable : ConvertibleCallable
            The *args and **kwargs of the Convertibles that are to be associated with the function or method.
    """

    def convert_handler(function: Callable) -> ConvertHandler:
        """
        The inner function that is responsible for creating the ConvertHandler.

        Parameters
        ----------
        function : Callable
            The function to be called with the converted arguments.

        Returns
        -------
        ConvertHandler
            The handler responsible for converting all the Convertibles to arguments.
        """
        return ConvertHandler.from_function(function, ConvertibleCallable(args, kwargs))

    return convert_handler
