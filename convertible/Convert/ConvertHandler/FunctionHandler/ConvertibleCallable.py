from typing import Tuple, Dict, NamedTuple
from convertible.Convertible import Convertible


class ConvertibleCallable(NamedTuple):
    """
    A representation of the Convertibles passed in a decorator that represent the arguments and keyword
    arguments of a function or method.
    """

    convertible_arguments: Tuple[Convertible, ...]
    convertible_keyword_arguments: Dict[str, Convertible]
