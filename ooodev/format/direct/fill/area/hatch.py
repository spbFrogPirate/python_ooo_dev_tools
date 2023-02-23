"""
Module for Fill Properties Fill Hatch.

.. versionadded:: 0.9.0
"""
from __future__ import annotations
from typing import Any, Tuple, cast, overload, Type, TypeVar

import uno
from ooo.dyn.drawing.fill_style import FillStyle
from ooo.dyn.drawing.hatch_style import HatchStyle as HatchStyle
from ooo.dyn.drawing.hatch import Hatch as UnoHatch

from .....events.args.key_val_cancel_args import KeyValCancelArgs
from .....events.format_named_event import FormatNamedEvent
from .....exceptions import ex as mEx
from .....utils import lo as mLo
from .....utils import props as mProps
from .....utils.color import Color
from .....utils.color import StandardColor
from .....utils.data_type.angle import Angle as Angle
from .....utils.unit_convert import UnitConvert
from ....kind.format_kind import FormatKind
from ....preset import preset_hatch as mPreset
from ....preset.preset_hatch import PresetHatchKind as PresetHatchKind
from ....style_base import StyleMulti
from ...structs.hatch_struct import HatchStruct
from .fill_color import FillColor
from ...common.props.area_hatch_props import AreaHatchProps
from ...common.props.fill_color_props import FillColorProps
from .....events.format_named_event import FormatNamedEvent as FormatNamedEvent


_THatch = TypeVar(name="_THatch", bound="Hatch")


