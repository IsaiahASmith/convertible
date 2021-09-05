from typing import Tuple, List, Optional, Iterable

from .ConvertibleCallable import ConvertibleCallable
from .ConvertibleArgument import ConvertibleArgument
from ..Iterable import ConvertIterable
from convertible.Convertible.Convertible import Convertible
from convertible.Convertible.Ignore import Ignore


def _get_argument_convertibles(
    args: List[str], convertibles: Tuple[Convertible, ...], is_method: bool = False
) -> Tuple[ConvertibleArgument, ...]:
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
    is_method: bool
        Determines if the first parameter should be ignored, by default False.

    Returns
    -------
    Tuple[Tuple[str, Convertible], ...]
        The list of argument names and their respective Convertible.
    """
    if is_method:
        return _get_argument_convertibles(args[1:], (Ignore(), *convertibles))
    return tuple([ConvertibleArgument(name, convertible) for name, convertible in zip(args, convertibles)])


def _get_arguments_convertible(
    argument_convertibles: Tuple[Tuple[str, Convertible], ...],
    varargs: Optional[str],
    convertibles: ConvertibleCallable,
) -> Iterable[Convertible]:
    """
    Finds the Convertibles associated with *args.
    If None are found, then the function will search for a keyword for the *arg variable name instead.
    Note: If a Convertible is provided with a keyword, then it will be assumed to be a keyword only
        argument.  All argument Convertibles must be passed as arguments, not keywords.

    Parameters
    ----------
    argument_convertibles : Tuple[Tuple[str, Convertible], ...]
        A Tuple containing both the argument and keyword arguments for the function or method, respectively.
    varargs : Optional[str]
        The name of the *args variable inside the function or method.
    convertibles : ConvertibleCallable
        A Tuple containing both the argument and keyword arguments for the Convertibles, respectively.

    Returns
    -------
    Iterable[Convertible]
        An Iterable that will provide a Convertible for each arg in *args to be converted.
    """
    if varargs is None:
        return ConvertIterable()
    if (args_len := len(argument_convertibles)) > len(convertibles[0]):
        if varargs in convertibles[1]:
            return convertibles.convertible_keyword_arguments[varargs]
        return ConvertIterable()
    return ConvertIterable(convertibles.convertible_arguments[args_len:])


class FunctionArgumentHandler:
    """
    A class to find the arguments of a function or method.
    """

    __slots__ = ("argument_convertibles", "arguments_convertible")

    def __init__(
        self, argument_convertibles: Tuple[ConvertibleArgument, ...], arguments_convertible: Iterable[Convertible]
    ):
        """
        Initializes the handler with how to convert arguments for a function or method.

        Parameters
        ----------
        argument_convertibles : Tuple[ConvertibleArgument, ...]
            A tuple of tuples representing the name of the argument and its corresponding convertible.
        arguments_convertible : Iterable[Convertible]
            An iterator to convert an unknown amount of *args ad hoc.
        """
        self.argument_convertibles = argument_convertibles
        self.arguments_convertible = arguments_convertible

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.argument_convertibles}, {self.arguments_convertible})"

    @classmethod
    def from_function(
        cls, args: List[str], varargs: Optional[str], convertibles: ConvertibleCallable, is_method: bool = False
    ):
        """
        Initializes the handler from variables associated from inspecting a function or method.

        Parameters
        ----------
        args : List[str]
            The list of names for the arguments of a function.
        varargs : Optional[str]
            The name of the *args variable, if one is present.
        convertibles : ConvertibleCallable
            A Tuple containing both the argument and keyword arguments for the Convertibles, respectively.
        """
        return cls(
            (argument_convertibles := _get_argument_convertibles(args, convertibles[0], is_method)),
            _get_arguments_convertible(argument_convertibles, varargs, convertibles),
        )
