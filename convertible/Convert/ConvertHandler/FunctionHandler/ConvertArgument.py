from typing import NamedTuple, Optional, Any
from convertible.Convertible import Convertible


class ConvertArgument(NamedTuple):
    """
    A representation of the arguments requested by Convert.
    This includes:
        an optional keyword for the name of the argument,
        an optional convertible to convert the argument if present,
        and the argument passed.
    """

    keyword: Optional[str]
    convertible: Optional[Convertible]
    argument: Any
