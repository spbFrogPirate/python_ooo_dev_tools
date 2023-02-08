from __future__ import annotations
from typing import Any, Tuple, overload, cast

import uno

from .....events.args.key_val_cancel_args import KeyValCancelArgs
from .....events.format_named_event import FormatNamedEvent
from .....exceptions import ex as mEx
from .....utils import lo as mLo
from .....utils import props as mProps
from .....utils.color import Color, StandardColor
from .....utils.data_type.angle import Angle as Angle
from .....utils.unit_convert import UnitConvert
from .....utils.type_var import T
from ....kind.format_kind import FormatKind
from ....preset import preset_hatch as mPreset
from ....preset.preset_hatch import PresetHatchKind as PresetHatchKind
from ....style_base import StyleMulti
from ...structs.hatch_struct import HatchStruct
from .color import Color as FillColor

from ooo.dyn.drawing.fill_style import FillStyle
from ooo.dyn.drawing.hatch_style import HatchStyle as HatchStyle
from ooo.dyn.drawing.hatch import Hatch as UnoHatch

PARA_BACK_COLOR_FLAGS = 0x7F000000


class Hatch(StyleMulti):
    """
    Class for Fill Properties Fill Hatch.

    .. versionadded:: 0.9.0
    """

    def __init__(
        self,
        style: HatchStyle = HatchStyle.SINGLE,
        color: Color = Color(0),
        space: float = 0.0,
        angle: Angle | int = 0,
        bg_color: Color = Color(-1),
        name: str = "",
        auto_name: bool = False,
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
        self._auto_name = auto_name
        self._name = name  # this may change in _set_fill_hatch()
        init_vals = {"ParaBackTransparent": False, "FillStyle": FillStyle.HATCH}

        bk_color = FillColor(bg_color)
        # FillStyle is set by this class
        bk_color._remove("FillStyle")
        # add event listener to prevent FillStyle from being set
        bk_color.add_event_listener(FormatNamedEvent.STYLE_SETTING, _on_bg_color_setting)
        bk_color.prop_color = bg_color

        if bg_color < 0:
            init_vals["FillBackground"] = False
        else:
            init_vals["FillBackground"] = True

        super().__init__(**init_vals)
        self._set_bg_color(color)
        in_hatch = HatchStruct(style=style, color=color, distance=space, angle=angle)
        self._set_fill_hatch(in_hatch, False)

        self._set_style("fill_color", bk_color, *bk_color.get_attrs())

    # region Internal Methods
    def _set_bg_color(self, color: int) -> None:
        # Writer stores ParaBackColor as flag values when there is no background color
        # When there is background color then ParaBackColor contains the actual color.
        # To find the flag value a known value was used.
        # In this case the Hatch Color is used as part of the flag.
        #
        # background colors
        # ParaBackColor HEX         Name
        # 2130706432    0x7f000000  "Black 0 Degrees"
        # 2130706432    0x7f000000  "Black 90 Degrees"
        # 2130706432    0x7f000000  "Black 180 Degrees Crossed"
        # 2133483673    0x7f2a6099  "Blue 45 Degrees"
        # 2133483673    0x7f2a6099  "Blue -45 Degrees"
        # 2133483673    0x7f2a6099  "Blue 45 Degrees Crossed"
        # 2147467008    0x7fffbf00  "Yellow 45 Degrees"
        # 2130749747    0x7f00a933  "Green 30 Degrees"
        # 2147418112    0x7fff0000  "Red 45 Degrees"
        #
        # BLACK_HATCH = 0x7F000000
        # flags = BLUE_HATCH & ~StandardColor.BLUE
        # print(hex(flags))
        # '0x7F000000'
        #
        # This is the flags value assigned to PARA_BACK_COLOR_FLAGS
        # see also:
        # https://github.com/LibreOffice/core/blob/1a79594a27f41ad369e7c387c51e00afb1352872/xmloff/source/text/txtprmap.cxx#L396
        # https://github.com/LibreOffice/core/blob/776ea34deefe7bdce2fb8a06e5c55ef27ec87ea7/xmloff/source/style/prstylei.cxx#L121
        # https://github.com/LibreOffice/core/blob/1a79594a27f41ad369e7c387c51e00afb1352872/include/xmloff/xmltypes.hxx

        fb = cast(bool, self._get("FillBackground"))
        if fb:
            para_bg_color = color
        else:
            para_bg_color = PARA_BACK_COLOR_FLAGS | color
        self._set("ParaBackColor", para_bg_color)

    def _set_fill_hatch(self, hatch_struct: HatchStruct, ignore_preset: bool) -> None:
        name_hatch = self._get_named_hatch_struct(hatch_struct, self._name, ignore_preset)
        self._set("FillHatchName", self._name)
        self._set_style("fill_hatch", name_hatch, *name_hatch.get_attrs())

    def _get_fill_color(self) -> FillColor:
        return self._get_style_inst("fill_color")

    def _get_hatch_struct(self) -> HatchStruct:
        return self._get_style_inst("fill_hatch")

    def _get_named_hatch_struct(self, hatch_struct: HatchStruct, name: str, ignore_preset: bool) -> HatchStruct:
        # if the name passed in already exist in the Hatch Table then it is returned.
        # Otherwise the hatch is added to the Hatch Table and then returned
        # unless name is a present name.
        # If it is a preset name any value in the Hatch Table is ignore.
        # This is due to Writer alters the stored Struct for some unknown reason.
        # Presets are not added to Hatch Table. Write handles this for hatch.
        #
        # After Hatch is added to table all other subsequent call of this name will return (unless preset)
        # that Hatch from the Table. With the exception of auto_name which will force a new entry
        # into the Table each time.
        self._is_preset = False
        if name:
            if not ignore_preset and PresetHatchKind.is_preset(name):
                self._is_preset = True
                # When getting value from Hatch table that Writer has inserted
                # The values are somehow changed by Writer
                # For this reason will return directly here
                return hatch_struct
        else:
            self._auto_name = True
            name = "Hatch"
        nc = self._container_get_inst()
        if self._auto_name:
            # if auto name is True then will not longer be treated as a preset.
            # for preset expect name similar to 'Black 0 Degrees 1'
            self._is_preset = False

            name = name.rstrip() + " "  # add a space after name before getting unique name
            self._name = self._container_get_unique_el_name(name, nc)
        else:
            self._name = name
        hatch = self._container_get_value(self._name, nc)  # raises value error if name is empty
        if not hatch is None:
            return HatchStruct.from_hatch(hatch)

        self._container_add_value(name=self._name, obj=hatch_struct.get_hatch(), allow_update=False, nc=nc)
        hatch = self._container_get_value(self._name, nc)
        return HatchStruct.from_hatch(hatch)

    def _on_hatch_property_change(self) -> None:
        if self._is_preset:
            hs = self._get_hatch_struct()
            self._auto_name = True
            self._set_fill_hatch(hs, True)
            self._is_preset = False

    # endregion Internal Methods

    # region Overrides

    def _supported_services(self) -> Tuple[str, ...]:
        return (
            "com.sun.star.drawing.FillProperties",
            "com.sun.star.text.TextContent",
            "com.sun.star.beans.PropertySet",
        )

    def _container_get_service_name(self) -> str:
        # https://github.com/LibreOffice/core/blob/d9e044f04ac11b76b9a3dac575f4e9155b67490e/chart2/source/tools/PropertyHelper.cxx#L229
        return "com.sun.star.drawing.HatchTable"

    def copy(self: T) -> T:
        cp = super().copy()
        cp._name = self._name
        cp._is_preset = self._is_preset
        cp._auto_name = self._auto_name
        return cp

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

    # region Static Methods
    @classmethod
    def from_preset(cls, preset: PresetHatchKind) -> Hatch:
        """
        Gets an instance from a preset

        Args:
            preset (PatternKind): Preset

        Returns:
            Hatch: Instance from preset.
        """
        # kargs = mPreset.get_write_preset(preset)
        kargs = mPreset.get_fill_preset(preset)
        kargs["name"] = str(preset)
        kargs["auto_name"] = False
        inst = super(Hatch, cls).__new__(cls)
        inst.__init__(**kargs)
        return inst

    @classmethod
    def from_obj(cls, obj: object) -> Hatch:
        """
        Gets instance from object

        Args:
            obj (object): UNO object.

        Raises:
            NotSupportedError: If ``obj`` is not supported.

        Returns:
            Hatch: ``Hatch`` instance that represents ``obj`` hatch pattern.
        """
        nu = super(Hatch, cls).__new__(cls)
        nu.__init__()
        if not nu._is_valid_obj(obj):
            raise mEx.NotSupportedError("Object is not support to convert to Hatch")

        hatch = cast(UnoHatch, mProps.Props.get(obj, "FillHatch"))
        fc = FillColor.from_obj(obj)

        inst = super(Hatch, cls).__new__(cls)
        inst.__init__(
            style=hatch.Style,
            color=hatch.Color,
            space=UnitConvert.convert_mm100_mm(hatch.Distance),
            angle=hatch.Angle,
            bg_color=fc.prop_color,
            name=mProps.Props.get(obj, "FillHatchName"),
            auto_name=False,
        )
        return inst

    # endregion Static Methods

    # region Properties
    @property
    def prop_format_kind(self) -> FormatKind:
        """Gets the kind of style"""
        return FormatKind.TXT_CONTENT | FormatKind.FILL | FormatKind.PARA

    @property
    def prop_bg_color(self) -> Color:
        """Gets sets if fill image is tiled"""
        return self._get_fill_color().prop_color

    @prop_bg_color.setter
    def prop_bg_color(self, value: Color):
        fc = self._get_fill_color()
        fc.prop_color = value
        if value < 0:
            self._set("FillBackground", False)
        else:
            self._set("FillBackground", True)
        self._set_bg_color(self.prop_color)

    @property
    def prop_style(self) -> HatchStyle:
        """Gets/Sets the style of the hatch."""
        return self._get_hatch_struct().prop_style

    @prop_style.setter
    def prop_style(self, value: HatchStyle):
        self._on_hatch_property_change()
        hs = self._get_hatch_struct()
        hs.prop_style = value

    @property
    def prop_color(self) -> Color:
        """Gets/Sets the color of the hatch lines."""
        return self._get_hatch_struct().prop_color

    @prop_color.setter
    def prop_color(self, value: Color):
        self._on_hatch_property_change()
        hs = self._get_hatch_struct()
        hs.prop_color = value
        self._set_bg_color(value)

    @property
    def prop_distance(self) -> float:
        """Gets/Sets the distance between the lines in the hatch (in ``mm`` units)."""
        return self._get_hatch_struct().prop_distance

    @prop_distance.setter
    def prop_distance(self, value: float):
        self._on_hatch_property_change()
        hs = self._get_hatch_struct()
        hs.prop_distance = value

    @property
    def prop_angle(self) -> Angle:
        """Gets/Sets angle of the hatch."""
        return self._get_hatch_struct().prop_angle

    @prop_angle.setter
    def prop_angle(self, value: Angle | int):
        self._on_hatch_property_change()
        hs = self._get_hatch_struct()
        hs.prop_angle = value

    # endregion Properties


def _on_bg_color_setting(source: Any, event_args: KeyValCancelArgs, *args, **kwargs) -> None:
    if event_args.key == "FillStyle":
        event_args.cancel = True
    elif event_args.key == "FillColor":
        # -1 means automatic color.
        # Fillcolor for hatch has not automatic color
        if event_args.value == -1:
            # strickly speaking this is not needed but follows how Draw handles it.
            event_args.value = StandardColor.DEFAULT_BLUE
