# coding: utf-8
from email import message
from pathlib import Path
from typing import Any


class MissingInterfaceError(Exception):
    """Error when a interface is not found for a uno object"""

    def __init__(self, interface: Any, message: Any = None, *args) -> None:
        """
        MissingInterfaceError constructor

        Args:
            interface (Any): Missing Interface that caused error
            message (Any, optional): Message of error
        """
        if message is None:
            try:
                message = f"Missing interface {interface.__pyunointerface__}"
            except AttributeError:
                message = "Missing Uno Interface Error"
        super().__init__(interface, message, *args)

    def __str__(self) -> str:
        return repr(self.args[1])


class CellError(Exception):
    """Cell error"""

    pass


class ConfigError(Exception):
    """Config Error"""

    pass


class PropertyError(Exception):
    """
    Property Error
    """

    def __init__(self, prop_name: str, *args: object) -> None:
        """
        PropertyError Constructor

        Args:
            prop_name (str): Property name that caused error
        """
        super().__init__(prop_name, *args)

    def __str__(self) -> str:
        return repr(f"Property Error for: {self.args[0]}")


class PropertyNotFoundError(PropertyError):
    """Propery Not Found Error"""

    def __str__(self) -> str:
        return repr(f"Property not found for: {self.args[0]}")


class GoalDivergenceError(Exception):
    """Error when goal seek result divergence is too high"""

    def __init__(self, divergence: float, message: Any = None) -> None:
        """
        GoalDivergenceError Constructor

        Args:
            divergence (float): divergence amount
            message (Any, optional): Message of error
        """
        if message is None:
            message = f"Divergence error: {divergence:.4f}"
        super().__init__(divergence, message)

    def __str__(self) -> str:
        return repr(self.args[1])


class UnKnownError(Exception):
    """Error for unnown results"""
    pass

class UnOpenableError(Exception):
    def __init__(self, fnm: str | Path, *args: object) -> None:
        """
        PropertyError Constructor

        Args:
            fnm (str| path): File path that is not openable.
        """
        super().__init__(fnm, *args)

    def __str__(self) -> str:
        return repr(f"Un-openable file: '{self.args[0]}'")