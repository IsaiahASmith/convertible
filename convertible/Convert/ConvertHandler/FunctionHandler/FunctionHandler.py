from typing import Type, Dict, Callable, Optional, Tuple, Iterator
from collections import deque
from inspect import getfullargspec

from . import Convertibles
from .FunctionArgumentHandler import FunctionArgumentHandler
from .FunctionKeywordArgumentHandler import FunctionKeywordArgumentHandler
from convertible.Convertible import Convertible


class FunctionIterator:
    def __init__(
        self,
        argument_handler: FunctionArgumentHandler,
        keyword_handler: FunctionKeywordArgumentHandler,
        *args,
        **kwargs,
    ):
        self.args = deque(args)
        self.kwargs = kwargs
        self.argument_handler = argument_handler
        self.keyword_handler = keyword_handler

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.argument_handler}, {self.keyword_handler})"

    def __iter__(self):
        def iterator():
            for (name, convertible) in self.argument_convertibles:
                try:
                    arg = self.args.popleft()
                except IndexError:
                    if name in self.kwargs:
                        arg = self.kwargs[name]
                        del self.kwargs[name]
                    else:
                        arg = None
                yield convertible.convert(arg)

            arguments_convertible = self.arguments_convertible
            while True:
                try:
                    arg = self.args.popleft()
                except IndexError:
                    break

                try:
                    convertible = next(arguments_convertible)
                except StopIteration:
                    convertible = None
                if convertible is not None:
                    yield convertible.convert(arg)
                else:
                    yield arg

            for name, convertible in self.keyword_only_convertibles.items():
                if name in self.kwargs:
                    kwarg = self.kwargs[name]
                    del self.kwargs[name]
                else:
                    kwarg = None
                yield convertible.convert(kwarg)

            for name, kwarg in self.kwargs.items():
                if name in self.keyword_arguments_convertible:
                    convertible = self.keyword_arguments_convertible[name]
                    del self.keyword_arguments_convertible[name]
                    yield convertible.convert(kwarg)
                else:
                    yield kwarg

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


class FunctionHandler:
    __slots__ = ("argument_handler", "keyword_handler")

    def __init__(
        self,
        argument_handler: FunctionArgumentHandler,
        keyword_handler: FunctionKeywordArgumentHandler,
    ):
        self.argument_handler = argument_handler
        self.keyword_handler = keyword_handler

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.argument_handler}, {self.keyword_handler})"

    def __call__(self, *args, **kwargs):
        pass

    @classmethod
    def from_function(
        cls,
        function: Callable,
        convertibles: Convertibles,
        argument_handler: Optional[Type[FunctionArgumentHandler]] = None,
        keyword_handler: Optional[Type[FunctionKeywordArgumentHandler]] = None,
    ):
        args, varargs, varkw, _, kwonlyargs, _, _ = getfullargspec(function)
        argument_handler = argument_handler or FunctionArgumentHandler
        keyword_handler = keyword_handler or FunctionKeywordArgumentHandler
        return cls(
            argument_handler.from_function(args, varargs, convertibles),
            keyword_handler.from_function(set(kwonlyargs), varkw, convertibles[1]),
        )
