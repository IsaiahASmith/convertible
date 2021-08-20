from typing import Tuple, Any, Iterator

from convertible.Convertible import Convertible


class _ConvertArgsIterator:
    __slots__ = ("converts",)

    def __init__(self, *converts: Convertible):
        self.converts = converts

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.converts})"

    def __call__(self, *args: Any) -> Iterator:
        class _InnerArgIterator:
            """
            The actual class that handles the iteration of arguments.
            Unlike the outer class, the index of argument to be check can be modified.
            This enables Convert and other subclasses to implement Convertibles that can take multiple arguments.
            """

            def __init__(_self, *args: Convertible):
                _self.args = args
                _self.index = -1

            def __repr__(_self) -> str:
                return f"{_self.__class__.__name__}({_self.args})"

            def __iter__(_self):
                return _self

            def get_next(_self) -> Any:
                _self.index += 1
                if _self.index < len(_self.args):
                    return _self.args[_self.index]
                else:
                    raise StopIteration

            def undo(_self):
                _self.index -= 1
                if _self.index < 0:
                    raise IndexError(f"{_self} cannot have an index below zero")

            def __next__(_self):
                arg = _self.get_next()
                if _self.index < len(self.converts):
                    return self.converts[_self.index].convert(arg)
                else:
                    return arg

        return iter(_InnerArgIterator(*args))


class _ConvertKwargsIterator:
    __slots__ = ("converts",)

    def __init__(self, **converts: Convertible):
        self.converts = converts

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.converts})"

    def __call__(self, **kwargs) -> Iterator:
        class _InnerKwargIterator:
            def __init__(_self, **kwargs):
                _self.kwargs = kwargs

            def __repr__(_self) -> str:
                return f"{_self.__class__.__name__}({_self.kwargs})"

            def __iter__(_self):
                for key, value in kwargs.items():
                    if key in self.converts:
                        yield key, self.converts[key].convert(value)
                    else:
                        yield key, value

        return iter(_InnerKwargIterator(**kwargs))


class ConvertHandler:
    __slots__ = ("args_converter", "kwargs_converter")

    def __init__(self, *args: Convertible, **kwargs: Convertible):
        self.args_converter = _ConvertArgsIterator(*args)
        self.kwargs_converter = _ConvertKwargsIterator(**kwargs)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.args_converter.converts}, {self.kwargs_converter.converts})"

    def __call__(self, *args, **kwargs) -> Tuple[Iterator[Any], Iterator[Tuple[str, Any]]]:
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
