from __future__ import annotations
from typing import Any, Dict, TYPE_CHECKING
from ooodev.adapter.container.index_access_comp import IndexAccessComp
from ooodev.adapter.ui.the_module_ui_configuration_manager_supplier_comp import (
    TheModuleUIConfigurationManagerSupplierComp,
)
from ooodev.gui.menu.menu import Menu
from ooodev.gui.menu.menu_base import MenuBase
from ooodev.gui.menu.menu_debug import MenuDebug
from ooodev.loader import lo as mLo
from ooodev.loader.inst.service import Service
from ooodev.utils import props as mProps
from ooodev.utils.partial.lo_inst_props_partial import LoInstPropsPartial
from ooodev.utils.kind.menu_lookup_kind import MenuLookupKind


if TYPE_CHECKING:
    from ooodev.adapter.ui.ui_configuration_manager_comp import UIConfigurationManagerComp
    from ooodev.loader.inst.lo_inst import LoInst


class MenuApp(LoInstPropsPartial):
    """Class for manager menu by LibreOffice module"""

    NODE = "private:resource/menubar/menubar"
    MENUS = MenuLookupKind.get_dict()

    def __init__(self, app: str | Service, lo_inst: LoInst | None = None):
        """
        :param app: LibreOffice Module: calc, writer, draw, impress, math, main
        :type app: str
        """
        if lo_inst is None:
            lo_inst = mLo.Lo.current_lo
        LoInstPropsPartial.__init__(self, lo_inst)
        self._app = str(app)
        self._config = self._get_config()
        self._menus = self._config.get_settings(self.NODE, True)

    def _get_config(self) -> UIConfigurationManagerComp:
        supp = TheModuleUIConfigurationManagerSupplierComp.from_lo(lo_inst=self.lo_inst)
        return supp.get_ui_configuration_manager(self._app)

    def debug(self):
        """Debug menu"""
        MenuDebug()(self._menus)
        return

    def __contains__(self, name: str):
        """
        If exists name in menu.

        Args:
            name (str): Menu CommandURL.
        """
        exists = False
        for m in self._menus:
            menu = mProps.Props.data_to_dict(m)
            cmd = menu.get("CommandURL", "")
            if name == cmd:
                exists = True
                break
        return exists

    def __getitem__(self, index: int | str | MenuLookupKind):
        """
        Index access.

        Args:
            index (int, str, MenuLookupKind): Index or Menu name or MenuLookupKind or CommandURL.
                If index is a str then it can be a know menu name or a CommandURL.

        Returns:
            Menu: Menu instance.

        Hint:
            - ``MenuLookupKind`` is an enum and can be imported from ``ooodev.utils.kind.menu_lookup_kind``

        Note:
            Index can also be any object the returns a command URL when str() is called on it.
        """
        if isinstance(index, int):
            menu = mProps.Props.data_to_dict(self._menus[index])
        else:
            if isinstance(index, str):
                if index.lower() in self.MENUS:
                    key = self.MENUS[index.lower()]
                else:
                    # assume a command URL has been passed in
                    key = index
            else:
                # MenuLookupKind
                # By calling str() on the enum, we get the value of the enum.
                # This can also allow other custom enums to be used as lookup values in the future.
                key = str(index)
            for m in self._menus:
                menu = mProps.Props.data_to_dict(m)
                cmd = menu.get("CommandURL", "")
                if cmd == key:
                    break
        ia = menu["ItemDescriptorContainer"]
        if ia is None:
            ia_menu = None
        else:
            ia_menu = IndexAccessComp(ia)
        obj = Menu(
            config=self._config,
            menus=self._menus,
            app=self._app,
            menu=ia_menu,  # type: ignore
            lo_inst=self.lo_inst,
        )
        return obj

    def insert(self, menu: Dict[str, Any], after: int | str = "", save: bool = True):
        """
        Insert new menu.

        Args:
            menu (dict): New menu data
            after (int, str, optional): Insert in after menu (CommandURL). Defaults to "".
            save (bool, optional): For persistent save. Defaults to True.
        """
        mb = MenuBase(config=self._config, menus=self._menus, app=self._app, lo_inst=self.lo_inst)

        mb.insert(self._menus, menu, after)
        if save:
            self._config.component.store()  # type: ignore
        return

    def remove(self, menu: str) -> None:
        """
        Remove menu.

        Args:
            menu (str): Menu CommandURL
        """
        mb = MenuBase(config=self._config, menus=self._menus, app=self._app, lo_inst=self.lo_inst)
        mb.remove(self._menus, menu)
        return
