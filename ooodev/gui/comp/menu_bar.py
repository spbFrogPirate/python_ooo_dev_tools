from __future__ import annotations
from typing import Any, cast, TYPE_CHECKING, Callable
import uno
from com.sun.star.awt import XMenuBar

from ooodev.events.args.generic_args import GenericArgs
from ooodev.adapter._helper.builder import builder_helper
from ooodev.adapter.component_prop import ComponentProp
from ooodev.utils.builder.default_builder import DefaultBuilder
from ooodev.events.args.event_args import EventArgs
from ooodev.adapter.awt.menu_bar_partial import MenuBarPartial
from ooodev.adapter.awt.menu_events import MenuEvents
from ooodev.adapter.lang.service_info_partial import ServiceInfoPartial
from ooodev.adapter.awt.popup_menu_comp import PopupMenuComp

if TYPE_CHECKING:
    from com.sun.star.awt import MenuBar as UnoMenuBar
    from ooodev.loader.inst.lo_inst import LoInst


class _MenuBar(ComponentProp):

    NODE = "private:resource/menubar/menubar"

    def __init__(self, component: Any) -> None:
        super().__init__(component)
        self._index = -1

    # region Dunder Methods
    def __getitem__(self, index: int) -> int:
        self = cast(MenuBarPartial, self)
        return self.get_item_id(index)

    def __iter__(self) -> _MenuBar:
        self._index = 0
        return self

    def __next__(self) -> int:
        self = cast(Any, self)
        if self._index >= self.get_item_count():
            self._index = -1
            raise StopIteration
        item_id = self.get_item_id(self._index)
        self._index += 1
        return item_id

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ComponentProp):
            return False
        if self is other:
            return True
        if self.component is other.component:
            return True
        return self.component == other.component

    # endregion Dunder Methods

    # region MenuPartial Overrides
    def get_popup_menu(self, item_id: int) -> PopupMenuComp | None:
        """
        Gets the popup menu from the menu item.
        """
        menu = self.component.getPopupMenu(item_id)
        if menu is None:
            return None
        return PopupMenuComp(menu)

    # endregion MenuPartial Overrides

    # region Add/Remove Events
    def subscribe_all_item_activated(self, cb: Callable[[Any, EventArgs, PopupMenuComp], None]) -> None:
        """
        Adds a callbacks for the item activated event for all menu and submenus items.

        Args:
            cb (Callable[[Any, EventArgs, PopupMenuComp], None]): Callback function.
        """

        for i in self:
            pop_out = self.get_popup_menu(i)
            if pop_out is not None:
                pop_out.subscribe_all_item_activated(cb)

    def subscribe_all_item_deactivated(self, cb: Callable[[Any, EventArgs, PopupMenuComp], None]) -> None:
        """
        Adds a callbacks for the item deactivated event for all menu and submenus items.

        Args:
            cb (Callable[[Any, EventArgs, PopupMenuComp], None]): Callback function.
        """

        for i in self:
            pop_out = self.get_popup_menu(i)
            if pop_out is not None:
                pop_out.subscribe_all_item_deactivated(cb)

    def subscribe_all_item_highlighted(self, cb: Callable[[Any, EventArgs, PopupMenuComp], None]) -> None:
        """
        Adds a callbacks for the item highlighted event for all menu and submenus items.

        Args:
            cb (Callable[[Any, EventArgs, PopupMenuComp], None]): Callback function.
        """
        for i in self:
            pop_out = self.get_popup_menu(i)
            if pop_out is not None:
                pop_out.subscribe_all_item_highlighted(cb)

    def subscribe_all_item_selected(self, cb: Callable[[Any, EventArgs, PopupMenuComp], None]) -> None:
        """
        Adds a callbacks for the item selected event for all menu and submenus items.

        Args:
            cb (Callable[[Any, EventArgs, PopupMenuComp], None]): Callback function.
        """

        for i in self:
            pop_out = self.get_popup_menu(i)
            if pop_out is not None:
                pop_out.subscribe_all_item_selected(cb)

    def unsubscribe_all_item_activated(self, cb: Callable[[Any, EventArgs, PopupMenuComp], None]) -> None:
        """
        Remove callbacks for the item selected event for all menu and submenus items.

        Args:
            cb (Callable[[Any, EventArgs, PopupMenuComp], None]): Callback function.
        """

        for i in self:
            pop_out = self.get_popup_menu(i)
            if pop_out is not None:
                pop_out.unsubscribe_all_item_activated(cb)

    def unsubscribe_all_item_deactivated(self, cb: Callable[[Any, EventArgs, PopupMenuComp], None]) -> None:
        """
        Remove callbacks for the item deactivated event for all menu and submenus items.

        Args:
            cb (Callable[[Any, EventArgs, PopupMenuComp], None]): Callback function.
        """

        for i in self:
            pop_out = self.get_popup_menu(i)
            if pop_out is not None:
                pop_out.unsubscribe_all_item_deactivated(cb)

    def unsubscribe_all_item_highlighted(self, cb: Callable[[Any, EventArgs, PopupMenuComp], None]) -> None:
        """
        Remove callbacks for the item highlighted event for all menu and submenus items.

        Args:
            cb (Callable[[Any, EventArgs, PopupMenuComp], None]): Callback function.
        """

        for i in self:
            pop_out = self.get_popup_menu(i)
            if pop_out is not None:
                pop_out.unsubscribe_all_item_highlighted(cb)

    def unsubscribe_all_item_selected(self, cb: Callable[[Any, EventArgs, PopupMenuComp], None]) -> None:
        """
        Remove callbacks for the item selected event for all menu and submenus items.

        Args:
            cb (Callable[[Any, EventArgs, PopupMenuComp], None]): Callback function.
        """

        for i in self:
            pop_out = self.get_popup_menu(i)
            if pop_out is not None:
                pop_out.unsubscribe_all_item_selected(cb)

    # endregion Add/Remove Events

    # region Component Base Overrides
    def _ComponentBase__get_supported_service_names(self) -> tuple[str, ...]:
        """Returns a tuple of supported service names."""
        return ("com.sun.star.awt.MenuBar",)

    # endregion Component Base Overrides


