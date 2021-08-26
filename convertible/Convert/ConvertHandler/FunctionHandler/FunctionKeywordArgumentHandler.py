from typing import Dict, Optional, Set

from convertible.Convertible import Convertible


def get_keyword_only_convertibles(kwonlyargs: Set[str], convertibles: Dict[str, Convertible]) -> Dict[str, Convertible]:
    """
    Finds the keyword only argument Convertibles by looking for Convertibles passed by a keyword argument
        and finding the argument inside the function or method.

    Parameters
    ----------
    kwonlyargs : Set[str]
        A set of all keyword arguments inside the function or method passed.
    convertibles : Dict[str, Convertible]
        A dictionary containing all the name and Convertible pairs.

    Returns
    -------
    Dict[str, Convertible]
        A dictionary containing all the name and Convertible pairs for keyword only arguments.
    """
    return {name: convertibles[name] for name in set(convertibles.keys()).intersection(kwonlyargs)}


def get_keyword_arguments_convertible(
    keyword_only_convertibles: Dict[str, Convertible], varkw: Optional[str], convertibles: Dict[str, Convertible]
) -> Dict[str, Convertible]:
    """
    Finds the keyword arguments passed through **kwargs.

    Parameters
    ----------
    keyword_only_convertibles : Dict[str, Convertible]
        A dictionary containing all the name and Convertible pairs for keyword only arguments.
    varkw : Optional[str]
        The name representing **kwargs.
    convertibles : Dict[str, Convertible]
        A dictionary containing all the name and Convertible pairs.

    Returns
    -------
    Dict[str, Convertible]
        A dictionary containing all the name and Convertible pairs for **kwarg.
    """
    if varkw is None:
        return {}
    return {name: convertibles[name] for name in convertibles.keys() - keyword_only_convertibles.keys()}


class FunctionKeywordArgumentHandler:
    __slots__ = ("keyword_only_convertibles", "keyword_arguments_convertible")

    def __init__(
        self,
        keyword_only_convertibles: Dict[str, Convertible],
        keyword_arguments_convertible: Dict[str, Convertible],
    ):
        """
        Initializes the handler with how to convert keyword arguments for a function or method.

        Parameters
        ----------
        keyword_only_convertibles : Dict[str, Convertible]
            A dictionary representing name, Convertible pairs for the keyword arguments of a function or method.
        keyword_arguments_convertible : Dict[str, Convertible]
            A dictionary representing name, Convertible pairs to convert the unknown **kwargs.
        """
        self.keyword_only_convertibles = keyword_only_convertibles
        self.keyword_arguments_convertible = keyword_arguments_convertible

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.keyword_only_convertibles}, {self.keyword_arguments_convertible})"

    @classmethod
    def from_function(cls, kwonlyargs: Set[str], varkw: Optional[str], convertibles: Dict[str, Convertible]):
        """
        Initializes the handler from variables associated with inspecting a function or method.

        Parameters
        ----------
        kwonlyargs : Set[str]
            The keyword only arguments of a function or method.
        varkw : Optional[str]
            The name of the **kwargs variable, if one is present.
        convertibles : Dict[str, Convertible]
            The name, Convertible pairs for the keyword arguments handled by Convertibles.
        """
        return cls(
            (keyword_only_convertibles := get_keyword_only_convertibles(kwonlyargs, convertibles)),
            get_keyword_arguments_convertible(keyword_only_convertibles, varkw, convertibles),
        )
