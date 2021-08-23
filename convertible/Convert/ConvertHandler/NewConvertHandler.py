from typing import Tuple, List, Iterator, Callable, Dict, Optional, Set, Iterable
from inspect import getfullargspec

from .Iterable import ConvertIterable
from convertible.Convertible import Convertible


class Convertibles:
    def __init__(self, *args: Convertible, **kwargs: Convertible):
        self.args, self.kwargs = args, kwargs


class ConvertibleNoneArgumentException(Exception):
    pass


class ConvertHandler:
    def __init__(self, function: Callable, convertibles: Convertibles):
        args, varargs, varkw, _, kwonlyargs, _, _ = getfullargspec(function)

        self._argument_convertibles = self._get_argument_convertibles(args, convertibles.args)
        self._arguments_convertible = self._get_arguments_convertible(varargs, convertibles)
        self._keyword_only_convertibles = self._get_keyword_only_convertibles(set(kwonlyargs), convertibles.kwargs)
        self._keyword_arguments_convertible = self._get_keyword_arguments_convertible(varkw, convertibles.kwargs)

    @property
    def argument_convertibles(self) -> Tuple[Tuple[str, Convertible], ...]:
        return self._argument_convertibles

    @property
    def arguments_convertible(self) -> Iterator[Convertible]:
        return iter(self._arguments_convertible)

    @property
    def keyword_only_convertibles(self) -> Dict[str, Convertible]:
        return self._keyword_only_convertibles

    @property
    def keyword_arguments_convertible(self) -> Dict[str, Convertible]:
        return self._keyword_arguments_convertible