class MenuBar(_MenuBar, MenuBarPartial, ServiceInfoPartial, MenuEvents):
    """
    Class for managing MenuBar Component.
    """

    # pylint: disable=unused-argument
    def __new__(cls, component: Any, *args, **kwargs):
        def on_event_init(src: Any, event: EventArgs):
            clz = event.event_data["data"]["class"]
            if clz is MenuEvents:
                event.event_data["triggers"] = {"menu_bar": event.event_data["data"]["instance"]}

        builder = get_builder(component=component)
        builder.subscribe_class_event_init(on_event_init)
        builder_helper.builder_add_comp_defaults(builder)

        builder_only = kwargs.get("_builder_only", False)
        if builder_only:
            # cast to prevent type checker error
            return cast(Any, builder)

        inst = builder.build_class(
            name="ooodev.gui.comp.menu_bar.MenuBar",
            base_class=_MenuBar,
        )
        return inst

    def __init__(self, component: XMenuBar) -> None:
        """
        Constructor

        Args:
            component (UnoControlDialog): UNO Component that supports `com.sun.star.awt.MenuBar`` service.
        """
        # this it not actually called as __new__ is overridden
        pass

    # region Overrides
    def _ComponentBase__get_supported_service_names(self) -> tuple[str, ...]:
        """Returns a tuple of supported service names."""
        return ("com.sun.star.awt.MenuBar",)

    # endregion Overrides

    @classmethod
    def from_lo(cls, lo_inst: LoInst | None = None) -> _MenuBar:
        """
        Creates a new  instance from Lo.

        Args:
            lo_inst (LoInst, optional): LoInst, Defaults to ``Lo.current_lo``.

        Returns:
            MenuBarComp: The instance.
        """
        # pylint: disable=import-outside-toplevel
        from ooodev.loader import lo as mLo

        if lo_inst is None:
            lo_inst = mLo.Lo.current_lo
        inst = lo_inst.create_instance_mcf(XMenuBar, "com.sun.star.awt.MenuBar", raise_err=True)  # type: ignore
        return cls(inst)

    # region Properties

    @property
    def component(self) -> UnoMenuBar:
        """MenuBar Component"""
        # pylint: disable=no-member
        return cast("UnoMenuBar", self._ComponentBase__get_component())  # type: ignore

    # endregion Properties


def get_builder(component: Any) -> DefaultBuilder:
    """
    Get the builder for the component.

    Args:
        component (Any): The component.

    Returns:
        DefaultBuilder: Builder instance.
    """
    builder = DefaultBuilder(component)
    builder.auto_interface()
    builder.set_omit("ooodev.adapter.awt.menu_partial.MenuPartial")
    builder.add_event(
        module_name="ooodev.adapter.awt.menu_events",
        class_name="MenuEvents",
        uno_name="com.sun.star.awt.XMenuBar",
        optional=True,
    )
    return builder
