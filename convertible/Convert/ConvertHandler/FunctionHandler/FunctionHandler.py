from typing import Type, Dict, Callable, Optional, Tuple, Iterator
from inspect import getfullargspec

from . import Convertibles
from .FunctionArgumentHandler import FunctionArgumentHandler
from .FunctionKeywordArgumentHandler import FunctionKeywordArgumentHandler
from convertible.Convertible import Convertible


class FunctionHandler:
    __slots__ = ("argument_handler", "keyword_handler")

    def __init__(
        self,
        function: Callable,
        convertibles: Convertibles,
        argument_handler: Optional[Type[FunctionArgumentHandler]] = None,
        keyword_handler: Optional[Type[FunctionKeywordArgumentHandler]] = None,
    ):
        args, varargs, varkw, _, kwonlyargs, _, _ = getfullargspec(function)
        argument_handler = argument_handler or FunctionArgumentHandler
        keyword_handler = keyword_handler or FunctionKeywordArgumentHandler
        self.argument_handler = argument_handler(args, varargs, convertibles)
        self.keyword_handler = keyword_handler(set(kwonlyargs), varkw, convertibles[1])

    @property
    def argument_convertibles(self) -> Tuple[Tuple[str, Convertible], ...]:
        return self.argument_handler.argument_convertibles

    @property
    def arguments_convertible(self) -> Iterator[Convertible]:
        return iter(self.argument_handler.arguments_convertible)

    @property
    def keyword_only_convertibles(self) -> Dict[str, Convertible]:
        return self.keyword_handler.keyword_only_convertibles

    @property
    def keyword_arguments_convertible(self) -> Dict[str, Convertible]:
        return self.keyword_handler.keyword_arguments_convertible
