from typing import List, Any, Optional

from convertible.Convert.NextArgumentException import NextArgumentException
from convertible.Convert.RejectArgumentException import RejectArgumentException
from convertible.Convert.ExceptionHandler.ConvertException import ConvertException
from convertible.Convert.Convert import NoMoreArguments

from .Convertible import Convertible


class Greedy(Convertible):
    """
    A Convertible that will continue to ask for more arguments until it runs into a ConvertException or
    is provided the argument of StopIterator.
    Once the Convertible is stopped, it will raise a RejectArgumentException with itself and the final result.
    """

    __slots__ = ("convertible", "_results")

    def __init__(self, convertible: Convertible, *, _results: Optional[List] = None):
        """
        Initialize a Greedy Convertible.

        Parameters
        ----------
        convertible : Convertible
            The Convertible that convert until an invalid argument rises.
        _results : Optional[List]
            During the Converting of multiple variables, _results maintains the list of the prior results.
        """
        self.convertible = convertible
        self._results = _results or []

    def __repr__(self) -> str:
        if self.convertible is self:
            if self._results:
                return f"{self.__class__.__name__}(..., _results={self._results})"
            else:
                return f"{self.__class__.__name__}(...)"
        else:
            if self._results:
                return f"{self.__class__.__name__}({self.convertible}, _results={self._results})"
            else:
                return f"{self.__class__.__name__}({self.convertible})"

    def _return_results(self):
        """
        Returns the results by raising a RejectArgumentException.
        This method also cleans up the results, for it to be called again.

        Raises
        ------
        RejectArgumentException
            Raises an exception to declare that the last argument was not used and returns the result.
        """
        self._results, results = [], self._results
        raise RejectArgumentException(self, results)

    def convert(self, argument: Any) -> None:
        """
        Converts the argument provided to a specified type.

        Parameters
        ----------
        argument : Any
            The argument to be converted.

        Raises
        ------
        NextArgumentException
            Raises an exception to request another argument.
        """
        if isinstance(argument, NoMoreArguments):
            self._return_results()

        try:
            res = self.convertible.convert(argument)
        except ConvertException:
            self._return_results()

        raise NextArgumentException(Greedy(self.convertible, _results=self._results + [res]))
