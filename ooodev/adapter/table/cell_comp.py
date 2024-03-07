from __future__ import annotations
from typing import cast, TYPE_CHECKING
from ooodev.adapter.beans.property_change_implement import PropertyChangeImplement
from ooodev.adapter.beans.vetoable_change_implement import VetoableChangeImplement
from ooodev.adapter.table.cell_partial import CellPartial
from ooodev.adapter.component_base import ComponentBase


if TYPE_CHECKING:
    from com.sun.star.table import Cell  # service
    from com.sun.star.table import XCell


class CellComp(ComponentBase, CellPartial, PropertyChangeImplement, VetoableChangeImplement):
    """
    Class for managing table Cell Component.
    """

    # pylint: disable=unused-argument

    def __init__(self, component: XCell) -> None:
        """
        Constructor

        Args:
            component (XCell): UNO Component that implements ``com.sun.star.table.Cell`` service.
        """
        ComponentBase.__init__(self, component)
        CellPartial.__init__(self, component=component, interface=None)
        # pylint: disable=no-member
        generic_args = self._ComponentBase__get_generic_args()  # type: ignore
        PropertyChangeImplement.__init__(self, component=self.component, trigger_args=generic_args)
        VetoableChangeImplement.__init__(self, component=self.component, trigger_args=generic_args)

    # region Overrides
    def _ComponentBase__get_supported_service_names(self) -> tuple[str, ...]:
        """Returns a tuple of supported service names."""
        return ("com.sun.star.table.Cell",)

    # endregion Overrides
    # region Properties
    @property
    def component(self) -> Cell:
        """Cell Component"""
        # pylint: disable=no-member
        return cast("Cell", self._ComponentBase__get_component())  # type: ignore

    # endregion Properties
