from typing import Dict, Tuple, Iterator, Any
from itertools import chain
from collections import deque

from .ConvertibleArgument import ConvertibleArgument
from .ConvertArgument import ConvertArgument
from .FunctionArgumentHandler import FunctionArgumentHandler
from .FunctionKeywordArgumentHandler import FunctionKeywordArgumentHandler
from convertible.Convertible import Convertible


class FunctionIterator:
    __slots__ = ("argument_handler", "keyword_handler", "args", "kwargs")

    def __init__(
        self,
        argument_handler: FunctionArgumentHandler,
        keyword_handler: FunctionKeywordArgumentHandler,
        args: Tuple[Any, ...],
        kwargs: Dict[str, Any],
    ):
        """
        Initializes an Iterator to iterate through the tuple pairs of names and convertibles

        Parameters
        ----------
        argument_handler : FunctionArgumentHandler
            The handler in charge of handling finding *args.
        keyword_handler : FunctionKeywordArgumentHandler
            The handler in charge of handling finding **kwargs.
        args : Tuple[Any, ...]
            The arguments passed to the function or method.
        kwargs : Dict[str, Any]
            The keyword arguments passed to the function or method.
        """
        self.args = deque(args)
        self.kwargs = kwargs
        self.argument_handler = argument_handler
        self.keyword_handler = keyword_handler

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.argument_handler}, {self.keyword_handler})"

    def __iter__(self):
        return chain(
            self.argument_convertibles_iterator(),
            self.arguments_convertible_iterator(),
            self.keyword_only_convertibles_iterator(),
            self.keyword_arguments_convertible_iterator(),
        )

    def argument_convertibles_iterator(self) -> Iterator[ConvertArgument]:
        """
        Provides an iterator to standardize the argument convertibles to a ConvertArgument.

        Yields
        -------
        Iterator[ConvertArgument]
            The representation of an argument requested by Convert.
        """
        for (name, convertible) in self.argument_convertibles:
            try:
                arg = self.args.popleft()
            except IndexError:
                arg = self.kwargs.pop(name, None)
            yield ConvertArgument(None, convertible, arg)

    def arguments_convertible_iterator(self) -> Iterator[ConvertArgument]:
        """
        Provides an iterator to standardize the argument convertible to a ConvertArgument.

        Yields
        -------
        Iterator[ConvertArgument]
            The representation of an argument requested by Convert.
        """
        arguments_convertible = self.arguments_convertible
        while self.args:
            arg = self.args.popleft()

            try:
                convertible = next(arguments_convertible)
            except StopIteration:
                convertible = None
            yield ConvertArgument(None, convertible, arg)

    def keyword_only_convertibles_iterator(self) -> Iterator[ConvertArgument]:
        """
        Provides an iterator to standardize the keyword only convertibles to a ConvertArgument.

        Yields
        -------
        Iterator[ConvertArgument]
            The representation of an argument requested by Convert.
        """
        for name, convertible in self.keyword_only_convertibles.items():
            kwarg = self.kwargs.pop(name, None)
            yield ConvertArgument(name, convertible, kwarg)

    def keyword_arguments_convertible_iterator(self) -> Iterator[ConvertArgument]:
        """
        Provides an iterator to standardize the keyword arguments convertibles to a ConvertArgument.

        Yields
        -------
        Iterator[ConvertArgument]
            The representation of an argument requested by Convert.
        """
        for name, kwarg in self.kwargs.items():
            convertible = self.keyword_arguments_convertible.pop(name, None)
            yield ConvertArgument(name, convertible, kwarg)

    @property
    def argument_convertibles(self) -> Tuple[ConvertibleArgument, ...]:
        """
        A tuple of convertible arguments correlating to the convertibles and callable provided.

        Note: The only purpose of this property is to provide better extendibility.
            This enables editing the argument convertibles throughout the class without
            needing to change them in their respective instances.

        Returns
        -------
        Tuple[ConvertibleArgument, ...]
            A tuple of convertible arguments correlating to the convertibles and callable provided.
        """
        return self.argument_handler.argument_convertibles

    @property
    def arguments_convertible(self) -> Iterator[Convertible]:
        """
        An iterator to convert an unknown amount of *args ad hoc.

        Note: The only purpose of this property is to provide better extendibility.
            This enables editing the argument convertible throughout the class without
            needing to change them in their respective instances.

        Yields
        -------
        Iterator[Convertible]
            An iterator to convert an unknown amount of *args ad hoc.
        """
        return iter(self.argument_handler.arguments_convertible)

    @property
    def keyword_only_convertibles(self) -> Dict[str, Convertible]:
        """
        A dictionary representing name, Convertible pairs for the keyword arguments of a function or method.

        Note: The only purpose of this property is to provide better extendibility.
            This enables editing the keyword only convertibles throughout the class without
            needing to change them in their respective instances.

        Returns
        -------
        Dict[str, Convertible]
            A dictionary representing name, Convertible pairs for the keyword arguments of a function or method.
        """
        return self.keyword_handler.keyword_only_convertibles

    @property
    def keyword_arguments_convertible(self) -> Dict[str, Convertible]:
        """
        A dictionary representing name, Convertible pairs to convert the unknown **kwargs.

        Note: The only purpose of this property is to provide better extendibility.
            This enables editing the keyword arguments convertible throughout the class without
            needing to change them in their respective instances.

        Returns
        -------
        Dict[str, Convertible]
            A dictionary representing name, Convertible pairs to convert the unknown **kwargs.
        """
        return self.keyword_handler.keyword_arguments_convertible
