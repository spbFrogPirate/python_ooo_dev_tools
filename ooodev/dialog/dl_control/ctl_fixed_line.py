# region imports
from __future__ import annotations
from typing import cast, TYPE_CHECKING
import uno  # pylint: disable=unused-import

from .ctl_base import DialogControlBase

if TYPE_CHECKING:
    from com.sun.star.awt import UnoControlFixedLine  # service
    from com.sun.star.awt import UnoControlFixedLineModel  # service
# endregion imports


class CtlFixedLine(DialogControlBase):
    """Class for Fixed Line Control"""

    # pylint: disable=unused-argument

    # region init
    def __init__(self, ctl: UnoControlFixedLine) -> None:
        """
        Constructor

        Args:
            ctl (UnoControlFixedLine): Fixed Line Control
        """
        # generally speaking EventArgs.event_data will contain the Event object for the UNO event raised.
        DialogControlBase.__init__(self, ctl)

    # endregion init

    # region Overrides
    def get_view_ctl(self) -> UnoControlFixedLine:
        return cast("UnoControlFixedLine", super().get_view_ctl())

    def get_uno_srv_name(self) -> str:
        """Returns ``com.sun.star.awt.UnoControlFixedLine``"""
        return "com.sun.star.awt.UnoControlFixedLine"

    def get_model(self) -> UnoControlFixedLineModel:
        """Gets the Model for the control"""
        return cast("UnoControlFixedLineModel", self.get_view_ctl().getModel())

    # endregion Overrides

    # region Properties
    @property
    def view(self) -> UnoControlFixedLine:
        return self.get_view_ctl()

    @property
    def model(self) -> UnoControlFixedLineModel:
        return self.get_model()

    # endregion Properties
