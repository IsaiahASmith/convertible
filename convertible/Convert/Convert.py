from typing import Callable, Optional, Iterator, Any, List, Dict

from convertible.Convertible import Convertible

from .NextArgumentException import NextArgumentException
from .ConvertHandler.ConvertHandler import ConvertHandler
from .ExceptionHandler.ExceptionHandler import ExceptionHandler
from .ExceptionHandler.ConvertException import ConvertException


class Convert:
    def __init__(
        self, function: Callable, convert_handler: ConvertHandler, exception_handler: Optional[ExceptionHandler] = None
    ):
        """
        Initializes the Convert class, which acts as a callable descriptor.

        Parameters
        ----------
        function : Callable
            The function we are decorating.
        convert_handler : ConvertHandler
            The convert handler provided.
            This manages the many Convertibles for arguments and keyword arguments, respectively.
        exception_handler : Optional[ExceptionHandler], optional
            The manager for any exceptions, by default None
            This will be called if a ConvertHandler raises a ConvertException.
            If None is provided, the ConvertExceptions will leak passed the Convert class.
        """
        self.function = function
        self.convert_handler = convert_handler
        self.exception_handler = exception_handler or ExceptionHandler({})

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.function}, {self.convert_handler}, {self.exception_handler})"

    def __get__(self, obj, type):
        if obj is None:
            return self
        return self.function

    def __call__(self, *args, **kwargs):
        """
        The actual decorator for the descriptor.  When called, this will automatically convert all eligible arguments.
        """
        args_iter, kwargs_iter = self.convert_handler(*args, **kwargs)
        return self.function(*self._get_arguments(args_iter), **self._get_keyword_arguments(kwargs_iter))

    def _validate(self, iterator: Iterator) -> Any:
        """
        Validates a Convertible and handles simple exceptions.

        Parameters
        ----------
        iterator : Iterator
            The iterator yielding the next result.

        Returns
        -------
        Any
            The argument provided after converting it or leaving it as is.
        """
        try:
            return next(iterator)
        except ConvertException as exception:
            self.exception_handler(exception)

    def _handle_next_argument_convertible(self, iterator: Iterator, convertible: Convertible) -> Any:
        """
        Some Convertibles can request to have an additional argument provided.
        To provide the extra arguments, this method pulls the next argument from the iterator.

        Parameters
        ----------
        iterator : Iterator
            The iterator yielding the next result.
        convertible : Convertible
            The argument provided after converting it or leaving it as is.
        arguments: List
            The arguments that are currently provided to the convertible.
        """

        try:
            # The Iterator will be of type _InnerArgIterator, having the method get_next.
            argument = iterator.get_next()
        except StopIteration:
            # StopIteration is passed to the convertible to indicate that there are no more arguments.
            argument = StopIteration

        try:
            return convertible.convert(argument)
        except NextArgumentException as exception:
            return self._handle_next_argument_convertible(iterator, exception.convertible)
        except ConvertException as exception:
            self.exception_handler(exception)

    def _validate_args(self, iterator: Iterator) -> Any:
        """
        Provides an extra series of checks for simple exceptions, to provide the ability to combine
        multiple arguments together to form types such as lists and sets.

        Parameters
        ----------
        iterator : Iterator
            The iterator yielding the next result.

        Returns
        -------
        Any
            The argument provided after converting it or leaving it as is.
        """
        try:
            return self._validate(iterator)
        except NextArgumentException as exception:
            return self._handle_next_argument_convertible(iterator, exception.convertible)

    def _get_arguments(self, iterator: Iterator, *args: Any) -> List[Any]:
        """
        Generates the a list of all the arguments passed from __call__.

        Parameters
        ----------
        iterator : Iterator
            The argument iterator that will automatically convert the arguments specified.
        args: Any
            The arguments passed to __call__.

        Returns
        -------
        List[Any]
            The results of the arguments if no exceptions occur.
        """
        new_args = []
        while True:
            try:
                new_args.append(self._validate_args(iterator))
            except StopIteration:
                break
        return new_args

    def _get_keyword_arguments(self, iterator: Iterator, **kwargs: Any) -> Dict[str, Any]:
        """
        Generates the a list of all the keyword arguments passed from __call__.

        Parameters
        ----------
        iterator : Iterator
            The keyword argument iterator that will automatically convert the keyword arguments specified.
        kwargs : Any
            The keyword arguments passed to __call__.

        Returns
        -------
        Dict[str, Any]
            The results of the keyword arguments if no exceptions occur.
        """
        new_kwargs = {}
        while True:
            try:
                key, value = self._validate_args(iterator)
            except StopIteration:
                break
            new_kwargs.update({key: value})
        return new_kwargs
