from typing import Type, Callable, Optional
from inspect import getfullargspec

from .ConvertibleCallable import ConvertibleCallable
from .FunctionIterator import FunctionIterator
from .FunctionArgumentHandler import FunctionArgumentHandler
from .FunctionKeywordArgumentHandler import FunctionKeywordArgumentHandler


class FunctionHandler:
    __slots__ = ("argument_handler", "keyword_handler")

    def __init__(
        self,
        argument_handler: FunctionArgumentHandler,
        keyword_handler: FunctionKeywordArgumentHandler,
    ):
        """
        Initializes a the handler with the handles required to determine both *args and **kwargs.

        Parameters
        ----------
        argument_handler : FunctionArgumentHandler
            The handler in charge of handling finding *args.
        keyword_handler : FunctionKeywordArgumentHandler
            The handler in charge of handling finding **kwargs.
        """
        self.argument_handler = argument_handler
        self.keyword_handler = keyword_handler

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.argument_handler}, {self.keyword_handler})"

    def __call__(self, *args, **kwargs) -> FunctionIterator:
        """
        Produces an iterable for iterating over the *args and **kwargs of the function or method.
        This uses the inspection of the handlers to determine

        Returns
        -------
        FunctionIterator
            The iterable in charge of finding the convertibles.
        """
        return FunctionIterator(self.argument_handler, self.keyword_handler, args, kwargs)

    @classmethod
    def from_function(
        cls,
        function: Callable,
        convertibles: ConvertibleCallable,
        argument_handler: Optional[Type[FunctionArgumentHandler]] = None,
        keyword_handler: Optional[Type[FunctionKeywordArgumentHandler]] = None,
    ):
        """
        Inspect the function and utilizes the constructor for the handlers to enable better
        convertible hints.  Specifically, *args can be accessed through a keyword argument, without
        needing explicit declaration.  Overall, this enables an argument to be handled equally
        even if it is called as an arg or kwarg.  The specifics of this is determined by the
        constructor of the respective handlers.

        Parameters
        ----------
        function : Callable
            The function or method to be inspected.
        convertibles : ConvertibleCallable
            The *args and **kwargs of the Convertibles that are to be associated with the function or method.
        argument_handler : Optional[Type[FunctionArgumentHandler]], optional
            The handler for determining the type hints of *args, by default None
            If None is provided, then the default type will be used.
        keyword_handler : Optional[Type[FunctionKeywordArgumentHandler]], optional
            The handler for determining the type hints of **kwargs, by default None
            If None is provided, then the default type will be used.
        """
        args, varargs, varkw, _, kwonlyargs, _, _ = getfullargspec(function)
        argument_handler = argument_handler or FunctionArgumentHandler
        keyword_handler = keyword_handler or FunctionKeywordArgumentHandler
        return cls(
            argument_handler.from_function(args, varargs, convertibles),
            keyword_handler.from_function(set(kwonlyargs), varkw, convertibles[1]),
        )
