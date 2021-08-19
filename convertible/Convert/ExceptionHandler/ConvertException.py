from typing import Optional, Any


from convertible.Convertible import Convertible


class ConvertException(Exception):
    """
    An exception that is raised when Convert cannot convert the argument.
    """

    def __init__(self, convert: Convertible, argument: Any, message: Optional[str] = None):
        self.convert = convert
        self.argument = argument
        super().__init__(message or f"{self.convert} was unable to convert {self.argument}")
