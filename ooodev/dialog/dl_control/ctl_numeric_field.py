# region imports
from __future__ import annotations
from typing import Any, cast, TYPE_CHECKING
import contextlib
import uno  # pylint: disable=unused-import

from ooodev.adapter.awt.spin_events import SpinEvents
from ooodev.adapter.awt.text_events import TextEvents
from ooodev.events.args.listener_event_args import ListenerEventArgs
from ooodev.utils.kind.dialog_control_kind import DialogControlKind
from ooodev.utils.kind.dialog_control_named_kind import DialogControlNamedKind

from .ctl_base import DialogControlBase

if TYPE_CHECKING:
    from com.sun.star.awt import UnoControlNumericField  # service
    from com.sun.star.awt import UnoControlNumericFieldModel  # service
# endregion imports


class CtlNumericField(DialogControlBase, SpinEvents, TextEvents):
    """Class for Numeric Field Control"""

    # pylint: disable=unused-argument

    # region init
    def __init__(self, ctl: UnoControlNumericField) -> None:
        """
        Constructor

        Args:
            ctl (UnoControlNumericField): Button Control
        """
        # generally speaking EventArgs.event_data will contain the Event object for the UNO event raised.
        DialogControlBase.__init__(self, ctl)
        generic_args = self._get_generic_args()
        # EventArgs.event_data will contain the ActionEvent
        SpinEvents.__init__(self, trigger_args=generic_args, cb=self._on_spin_events_listener_add_remove)
        TextEvents.__init__(self, trigger_args=generic_args, cb=self._on_text_events_listener_add_remove)

    # endregion init

    # region Lazy Listeners
    def _on_spin_events_listener_add_remove(self, source: Any, event: ListenerEventArgs) -> None:
        # will only ever fire once
        self.view.addSpinListener(self.events_listener_spin)
        event.remove_callback = True

    def _on_text_events_listener_add_remove(self, source: Any, event: ListenerEventArgs) -> None:
        # will only ever fire once
        self.view.addTextListener(self.events_listener_text)
        event.remove_callback = True

    # endregion Lazy Listeners

    # region Overrides

    def get_view_ctl(self) -> UnoControlNumericField:
        return cast("UnoControlNumericField", super().get_view_ctl())

    def get_uno_srv_name(self) -> str:
        """Returns ``com.sun.star.awt.UnoControlNumericField``"""
        return "com.sun.star.awt.UnoControlNumericField"

    def get_model(self) -> UnoControlNumericFieldModel:
        """Gets the Model for the control"""
        return cast("UnoControlNumericFieldModel", self.get_view_ctl().getModel())

    def get_control_kind(self) -> DialogControlKind:
        """Gets the control kind. Returns ``DialogControlKind.NUMERIC``"""
        return DialogControlKind.NUMERIC

    def get_control_named_kind(self) -> DialogControlNamedKind:
        """Gets the control named kind. Returns ``DialogControlNamedKind.NUMERIC``"""
        return DialogControlNamedKind.NUMERIC

    # endregion Overrides

    # region Properties
    @property
    def view(self) -> UnoControlNumericField:
        return self.get_view_ctl()

    @property
    def model(self) -> UnoControlNumericFieldModel:
        return self.get_model()

    @property
    def value(self) -> float:
        """Gets/Sets the value"""
        return self.model.Value

    @value.setter
    def value(self, value: float) -> None:
        self.model.Value = value

    @property
    def read_only(self) -> bool:
        """Gets/Sets the read-only property"""
        with contextlib.suppress(Exception):
            return self.model.ReadOnly
        return False

    @read_only.setter
    def read_only(self, value: bool) -> None:
        """Sets the read-only property"""
        with contextlib.suppress(Exception):
            self.model.ReadOnly = value

    # endregion Properties


# ctl = CtlButton(None)