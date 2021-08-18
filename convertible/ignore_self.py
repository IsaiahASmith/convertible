from typing import Callable, Any


def ignore_self(decorator: Callable[[Callable], Any]):
    """
    A decorator to ignore the self variable passed for classes.
    This will automatically strip the variable if required.

    Parameters
    ----------

    decorator : Callable[[Callable], Any]
        The decorator that should ignore the self variable.
    """

    class FunctionMethodAdaptor:
        """
        A descriptor to peak to see if it is a method or function at runtime.
        """

        def __init__(self, decorator: Callable[[Callable], Any], func: Callable):
            self.decorator = decorator
            self.func = func

        def __get__(self, instance, owner):
            return self.decorator(self.func.__get__(instance, owner))

        def __call__(self, *args, **kwargs):
            return self.decorator(self.func)(*args, **kwargs)

    def ignore_self(func: Callable):
        return FunctionMethodAdaptor(decorator, func)

    return ignore_self
