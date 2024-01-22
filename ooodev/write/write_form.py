from __future__ import annotations
from typing import TYPE_CHECKING
import uno

from ooodev.adapter.form.component.data_form_comp import DataFormComp
from ooodev.form.partial.form_partial import FormPartial
from ooodev.utils import lo as mLo
from ooodev.utils.inst.lo.lo_inst import LoInst
from ooodev.utils.partial.qi_partial import QiPartial

if TYPE_CHECKING:
    from com.sun.star.form.component import Form
    from .write_forms import WriteForms


class WriteForm(DataFormComp, QiPartial, FormPartial):
    """Writer Form"""

    def __init__(self, owner: WriteForms, component: Form, lo_inst: LoInst | None = None) -> None:
        """
        Constructor

        Args:
            owner (WriteForms): Owner of this component.
            component (Form): UNO object that supports ``com.sun.star.form.component.DataForm`` service.
            lo_inst (LoInst, optional): Lo instance. Defaults to ``None``.
        """
        if lo_inst is None:
            self._lo_inst = mLo.Lo.current_lo
        else:
            self._lo_inst = lo_inst
        self._owner = owner
        DataFormComp.__init__(self, component)
        QiPartial.__init__(self, component=component, lo_inst=self._lo_inst)
        draw_page = owner.owner.component
        FormPartial.__init__(self, owner=self, draw_page=draw_page, component=component)  # type: ignore

    # region Properties
    @property
    def name(self) -> str:
        """
        Gets/Sets the name of the form.
        """
        return self.component.getName()

    @name.setter
    def name(self, value: str) -> None:
        self.component.setName(value)

    @property
    def owner(self) -> WriteForms:
        """Component Owner"""
        return self._owner

    # endregion Properties