class Hatch(StyleMulti):
    """
    Class for Fill Properties Fill Hatch.

    .. versionadded:: 0.9.0
    """

    def __init__(
        self,
        *,
        style: HatchStyle = HatchStyle.SINGLE,
        color: Color = Color(0),
        space: float = 0.0,
        angle: Angle | int = 0,
        bg_color: Color = Color(-1),
    ) -> None:
        """
        Constructor

        Args:
            style (HatchStyle, optional): Specifies the kind of lines used to draw this hatch. Default ``HatchStyle.SINGLE``.
            color (Color, optional): Specifies the color of the hatch lines. Default ``0``.
            space (int, optional): Specifies the space between the lines in the hatch (in ``mm`` units). Default ``0.0``
            angle (Angle, int, optional): Specifies angle of the hatch in degrees. Default to ``0``.
            bg_color(Color, optionl): Specifies the background Color. Set this ``-1`` (default) for no background color.

        Returns:
            None:
        """

        hatch = HatchStruct(
            style=style,
            color=color,
            distance=space,
            angle=angle,
            _cattribs=self._get_hatch_cattribs(),
        )
        hatch._prop_parent = self
        # hatch._struct_property_name = self._props.hatch_prop

        # create event just to listen to fill color init
        bk_color = FillColor(color=bg_color, _cattribs=self._get_fill_color_cattribs())
        bk_color._prop_parent = self
        # FillStyle is set by this class
        bk_color._remove(self._props.style)
        # add event listener to prevent FillStyle from being set
        bk_color.add_event_listener(FormatNamedEvent.STYLE_SETTING, _on_bg_color_setting)
        bk_color.prop_color = bg_color

        init_vals = {}
        init_vals[self._props.style] = FillStyle.HATCH
        if bg_color < 0:
            init_vals[self._props.bg] = False
        else:
            init_vals[self._props.bg] = True
        self._bg_color = bg_color

        super().__init__(**init_vals)
        self._set_style("fill_color", bk_color, *bk_color.get_attrs())
        self._set_style("fill_hatch", hatch, *hatch.get_attrs())

    # region Overrides

    def _supported_services(self) -> Tuple[str, ...]:
        try:
            return self._supported_services_values
        except AttributeError:
            self._supported_services_values = (
                "com.sun.star.drawing.FillProperties",
                "com.sun.star.text.TextContent",
                "com.sun.star.beans.PropertySet",
                "com.sun.star.style.PageStyle",
            )
        return self._supported_services_values

    def _container_get_service_name(self) -> str:
        # https://github.com/LibreOffice/core/blob/d9e044f04ac11b76b9a3dac575f4e9155b67490e/chart2/source/tools/PropertyHelper.cxx#L229
        return "com.sun.star.drawing.HatchTable"

    # region apply()
    @overload
    def apply(self, obj: object) -> None:
        ...

    def apply(self, obj: object, **kwargs) -> None:
        """
        Applies styles to object

        Args:
            obj (object): UNO object that has supports ``com.sun.star.style.FillProperties`` or ``com.sun.star.beans.PropertySet`` service.

        Returns:
            None:
        """
        super().apply(obj, **kwargs)

    def _props_set(self, obj: object, **kwargs: Any) -> None:
        try:
            super()._props_set(obj, **kwargs)
        except mEx.MultiError as e:
            mLo.Lo.print(f"Hatch.apply(): Unable to set Property")
            for err in e.errors:
                mLo.Lo.print(f"  {err}")

    # endregion apply()

    # endregion Overrides

    # region Internal Methods
    def _get_hatch_cattribs(self) -> dict:
        return {
            "_supported_services_values": self._supported_services(),
            "_format_kind_prop": self.prop_format_kind,
            "_property_name": self._props.hatch_prop,
        }

    def _get_fill_color_cattribs(self) -> dict:
        return {
            "_supported_services_values": self._supported_services(),
            "_format_kind_prop": self.prop_format_kind,
            "_props_internal_attributes": FillColorProps(
                color=self._props.color, style=self._props.style, bg=self._props.bg
            ),
        }

    def copy(self: _THatch) -> _THatch:
        cp = super().copy()
        cp._bg_color = self._bg_color
        return cp

    # endregion Internal Methods

    # region Static Methods
    # region from_preset()
    @overload
    @classmethod
    def from_preset(cls: Type[_THatch], preset: PresetHatchKind) -> _THatch:
        ...

    @overload
    @classmethod
    def from_preset(cls: Type[_THatch], preset: PresetHatchKind, **kwargs) -> _THatch:
        ...

    @classmethod
    def from_preset(cls: Type[_THatch], preset: PresetHatchKind, **kwargs) -> _THatch:
        """
        Gets an instance from a preset.

        Args:
            preset (PresetHatchKind): Preset.

        Returns:
            Hatch: Instance from preset.
        """
        kargs = mPreset.get_preset(preset)
        kargs.update(kwargs)
        return cls(**kargs)

    # endregion from_preset()

    # region from_obj()
    @overload
    @classmethod
    def from_obj(cls: Type[_THatch], obj: object) -> _THatch:
        ...

    @overload
    @classmethod
    def from_obj(cls: Type[_THatch], obj: object, **kwargs) -> _THatch:
        ...

    @classmethod
    def from_obj(cls: Type[_THatch], obj: object, **kwargs) -> _THatch:
        """
        Gets instance from object

        Args:
            obj (object): UNO object.

        Raises:
            NotSupportedError: If ``obj`` is not supported.

        Returns:
            Hatch: ``Hatch`` instance that represents ``obj`` hatch pattern.
        """
        nu = cls(**kwargs)
        if not nu._is_valid_obj(obj):
            raise mEx.NotSupportedError("Object is not support to convert to Hatch")

        hatch = cast(UnoHatch, mProps.Props.get(obj, nu._props.hatch_prop))
        fc = FillColor.from_obj(obj, _cattribs=nu._get_fill_color_cattribs())

        if hatch.Angle > 0:
            angle = round(hatch.Angle / 10)
        else:
            angle = 0
        return cls(
            style=hatch.Style,
            color=hatch.Color,
            space=UnitConvert.convert_mm100_mm(hatch.Distance),
            angle=angle,
            bg_color=fc.prop_color,
            **kwargs,
        )

    # endregion from_obj()
    # endregion Static Methods

    # region Properties
    @property
    def prop_format_kind(self) -> FormatKind:
        """Gets the kind of style"""
        try:
            return self._format_kind_prop
        except AttributeError:
            self._format_kind_prop = FormatKind.TXT_CONTENT | FormatKind.FILL
        return self._format_kind_prop

    @property
    def prop_bg_color(self) -> Color:
        """Gets sets if fill image is tiled"""
        return self.prop_inner_color.prop_color

    @prop_bg_color.setter
    def prop_bg_color(self, value: Color):
        self.prop_inner_color.prop_color = value
        if value < 0:
            self._set(self._props.bg, False)
        else:
            self._set(self._props.bg, True)

    @property
    def prop_style(self) -> HatchStyle:
        """Gets/Sets the style of the hatch."""
        return self.prop_inner_hatch.prop_style

    @prop_style.setter
    def prop_style(self, value: HatchStyle):
        self.prop_inner_hatch.prop_style = value

    @property
    def prop_bg_color(self) -> Color:
        """Gets the back ground color passed in to constructor."""
        return Color(self._bg_color)

    @property
    def prop_color(self) -> Color:
        """Gets/Sets the color of the hatch lines."""
        return self.prop_inner_hatch.prop_color

    @prop_color.setter
    def prop_color(self, value: Color):
        self.prop_inner_hatch.prop_color = value

    @property
    def prop_distance(self) -> float:
        """Gets/Sets the distance between the lines in the hatch (in ``mm`` units)."""
        return self.prop_inner_hatch.prop_distance

    @prop_distance.setter
    def prop_distance(self, value: float):
        self.prop_inner_hatch.prop_distance = value

    @property
    def prop_angle(self) -> Angle:
        """Gets/Sets angle of the hatch."""
        return self.prop_inner_hatch.prop_angle

    @prop_angle.setter
    def prop_angle(self, value: Angle | int):
        self.prop_inner_hatch.prop_angle = value

    @property
    def prop_inner_color(self) -> FillColor:
        """Gets/Sets Fill Color instance"""
        try:
            return self._direct_inner_color
        except AttributeError:
            self._direct_inner_color = cast(FillColor, self._get_style_inst("fill_color"))
        return self._direct_inner_color

    @prop_inner_color.setter
    def prop_inner_color(self, value: FillColor) -> None:
        bk_color = FillColor(color=value.prop_color, _cattribs=self._get_fill_color_cattribs())
        bk_color._prop_parent = self
        # FillStyle is set by this class
        bk_color._remove(self._props.style)
        # add event listener to prevent FillStyle from being set
        bk_color.add_event_listener(FormatNamedEvent.STYLE_SETTING, _on_bg_color_setting)
        bk_color.prop_color = value.prop_color

        if bk_color.prop_color < 0:
            self._set(self._props.bg, False)
        else:
            self._set(self._props.bg, True)
        self._del_attribs("_direct_inner_color")
        self._set_style("fill_color", bk_color, *bk_color.get_attrs())

    @property
    def prop_inner_hatch(self) -> HatchStruct:
        """Gets/Sets Hatch Struct instance"""
        try:
            return self._direct_inner_hatch
        except AttributeError:
            self._direct_inner_hatch = cast(HatchStruct, self._get_style_inst("fill_hatch"))
        return self._direct_inner_hatch

    @prop_inner_hatch.setter
    def prop_inner_hatch(self, value: HatchStruct) -> None:
        hatch = HatchStruct.from_hatch(value=value.get_uno_struct(), _cattribs=self._get_hatch_cattribs())
        self._del_attribs("_direct_inner_hatch")
        self._set_style("fill_hatch", hatch, *hatch.get_attrs())

    @property
    def _props(self) -> AreaHatchProps:
        try:
            return self._props_internal_attributes
        except AttributeError:
            self._props_internal_attributes = AreaHatchProps(
                color="FillColor", style="FillStyle", bg="FillBackground", hatch_prop="FillHatch"
            )
        return self._props_internal_attributes

    # endregion Properties


def _on_bg_color_setting(source: Any, event_args: KeyValCancelArgs, *args, **kwargs) -> None:
    fc = cast(FillColor, event_args.event_source)
    hatch = cast(_THatch, fc.prop_parent)
    if event_args.key == hatch._props.style:
        event_args.cancel = True
    elif event_args.key == hatch._props.color:
        # -1 means automatic color.
        # Fillcolor for hatch has not automatic color
        if event_args.value == -1:
            # strickly speaking this is not needed but follows how Draw handles it.
            event_args.value = StandardColor.DEFAULT_BLUE
