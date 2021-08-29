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
    def __init__(self, function: Callable, convertible_callable: ConvertibleCallable):
        self.handler = FunctionHandler.from_function(function, convertible_callable)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.handler})"

    def __call__(self, *args, **kwargs) -> Tuple[List[Any], Dict[str, Any]]:
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
        if convert_argument.convertible is None:
            return convert_argument.keyword, convert_argument.argument

        return convert_argument.keyword, self._convert(
            function_iterator, convert_argument.convertible, convert_argument.argument
        )

    def _convert(self, function_iterator: FunctionIterator, convertible: Convertible, argument: Any):
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
