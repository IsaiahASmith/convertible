from typing import NamedTuple
from convertible.Convertible import Convertible


class ConvertibleArgument(NamedTuple):
    """
    A representation of a decorated argument that is being extended by a Convertible.
    """

    argument_name: str
    convertible: Convertible
