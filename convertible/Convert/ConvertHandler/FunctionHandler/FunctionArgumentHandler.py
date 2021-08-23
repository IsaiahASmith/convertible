from typing import Tuple, List, Optional, Iterable

from . import Convertibles
from ..Iterable import ConvertIterable
from convertible.Convertible import Convertible


def _get_argument_convertibles(
    args: List[str], convertibles: Tuple[Convertible, ...]
) -> Tuple[Tuple[str, Convertible], ...]:
    """
    Finds the arguments Convertibles and their respective names.
    Note: If a Convertible is provided with a keyword, then it will be assumed to be a keyword only
        argument.  All argument Convertibles must be passed as arguments, not keywords.

    Parameters
    ----------
    args : List[str]
        The arguments' names of the function being decorated.
    convertibles : Tuple[Convertible, ...]
        The Convertibles being applied to the function.

    Returns
    -------
    Tuple[Tuple[str, Convertible], ...]
        The list of argument names and their respective Convertible.
    """
    return tuple([(name, convertible) for name, convertible in zip(args, convertibles)])


def _get_arguments_convertible(
    argument_convertibles: Tuple[Tuple[str, Convertible], ...], varargs: Optional[str], convertibles: Convertibles
) -> Iterable[Convertible]:
    """
    [summary]

    Parameters
    ----------
    argument_convertibles : Tuple[Tuple[str, Convertible], ...]
        [description]
    varargs : Optional[str]
        [description]
    convertibles : Convertibles
        [description]

    Returns
    -------
    Iterable[Convertible]
        [description]
    """
    if varargs is None:
        return ConvertIterable()
    if (args_len := len(argument_convertibles)) > len(convertibles[0]):
        if varargs in convertibles[1]:
            return convertibles[1][varargs]
        return ConvertIterable()
    return ConvertIterable(convertibles.args[args_len:])


class FunctionArgumentHandler:
    __slots__ = ("argument_convertibles", "arguments_convertible")

    def __init__(
        self, argument_convertibles: Tuple[Tuple[str, Convertible], ...], arguments_convertible: Iterable[Convertible]
    ):
        self.argument_convertibles = argument_convertibles
        self.arguments_convertible = arguments_convertible

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.argument_convertibles}, {self.arguments_convertible})"

    @classmethod
    def from_function(cls, args: List[str], varargs: Optional[str], convertibles: Convertibles):
        return cls(
            (argument_convertibles := _get_argument_convertibles(args, convertibles[0])),
            _get_arguments_convertible(argument_convertibles, varargs, convertibles),
        )
