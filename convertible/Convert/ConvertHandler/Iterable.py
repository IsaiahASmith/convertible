from typing import Tuple, Optional

from convertible.Convertible.Convertible import Convertible


class ConvertIterable:
    """
    A Convertible that will unpack a series of convertibles, similar to *args.
    """

    __slots__ = ("convertibles",)

    def __init__(self, convertibles: Optional[Tuple[Convertible, ...]] = None):
        """
        Initializes the Convertible to provide

        Parameters
        ----------
        convertibles : Optional[List[Convertible]], optional
            [description], by default None
        """
        self.convertibles = convertibles if convertibles is not None else []

    def __iter__(self):
        def convert_iterator():
            """
            Iterate over the convertibles inside ConvertIterable
            """
            for convertible in self.convertibles:
                yield convertible

        return convert_iterator()
