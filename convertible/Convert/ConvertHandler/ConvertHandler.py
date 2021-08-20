from typing import Tuple, Any, Iterator

from convertible.Convertible import Convertible


class _InnerArgIterator:
    """
    The actual class that handles the iteration of arguments.
    Unlike the outer class, the index of argument to be check can be modified.
    This enables Convert and other subclasses to implement Convertibles that can take multiple arguments.
    """

    def __init__(self, convertibles: Tuple[Convertible, ...], *args: Any):
        self.convertibles = convertibles
        self.args = args
        self.index = -1

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.args})"

    def __iter__(self) -> "_InnerArgIterator":
        return self

    def get_next(self) -> Any:
        self.index += 1
        if self.index < len(self.args):
            return self.args[self.index]
        else:
            raise StopIteration

    def undo(self):
        self.index -= 1
        if self.index < 0:
            raise IndexError(f"{self} cannot have an index below zero")

    def __next__(self):
        arg = self.get_next()
        if self.index < len(self.convertibles):
            return self.convertibles[self.index].convert(arg)
        else:
            return arg


class _ConvertArgsIterator:
    __slots__ = ("convertibles",)

    def __init__(self, *convertibles: Convertible):
        self.convertibles = convertibles

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.convertibles})"

    def __call__(self, *args: Any) -> _InnerArgIterator:
        return iter(_InnerArgIterator(self.convertibles, *args))


class _ConvertKwargsIterator:
    __slots__ = ("convertibles",)

    def __init__(self, **convertibles: Convertible):
        self.convertibles = convertibles

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.convertibles})"

    def __call__(self, **kwargs) -> Iterator:
        class _InnerKwargIterator:
            def __init__(_self, **kwargs):
                _self.kwargs = kwargs

            def __repr__(_self) -> str:
                return f"{_self.__class__.__name__}({_self.kwargs})"

            def __iter__(_self):
                for key, value in kwargs.items():
                    if key in self.convertibles:
                        yield key, self.convertibles[key].convert(value)
                    else:
                        yield key, value

        return iter(_InnerKwargIterator(**kwargs))


class ConvertHandler:
    __slots__ = ("args_converter", "kwargs_converter")

    def __init__(self, *args: Convertible, **kwargs: Convertible):
        self.args_converter = _ConvertArgsIterator(*args)
        self.kwargs_converter = _ConvertKwargsIterator(**kwargs)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.args_converter.convertibles}, {self.kwargs_converter.convertibles})"

    def __call__(self, *args, **kwargs) -> Tuple[_InnerArgIterator, Iterator[Tuple[str, Any]]]:
        """
        The args and kwargs passed to this method represent the arguments passed to the inner function
        of the convert descriptor.
        This method will provide an iterator for the args and kwargs, respectively.
        If a Convertible was provided for the given argument or kwarg, then it will attempt to convert it.
        If there is no Convertible, then the argument will be unaffected.

        Returns
        -------
        Tuple[Iterable[Any], Iterable[Tuple[str, Any]]]
            An iterator for the args and kwargs passed to the inner function, respectively.
        """
        return self.args_converter(*args), self.kwargs_converter(**kwargs)
