from typing import Optional, List, Any

from convertible.Convertible.Convertible import Convertible


class RejectArgumentException(Exception):
    """
    An exception to request the next element of the iterator.
    """

    def __init__(
        self, convertible: Convertible, rejected_arguments: List[Any], result: Any, message: Optional[str] = None
    ):
        """
        Creates an exception to denote that the last argument was not used, and to push this to the iterator.

        Parameters
        ----------
        convertible : Convertible
            The Convertible that rejected the last input.
        result : Any
            The final result o the Convertible, as the Convertible will not be called again.
        rejected_arguments: List[Any]
            The arguments that were taken but not utilized by the Convertible.
        message : Optional[str], optional
            The message of the exception if it is not caught, by default None
            If None is passed, a message will automatically be provided.
        """
        self.convertible = convertible
        self.result = result
        self.rejected_arguments = rejected_arguments
        super().__init__(message or f"The {self.convertible} returned {self.result} and rejected the last argument")
