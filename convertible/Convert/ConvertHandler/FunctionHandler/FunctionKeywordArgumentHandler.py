from typing import Dict, Optional, Set

from convertible.Convertible import Convertible


class FunctionKeywordArgumentHandler:
    __slots__ = ("keyword_only_convertibles", "keyword_arguments_convertible")

    def __init__(self, kwonlyargs: Set[str], varkw: Optional[str], convertibles: Dict[str, Convertible]):
        self.keyword_only_convertibles = self.get_keyword_only_convertibles(kwonlyargs, convertibles)
        self.keyword_arguments_convertible = self.get_keyword_arguments_convertible(varkw, convertibles)

    def get_keyword_only_convertibles(
        self, kwonlyargs: Set[str], convertibles: Dict[str, Convertible]
    ) -> Dict[str, Convertible]:
        return {name: convertibles[name] for name in set(convertibles.keys()).intersection(kwonlyargs)}

    def get_keyword_arguments_convertible(
        self, varkw: Optional[str], convertibles: Dict[str, Convertible]
    ) -> Dict[str, Convertible]:
        if varkw is None:
            return {}
        return {name: convertibles[name] for name in convertibles.keys() - self.keyword_only_convertibles.keys()}
