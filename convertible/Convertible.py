from typing import Any
from abc import ABC, abstractmethod


class Convertible(ABC):
    """
    A class to automatically convert an argument
    """

    @abstractmethod
    def convert(self, argument: Any) -> Any:
        """
        Converts the argument provided to a specified type.

        Parameters
        ----------
        argument : Any
            The argument to be converted.
        """
