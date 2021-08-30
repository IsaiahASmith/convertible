from typing import Tuple, Callable, Dict, Any, Optional, List

from ..NextArgumentException import NextArgumentException
from ..RejectArgumentException import RejectArgumentException
from .FunctionHandler.FunctionHandler import FunctionHandler
from .FunctionHandler.ConvertibleCallable import ConvertibleCallable
from .FunctionHandler.FunctionIterator import FunctionIterator
from .FunctionHandler.ConvertArgument import ConvertArgument
from convertible.Convertible import Convertible


class NoMoreArguments:
    """A class to indicate when there are no more arguments from the iterator"""


class ConvertHandler:
    def __init__(self, handler: FunctionHandler):
        """
        Initializes the handler to be able to provide the *args and **kwargs after converting.

        Parameters
        ----------
        handler : FunctionHandler
            The handler that determines how the Convertibles interact.
        """
        self.handler = handler

    @classmethod
    def from_function(cls, function: Callable, convertible_callable: ConvertibleCallable):
        """
        Creates a function handler using the default parameters to initialize the handler with.

        Parameters
        ----------
        function : Callable
            The function that the FunctionHandler will inspect.
        convertible_callable : ConvertibleCallable
            The *args and **kwargs of the Convertibles that are to be associated with the function or method.
        """
        return cls(FunctionHandler.from_function(function, convertible_callable))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.handler})"

    def __call__(self, *args, **kwargs) -> Tuple[List[Any], Dict[str, Any]]:
        """
        Takes the arguments passed to the function and converts them automatically to *args and **kwargs.

        Returns
        -------
        Tuple[List[Any], Dict[str, Any]]
            The *args and **kwargs to be passed to the function.

        Raises
        ------
        ConvertException
            The 'Convertible' was unable to convert the argument.
        """
        function_iterator = self.handler(*args, **kwargs)
        _args, _kwargs = [], {}
        for convert_argument in iter(function_iterator):
            result = self.convert(function_iterator, convert_argument)
            if (keyword := convert_argument.keyword) is not None:
                _kwargs.update({keyword: result})
            else:
                _args.append(result)
        return _args, _kwargs

    def convert(
        self, function_iterator: FunctionIterator, convert_argument: ConvertArgument
    ) -> Tuple[Optional[str], Any]:
        """
        Converts an argument if applicable.

        If there is no 'Convertible' associated with the argument, then it will simply pass through
        unaffected.  If present, it will continue be handled inside self._convert.

        Parameters
        ----------
        function_iterator : FunctionIterator
            The iterable in charge of finding the convertibles.
        convert_argument : ConvertArgument
            A class containing the key information to handle an argument.

        Returns
        -------
        Tuple[Optional[str], Any]
            The keyword of the argument, if applicable and its result.

        Raises
        ------
        ConvertException
            The 'Convertible' was unable to convert the argument.
        """
        if convert_argument.convertible is None:
            return convert_argument.keyword, convert_argument.argument

        return convert_argument.keyword, self._convert(
            function_iterator, convert_argument.convertible, convert_argument.argument
        )

    def _convert(self, function_iterator: FunctionIterator, convertible: Convertible, argument: Any) -> Any:
        """
        Handles converting an argument using the 'Convertible'.

        Parameters
        ----------
        function_iterator : FunctionIterator
            The iterable in charge of finding the convertibles.
        convertible : Convertible
            The 'Convertible' handling the converting of the argument.
        argument : Any
            The argument to be provided to the 'Convertible'

        Returns
        -------
        Any
            The result from the 'Convertible'.

        Raises
        ------
        ConvertException
            The 'Convertible' was unable to convert the argument.

        Warnings
        --------
        If 'NextArgumentException' is raised with a kwarg, then NoMoreArguments will be provided.

        Notes
        -----
        If no exceptions are raised, then the argument will simply be converted and returned.

        If 'NextArgumentException' is raised, then next argument from the function iterator will be returned
            If no arguments are present, then 'NoMoreArguments' will be passed as the argument to the convertible.

        If 'RejectArgumentException' is raided, then the rejected arguments will be appended to the left
            side of the deque in the order they were popped off.
            The result will be returned from the exception.
        """
        try:
            result = convertible.convert(argument)
        except NextArgumentException as exception:
            try:
                argument = function_iterator.args.popleft()
            except IndexError:
                argument = NoMoreArguments()
            result = self._convert(function_iterator, exception.convertible, argument)
        except RejectArgumentException as exception:
            for argument in exception.rejected_arguments:
                function_iterator.args.appendleft(argument)
            result = exception.result
        return result
