from typing import Generic, TypeVar, Callable, Any


Return = TypeVar("Return")


class FunctionMethodAdaptor(Generic[Return]):
    """
    A descriptor to peak to see if it is a method or function at runtime.
    """

    __slots__ = ("decorator", "func")

    # Todo: In Python 3.10 and the addition of PEP 612, add ParamSpec to enable better
    # type hints.  Currently there is no type hints for the arguments passed to the function.
    WrappedFunction = Callable[..., Return]

    def __init__(self, decorator: Callable[[Callable], WrappedFunction], func: Callable):
        self.decorator = decorator
        self.func = func

    def __get__(self, instance, owner):
        return self.decorator(self.func.__get__(instance, owner))

    def __call__(self, *args, **kwargs) -> Return:
        return self.wrapped_function(*args, **kwargs)

    @property
    def wrapped_function(self) -> WrappedFunction:
        return self.decorator(self.func)


def ignore_self(decorator: Callable[[Callable], Any]):
    """
    A decorator to ignore the self variable passed for classes.
    This will automatically strip the variable if required.

    Parameters
    ----------

    decorator : Callable[[Callable], Any]
        The decorator that should ignore the self variable.
    """

    def ignore_self(func: Callable):
        return FunctionMethodAdaptor(decorator, func)

    return ignore_self
