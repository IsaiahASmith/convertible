from typing import Any

from .Convertible import Convertible


class Ignore(Convertible):
    """
    A Convertible that does not convert the type
    """

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def convert(self, argument: Any) -> Any:
        """
        Converts the argument provided to a specified type.

        Parameters
        ----------
        argument : Any
            The argument to be converted.
        """
        return argument
