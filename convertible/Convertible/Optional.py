from typing import Any

from convertible.Convert.ExceptionHandler.ConvertException import ConvertException

from .Convertible import Convertible


class Optional(Convertible):
    """
    A Convertible that will either Convert the argument with the Convertible provided or return None.
    """

    __slots__ = ("convertible",)

    def __init__(self, convertible: Convertible):
        """
        Initialize a Optional Convertible.

        Parameters
        ----------
        convertible : Convertible
            The Convertible that convert or provide an exception.
        """
        self.convertible = convertible

    def convert(self, argument: Any) -> Any:
        """
        Converts the argument to the specified type of the Convertible provided or returns None.

        Parameters
        ----------
        argument : Any
            The argument to be converted.

        Returns
        -------
        Any
            The converted argument or None.
        """
        try:
            return self.convertible.convert(argument)
        except ConvertException:
            return None
        except StopIteration:
            return None
