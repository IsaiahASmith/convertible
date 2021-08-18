from typing import Tuple, List, Any, Dict

from convertible.Convertible import Convertible


class ConvertHandler:
    def __init__(self, *args: Convertible, **kwargs: Convertible):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs) -> Tuple[List[Any], Dict[str, Any]]:
        """
        For each argument provided, we will try to find a convertible.
        If none are found, then we will just pass the value provided.
        """
        new_args, new_kwargs = [], {}
        for idx, arg in enumerate(args):
            try:
                new_args.append(self.args[idx].convert(arg))
            except IndexError:
                new_args.append(arg)
        for idx, (key, value) in enumerate(kwargs.items()):
            try:
                new_kwargs.update({key: self.kwargs[key].convert(value)})
            except KeyError:
                new_kwargs.update({key: value})
        return new_args, new_kwargs
