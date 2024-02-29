from __future__ import annotations
from typing import Any, cast, TYPE_CHECKING
import uno
from ooo.dyn.table.table_border import TableBorder
from ooo.dyn.table.border_line import BorderLine

from ooodev.adapter.component_base import ComponentBase
from ooodev.events.events import Events
from ooodev.events.args.key_val_cancel_args import KeyValCancelArgs
from ooodev.events.args.key_val_args import KeyValArgs
from ooodev.adapter.table.border_line_comp import BorderLineComp
from ooodev.utils import info as mInfo

if TYPE_CHECKING:
    from ooodev.events.events_t import EventsT

# It seems that it is necessary to assign the struct to a variable, then change the variable and assign it back to the component.
# It is as if LibreOffice creates a new instance of the struct when it is changed.


class TableBorderComp(ComponentBase):
    """
    Table Border Struct

    This class raises an event before and after a property is changed if it has been passed an event provider.

    The event raised before the property is changed is called ``com_sun_star_table_TableBorder_changing``.
    The event raised after the property is changed is called ``com_sun_star_table_TableBorder_changed``.

    The event args for before the property is changed is of type ``KeyValCancelArgs``.
    The event args for after the property is changed is of type ``KeyValArgs``.
    """

    def __init__(self, component: TableBorder, prop_name: str, event_provider: EventsT | None) -> None:
        """
        Constructor

        Args:
            component (TableBorder): Table Border.
            prop_name (str): Property Name. This value is assigned to the ``prop_name`` of ``event_data``.
            event_provider (EventsT | None): Event Provider.
        """
        ComponentBase.__init__(self, component)
        self._event_provider = event_provider
        self._prop_name = prop_name
        self._props = {}
        self._events = Events(source=self)

        # pylint: disable=unused-argument

        def on_border_line_changed(src: Any, event_args: KeyValArgs) -> None:
            prop_name = str(event_args.event_data["prop_name"])
            if hasattr(self, prop_name):
                setattr(self, prop_name, event_args.source.component)

        self.__fn_on_border_line_changed = on_border_line_changed
        self._events.subscribe_event("com_sun_star_table_BorderLine_changed", self.__fn_on_border_line_changed)

    # region Overrides
    def _ComponentBase__get_supported_service_names(self) -> tuple[str, ...]:
        """Returns a tuple of supported service names."""
        # PropertySetPartial will validate
        return ()

    # endregion Overrides

    def _get_on_changed_event_name(self) -> str:
        return "com_sun_star_table_TableBorder_changed"

    def _get_on_changing_event_name(self) -> str:
        return "com_sun_star_table_TableBorder_changing"

    def _get_prop_name(self) -> str:
        return self._prop_name

    def _on_property_changing(self, event_args: KeyValCancelArgs) -> None:
        if self._event_provider is not None:
            self._event_provider.trigger_event(self._get_on_changing_event_name(), event_args)

    def _on_property_changed(self, event_args: KeyValArgs) -> None:
        if self._event_provider is not None:
            self._event_provider.trigger_event(self._get_on_changed_event_name(), event_args)

    def _copy(self, src: TableBorder | None = None) -> TableBorder:
        if src is None:
            src = self.component

        def copy_bdr(src: BorderLine) -> BorderLine:
            return BorderLine(
                Color=src.Color,
                InnerLineWidth=src.InnerLineWidth,
                OuterLineWidth=src.OuterLineWidth,
                LineDistance=src.LineDistance,
            )

        return TableBorder(
            TopLine=copy_bdr(src.TopLine),
            IsTopLineValid=src.IsTopLineValid,
            BottomLine=copy_bdr(src.BottomLine),
            IsBottomLineValid=src.IsBottomLineValid,
            LeftLine=copy_bdr(src.LeftLine),
            IsLeftLineValid=src.IsLeftLineValid,
            RightLine=copy_bdr(src.RightLine),
            IsRightLineValid=src.IsRightLineValid,
            HorizontalLine=copy_bdr(src.HorizontalLine),
            IsHorizontalLineValid=src.IsHorizontalLineValid,
            VerticalLine=copy_bdr(src.VerticalLine),
            IsVerticalLineValid=src.IsVerticalLineValid,
            Distance=src.Distance,
            IsDistanceValid=src.IsDistanceValid,
        )

    def copy(self) -> TableBorder:
        """
        Makes a copy of the Table Border.

        Returns:
            TableBorder: Copied Table Border.
        """
        return self._copy()

    # region Properties

    @property
    def component(self) -> TableBorder:
        """TableBorder Component"""
        # pylint: disable=no-member
        return cast("TableBorder", self._ComponentBase__get_component())  # type: ignore

    @component.setter
    def component(self, value: TableBorder) -> None:
        # pylint: disable=no-member
        self._ComponentBase__set_component(self._copy(src=value))  # type: ignore

    @property
    def top_line(self) -> BorderLineComp:
        """
        Gets/Set the line style at the top edge.

        Setting value can be done with a ``BorderLine`` or ``BorderLineComp`` object.

        Returns:
            BorderLineComp: Returns Border Line.

        Hint:
            - ``BorderLine`` can be imported from ``ooo.dyn.table.border_line``
        """
        key = "top_line"
        prop = self._props.get(key, None)
        if prop is None:
            prop = BorderLineComp(self.component.TopLine, key, self._events)
            self._props[key] = prop
        return cast(BorderLineComp, prop)

    @top_line.setter
    def top_line(self, value: BorderLineComp | BorderLine) -> None:
        key = "top_line"
        old_value = self.component.TopLine
        if mInfo.Info.is_instance(value, BorderLineComp):
            new_value = value.copy()
        else:
            comp = BorderLineComp(cast(BorderLine, value), key)
            new_value = comp.copy()

        event_args = KeyValCancelArgs(
            source=self,
            key=key,
            value=new_value,
        )
        event_args.event_data = {
            "old_value": old_value,
            "prop_name": self._get_prop_name(),
        }
        self._on_property_changing(event_args)
        if event_args.cancel:
            return
        struct = self._copy()
        struct.TopLine = event_args.value
        self.component = struct
        self._props[key] = BorderLineComp(self.component.TopLine, key, self._events)
        self._on_property_changed(KeyValArgs.from_args(event_args))  # type: ignore

    @property
    def is_top_line_valid(self) -> bool:
        """
        Gets/Sets whether the value of ``TableBorder.TopLine`` is used.
        """
        return self.component.IsTopLineValid

    @is_top_line_valid.setter
    def is_top_line_valid(self, value: bool) -> None:
        old_value = self.component.IsTopLineValid
        if old_value != value:
            event_args = KeyValCancelArgs(
                source=self,
                key="is_top_line_valid",
                value=value,
            )
            event_args.event_data = {
                "old_value": old_value,
                "prop_name": self._get_prop_name(),
            }
            self._on_property_changing(event_args)
            if not event_args.cancel:
                struct = self._copy()
                struct.IsTopLineValid = event_args.value
                self.component = struct
                self._on_property_changed(KeyValArgs.from_args(event_args))  # type: ignore

    @property
    def bottom_line(self) -> BorderLineComp:
        """
        Gets/Set the line style at the bottom edge.

        Setting value can be done with a ``BorderLine`` or ``BorderLineComp`` object.

        Returns:
            BorderLineComp: Returns Border Line.

        Hint:
            - ``BorderLine`` can be imported from ``ooo.dyn.table.border_line``
        """
        key = "bottom_line"
        prop = self._props.get(key, None)
        if prop is None:
            prop = BorderLineComp(self.component.BottomLine, key, self._events)
            self._props[key] = prop
        return cast(BorderLineComp, prop)

    @bottom_line.setter
    def bottom_line(self, value: BorderLineComp | BorderLine) -> None:
        key = "bottom_line"
        old_value = self.component.BottomLine
        if mInfo.Info.is_instance(value, BorderLineComp):
            new_value = value.copy()
        else:
            comp = BorderLineComp(cast(BorderLine, value), key)
            new_value = comp.copy()

        event_args = KeyValCancelArgs(
            source=self,
            key=key,
            value=new_value,
        )
        event_args.event_data = {
            "old_value": old_value,
            "prop_name": self._get_prop_name(),
        }
        self._on_property_changing(event_args)
        if event_args.cancel:
            return
        struct = self._copy()
        struct.BottomLine = event_args.value
        self.component = struct
        self._props[key] = BorderLineComp(self.component.BottomLine, key, self._events)
        self._on_property_changed(KeyValArgs.from_args(event_args))  # type: ignore

    @property
    def is_bottom_line_valid(self) -> bool:
        """
        Gets/Sets whether the value of ``TableBorder.BottomLine`` is used.
        """
        return self.component.IsBottomLineValid

    @is_bottom_line_valid.setter
    def is_bottom_line_valid(self, value: bool) -> None:
        old_value = self.component.IsBottomLineValid
        if old_value != value:
            event_args = KeyValCancelArgs(
                source=self,
                key="is_bottom_line_valid",
                value=value,
            )
            event_args.event_data = {
                "old_value": old_value,
                "prop_name": self._get_prop_name(),
            }
            self._on_property_changing(event_args)
            if not event_args.cancel:
                struct = self._copy()
                struct.IsBottomLineValid = event_args.value
                self.component = struct
                self._on_property_changed(KeyValArgs.from_args(event_args))  # type: ignore

    @property
    def left_line(self) -> BorderLineComp:
        """
        Gets/Set the line style at the left edge.

        Setting value can be done with a ``BorderLine`` or ``BorderLineComp`` object.

        Returns:
            BorderLineComp: Returns Border Line.

        Hint:
            - ``BorderLine`` can be imported from ``ooo.dyn.table.border_line``
        """
        key = "left_line"
        prop = self._props.get(key, None)
        if prop is None:
            prop = BorderLineComp(self.component.LeftLine, key, self._events)
            self._props[key] = prop
        return cast(BorderLineComp, prop)

    @left_line.setter
    def left_line(self, value: BorderLineComp | BorderLine) -> None:
        key = "left_line"
        old_value = self.component.LeftLine
        if mInfo.Info.is_instance(value, BorderLineComp):
            new_value = value.copy()
        else:
            comp = BorderLineComp(cast(BorderLine, value), key)
            new_value = comp.copy()

        event_args = KeyValCancelArgs(
            source=self,
            key=key,
            value=new_value,
        )
        event_args.event_data = {
            "old_value": old_value,
            "prop_name": self._get_prop_name(),
        }
        self._on_property_changing(event_args)
        if event_args.cancel:
            return
        struct = self._copy()
        struct.LeftLine = event_args.value
        self.component = struct
        self._props[key] = BorderLineComp(self.component.LeftLine, key, self._events)
        self._on_property_changed(KeyValArgs.from_args(event_args))  # type: ignore

    @property
    def is_left_line_valid(self) -> bool:
        """
        Gets/Sets whether the value of ``TableBorder.LeftLine`` is used.
        """
        return self.component.IsLeftLineValid

    @is_left_line_valid.setter
    def is_left_line_valid(self, value: bool) -> None:
        old_value = self.component.IsLeftLineValid
        if old_value != value:
            event_args = KeyValCancelArgs(
                source=self,
                key="is_left_line_valid",
                value=value,
            )
            event_args.event_data = {
                "old_value": old_value,
                "prop_name": self._get_prop_name(),
            }
            self._on_property_changing(event_args)
            if not event_args.cancel:
                struct = self._copy()
                struct.IsLeftLineValid = event_args.value
                self.component = struct
                self._on_property_changed(KeyValArgs.from_args(event_args))  # type: ignore

    @property
    def right_line(self) -> BorderLineComp:
        """
        Gets/Set the line style at the right edge.

        Setting value can be done with a ``BorderLine`` or ``BorderLineComp`` object.

        Returns:
            BorderLineComp: Returns Border Line.

        Hint:
            - ``BorderLine`` can be imported from ``ooo.dyn.table.border_line``
        """
        key = "right_line"
        prop = self._props.get(key, None)
        if prop is None:
            prop = BorderLineComp(self.component.RightLine, key, self._events)
            self._props[key] = prop
        return cast(BorderLineComp, prop)

    @right_line.setter
    def right_line(self, value: BorderLineComp | BorderLine) -> None:
        key = "right_line"
        old_value = self.component.RightLine
        if mInfo.Info.is_instance(value, BorderLineComp):
            new_value = value.copy()
        else:
            comp = BorderLineComp(cast(BorderLine, value), key)
            new_value = comp.copy()

        event_args = KeyValCancelArgs(
            source=self,
            key=key,
            value=new_value,
        )
        event_args.event_data = {
            "old_value": old_value,
            "prop_name": self._get_prop_name(),
        }
        self._on_property_changing(event_args)
        if event_args.cancel:
            return
        struct = self._copy()
        struct.RightLine = event_args.value
        self.component = struct
        self._props[key] = BorderLineComp(self.component.RightLine, key, self._events)
        self._on_property_changed(KeyValArgs.from_args(event_args))  # type: ignore

    @property
    def is_right_line_valid(self) -> bool:
        """
        Gets/Sets whether the value of ``TableBorder.RightLine`` is used.
        """
        return self.component.IsRightLineValid

    @is_right_line_valid.setter
    def is_right_line_valid(self, value: bool) -> None:
        old_value = self.component.IsRightLineValid
        if old_value != value:
            event_args = KeyValCancelArgs(
                source=self,
                key="is_right_line_valid",
                value=value,
            )
            event_args.event_data = {
                "old_value": old_value,
                "prop_name": self._get_prop_name(),
            }
            self._on_property_changing(event_args)
            if not event_args.cancel:
                struct = self._copy()
                struct.IsRightLineValid = event_args.value
                self.component = struct
                self._on_property_changed(KeyValArgs.from_args(event_args))  # type: ignore

    @property
    def horizontal_line(self) -> BorderLineComp:
        """
        Gets/Set the horizontal line style edge.

        Setting value can be done with a ``BorderLine`` or ``BorderLineComp`` object.

        Returns:
            BorderLineComp: Returns Border Line.

        Hint:
            - ``BorderLine`` can be imported from ``ooo.dyn.table.border_line``
        """
        key = "horizontal_line"
        prop = self._props.get(key, None)
        if prop is None:
            prop = BorderLineComp(self.component.HorizontalLine, key, self._events)
            self._props[key] = prop
        return cast(BorderLineComp, prop)

    @horizontal_line.setter
    def horizontal_line(self, value: BorderLineComp | BorderLine) -> None:
        key = "horizontal_line"
        old_value = self.component.HorizontalLine
        if mInfo.Info.is_instance(value, BorderLineComp):
            new_value = value.copy()
        else:
            comp = BorderLineComp(cast(BorderLine, value), key)
            new_value = comp.copy()

        event_args = KeyValCancelArgs(
            source=self,
            key=key,
            value=new_value,
        )
        event_args.event_data = {
            "old_value": old_value,
            "prop_name": self._get_prop_name(),
        }
        self._on_property_changing(event_args)
        if event_args.cancel:
            return
        struct = self._copy()
        struct.HorizontalLine = event_args.value
        self.component = struct
        self._props[key] = BorderLineComp(self.component.HorizontalLine, key, self._events)
        self._on_property_changed(KeyValArgs.from_args(event_args))  # type: ignore

    @property
    def is_horizontal_line_valid(self) -> bool:
        """
        Gets/Sets whether the value of ``TableBorder.HorizontalLine`` is used.
        """
        return self.component.IsHorizontalLineValid

    @is_horizontal_line_valid.setter
    def is_horizontal_line_valid(self, value: bool) -> None:
        old_value = self.component.IsHorizontalLineValid
        if old_value != value:
            event_args = KeyValCancelArgs(
                source=self,
                key="is_horizontal_line_valid",
                value=value,
            )
            event_args.event_data = {
                "old_value": old_value,
                "prop_name": self._get_prop_name(),
            }
            self._on_property_changing(event_args)
            if not event_args.cancel:
                struct = self._copy()
                struct.IsHorizontalLineValid = event_args.value
                self.component = struct
                self._on_property_changed(KeyValArgs.from_args(event_args))  # type: ignore

    @property
    def vertical_line(self) -> BorderLineComp:
        """
        Gets/Set the vertical line style edge.

        Setting value can be done with a ``BorderLine`` or ``BorderLineComp`` object.

        Returns:
            BorderLineComp: Returns Border Line.

        Hint:
            - ``BorderLine`` can be imported from ``ooo.dyn.table.border_line``
        """
        key = "vertical_line"
        prop = self._props.get(key, None)
        if prop is None:
            prop = BorderLineComp(self.component.VerticalLine, key, self._events)
            self._props[key] = prop
        return cast(BorderLineComp, prop)

    @vertical_line.setter
    def vertical_line(self, value: BorderLineComp | BorderLine) -> None:
        key = "vertical_line"
        old_value = self.component.VerticalLine
        if mInfo.Info.is_instance(value, BorderLineComp):
            new_value = value.copy()
        else:
            comp = BorderLineComp(cast(BorderLine, value), key)
            new_value = comp.copy()

        event_args = KeyValCancelArgs(
            source=self,
            key=key,
            value=new_value,
        )
        event_args.event_data = {
            "old_value": old_value,
            "prop_name": self._get_prop_name(),
        }
        self._on_property_changing(event_args)
        if event_args.cancel:
            return
        struct = self._copy()
        struct.VerticalLine = event_args.value
        self.component = struct
        self._props[key] = BorderLineComp(self.component.VerticalLine, key, self._events)
        self._on_property_changed(KeyValArgs.from_args(event_args))  # type: ignore

    @property
    def is_vertical_line_valid(self) -> bool:
        """
        Gets/Sets whether the value of ``TableBorder.HorizontalLine`` is used.
        """
        return self.component.IsVerticalLineValid

    @is_vertical_line_valid.setter
    def is_vertical_line_valid(self, value: bool) -> None:
        old_value = self.component.IsVerticalLineValid
        if old_value != value:
            event_args = KeyValCancelArgs(
                source=self,
                key="is_vertical_line_valid",
                value=value,
            )
            event_args.event_data = {
                "old_value": old_value,
                "prop_name": self._get_prop_name(),
            }
            self._on_property_changing(event_args)
            if not event_args.cancel:
                struct = self._copy()
                struct.IsVerticalLineValid = event_args.value
                self.component = struct
                self._on_property_changed(KeyValArgs.from_args(event_args))  # type: ignore

    @property
    def distance(self) -> int:
        """
        Gets/Sets the distance between the lines and other contents.

        Returns:
            int: Distance value.
        """
        return self.component.Distance  # type: ignore

    @distance.setter
    def distance(self, value: int) -> None:
        old_value = self.component.Distance
        if old_value != value:
            event_args = KeyValCancelArgs(
                source=self,
                key="distance",
                value=value,
            )
            event_args.event_data = {
                "old_value": old_value,
                "prop_name": self._get_prop_name(),
            }
            self._on_property_changing(event_args)
            if not event_args.cancel:
                struct = self._copy()
                struct.Distance = event_args.value
                self.component = struct
                self._on_property_changed(KeyValArgs.from_args(event_args))  # type: ignore

    @property
    def is_distance_valid(self) -> bool:
        """
        Gets/Sets whether the value of ``TableBorder.Distance`` is used.
        """
        return self.component.IsVerticalLineValid

    @is_distance_valid.setter
    def is_distance_valid(self, value: bool) -> None:
        old_value = self.component.IsVerticalLineValid
        if old_value != value:
            event_args = KeyValCancelArgs(
                source=self,
                key="is_distance_valid",
                value=value,
            )
            event_args.event_data = {
                "old_value": old_value,
                "prop_name": self._get_prop_name(),
            }
            self._on_property_changing(event_args)
            if not event_args.cancel:
                struct = self._copy()
                struct.IsVerticalLineValid = event_args.value
                self.component = struct
                self._on_property_changed(KeyValArgs.from_args(event_args))  # type: ignore

    # endregion Properties
