from typing import Optional

from convertible.Convertible import Convertible


class NextArgumentException(Exception):
    """
    An exception to request the next element of the iterator.
    """

    def __init__(self, convertible: Convertible, message: Optional[str] = None):
        self.convertible = convertible
        super().__init__(message or f"{self.convertible} requested the next argument")
