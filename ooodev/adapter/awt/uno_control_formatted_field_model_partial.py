from __future__ import annotations
import contextlib
from typing import Any, TYPE_CHECKING
import uno  # pylint: disable=unused-import
from ooo.dyn.text.font_emphasis import FontEmphasisEnum
from ooo.dyn.text.font_relief import FontReliefEnum
from ooo.dyn.style.vertical_alignment import VerticalAlignment
from ooo.dyn.awt.mouse_wheel_behavior import MouseWheelBehaviorEnum
from ooodev.events.partial.events_partial import EventsPartial
from ooodev.utils.kind.border_kind import BorderKind
from ooodev.utils.color import Color
from ooodev.utils.kind.align_kind import AlignKind
from ooodev.utils.partial.model_prop_partial import ModelPropPartial
from .uno_control_model_partial import UnoControlModelPartial
from .font_descriptor_comp import FontDescriptorComp

if TYPE_CHECKING:
    from com.sun.star.util import XNumberFormatsSupplier
    from com.sun.star.awt import UnoControlFormattedFieldModel  # Service
    from com.sun.star.awt import FontDescriptor  # struct
    from ooodev.events.args.key_val_args import KeyValArgs


class UnoControlFormattedFieldModelPartial(UnoControlModelPartial):
    """Partial class for UnoControlFormattedFieldModel."""

    def __init__(self):
        """
        Constructor

        Args:
            component (Any): Component that implements ``com.sun.star.awt.UnoControlFormattedFieldModel`` service.
        """
        # pylint: disable=unused-argument
        if not isinstance(self, ModelPropPartial):
            raise TypeError("This class must be used as a mixin that implements ModelPropPartial.")

        self.model: UnoControlFormattedFieldModel
        event_provider = self if isinstance(self, EventsPartial) else None
        UnoControlModelPartial.__init__(self)
        self.__font_descriptor = FontDescriptorComp(self.model.FontDescriptor, event_provider)

        if event_provider is not None:

            def on_font_descriptor_changed(src: Any, event_args: KeyValArgs) -> None:
                self.model.FontDescriptor = self.__font_descriptor.component

            self.__fn_on_font_descriptor_changed = on_font_descriptor_changed
            # pylint: disable=no-member
            event_provider.subscribe_event("font_descriptor_struct_changed", self.__fn_on_font_descriptor_changed)

    def set_font_descriptor(self, font_descriptor: FontDescriptor) -> None:
        """
        Sets the font descriptor of the control.

        Args:
            font_descriptor (FontDescriptor): UNO Struct - Font descriptor to set.
        """
        # FontDescriptorComp do not have any state, so we can directly assign the component.
        self.__font_descriptor.component = font_descriptor
        self.model.FontDescriptor = self.__font_descriptor.component

    # region Properties

    @property
    def font_descriptor(self) -> FontDescriptorComp:
        """
        Gets the Font Descriptor

        Hint:
            ``set_font_descriptor()`` can be used to set the font descriptor.
        """
        return self.__font_descriptor

    @property
    def align(self) -> AlignKind:
        """
        Get/Sets the horizontal alignment of the text in the control.

        Hint:
            - ``AlignKind`` can be imported from ``ooodev.utils.kind.align_kind``.
        """
        return AlignKind(self.model.Align)

    @align.setter
    def align(self, value: AlignKind | int) -> None:
        kind = AlignKind(int(value))
        self.model.Align = kind.value

    @property
    def background_color(self) -> Color:
        """
        Gets/Set the background color of the control.

        Returns:
            ~ooodev.utils.color.Color: Color
        """
        return Color(self.model.BackgroundColor)

    @background_color.setter
    def background_color(self, value: Color) -> None:
        self.model.BackgroundColor = value  # type: ignore

    @property
    def border(self) -> BorderKind:
        """
        Gets/Sets the border style of the control.

        Note:
            Value can be set with ``BorderKind`` or ``int``.

        Hint:
            - ``BorderKind`` can be imported from ``ooodev.utils.kind.border_kind``.
        """
        return BorderKind(self.model.Border)

    @border.setter
    def border(self, value: int | BorderKind) -> None:
        kind = BorderKind(int(value))
        self.model.Border = kind.value

    @property
    def border_color(self) -> Color | None:
        """
        Gets/Sets the color of the border, if present

        Not every border style (see Border) may support coloring.
        For instance, usually a border with 3D effect will ignore the border_color setting.

        **optional**

        Returns:
            ~ooodev.utils.color.Color | None: Color or None if not set.
        """
        with contextlib.suppress(AttributeError):
            return Color(self.model.BorderColor)
        return None

    @border_color.setter
    def border_color(self, value: Color) -> None:
        with contextlib.suppress(AttributeError):
            self.model.BorderColor = value

    @property
    def effective_default(self) -> Any:
        """
        Gets the default value of the formatted field.

        This may be a numeric value (double) or a string, depending on the formatting of the field.
        """
        return self.model.EffectiveDefault

    @effective_default.setter
    def effective_default(self, value: Any) -> None:
        self.model.EffectiveDefault = value

    @property
    def effective_max(self) -> float:
        """
        Gets/Sets the maximum value that can be entered.

        This property is ignored if the format of the field is no numeric format.
        """
        return self.model.EffectiveMax

    @effective_max.setter
    def effective_max(self, value: float) -> None:
        self.model.EffectiveMax = value

    @property
    def effective_min(self) -> float:
        """
        Gets/Sets the minimum value that can be entered.

        This property is ignored if the format of the field is no numeric format.
        """
        return self.model.EffectiveMin

    @effective_min.setter
    def effective_min(self, value: float) -> None:
        self.model.EffectiveMin = value

    @property
    def effective_value(self) -> Any:
        """
        Gets/Sets specifies the current value of the formatted field.

        This may be a numeric value (float) or a string, depending on the formatting of the field.
        """
        # not sure why but UnoControlFormattedFieldModel does not have EffectiveValue property.
        # however, it is documented in the API.
        return self.model.EffectiveValue  # type: ignore

    @effective_value.setter
    def effective_value(self, value: Any) -> None:
        self.model.EffectiveValue = value  # type: ignore

    @property
    def enabled(self) -> bool:
        """
        Gets/Sets whether the control is enabled or disabled.
        """
        return self.model.Enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self.model.Enabled = value

    @property
    def font_emphasis_mark(self) -> FontEmphasisEnum:
        """
        Gets/Sets the ``FontEmphasis`` value of the text in the control.

        Note:
            Value can be set with ``FontEmphasisEnum`` or ``int``.

        Hint:
            - ``FontEmphasisEnum`` can be imported from ``ooo.dyn.text.font_emphasis``.
        """
        return FontEmphasisEnum(self.model.FontEmphasisMark)

    @font_emphasis_mark.setter
    def font_emphasis_mark(self, value: int | FontEmphasisEnum) -> None:
        self.model.FontEmphasisMark = int(value)

    @property
    def font_relief(self) -> FontReliefEnum:
        """
        Gets/Sets ``FontRelief`` value of the text in the control.

        Note:
            Value can be set with ``FontReliefEnum`` or ``int``.

        Hint:
            - ``FontReliefEnum`` can be imported from ``ooo.dyn.text.font_relief``.
        """
        return FontReliefEnum(self.model.FontRelief)

    @property
    def format_key(self) -> int:
        """
        Gets/Sets the format to be used when formatting the field input and output.

        This value is meaningful relative to the ``formats_supplier`` property only.
        """
        return self.model.FormatKey

    @format_key.setter
    def format_key(self, value: int) -> None:
        self.model.FormatKey = value

    @font_relief.setter
    def font_relief(self, value: int | FontReliefEnum) -> None:
        self.model.FontRelief = int(value)

    @property
    def formats_supplier(self) -> XNumberFormatsSupplier:
        """
        Gets/Sets - supplies the formats the field should work with.
        """
        return self.model.FormatsSupplier

    @formats_supplier.setter
    def formats_supplier(self, value: XNumberFormatsSupplier) -> None:
        self.model.FormatsSupplier = value

    @property
    def help_text(self) -> str:
        """
        Get/Sets the help text of the control.
        """
        return self.model.HelpText

    @help_text.setter
    def help_text(self, value: str) -> None:
        self.model.HelpText = value

    @property
    def help_url(self) -> str:
        """
        Gets/Sets the help URL of the control.
        """
        return self.model.HelpURL

    @help_url.setter
    def help_url(self, value: str) -> None:
        self.model.HelpURL = value

    @property
    def hide_inactive_selection(self) -> bool | None:
        """
        Gets/Sets whether the selection in the control should be hidden when the control is not active (focused).

        **optional**
        """
        with contextlib.suppress(AttributeError):
            return self.model.HideInactiveSelection
        return None

    @hide_inactive_selection.setter
    def hide_inactive_selection(self, value: bool) -> None:
        with contextlib.suppress(AttributeError):
            self.model.HideInactiveSelection = value

    @property
    def max_text_len(self) -> int:
        """
        Gets/Sets the maximum character count.

        There's no limitation, if set to 0.
        """
        return self.model.MaxTextLen

    @max_text_len.setter
    def max_text_len(self, value: int) -> None:
        self.model.MaxTextLen = value

    @property
    def mouse_wheel_behavior(self) -> MouseWheelBehaviorEnum | None:
        """
        Gets/Sets how the mouse wheel can be used to scroll through the control's content.

        Usually, the mouse wheel scroll through the control's entry list.
        Using this property,you can control under which circumstances this is possible.

        **optional**

        Note:
            Value can be set with ``MouseWheelBehaviorEnum`` or ``int``.

        Hint:
            - ``MouseWheelBehaviorEnum`` can be imported from ``ooo.dyn.awt.mouse_wheel_behavior``
        """
        with contextlib.suppress(AttributeError):
            return MouseWheelBehaviorEnum(self.model.MouseWheelBehavior)
        return None

    @mouse_wheel_behavior.setter
    def mouse_wheel_behavior(self, value: int | MouseWheelBehaviorEnum) -> None:
        with contextlib.suppress(AttributeError):
            self.model.MouseWheelBehavior = int(value)

    @property
    def printable(self) -> bool:
        """
        Gets/Sets that the control will be printed with the document.
        """
        return self.model.Printable

    @printable.setter
    def printable(self, value: bool) -> None:
        self.model.Printable = value

    @property
    def read_only(self) -> bool:
        """
        Gets/Sets if the content of the control cannot be modified by the user.
        """
        return self.model.ReadOnly

    @read_only.setter
    def read_only(self, value: bool) -> None:
        self.model.ReadOnly = value

    @property
    def repeat(self) -> bool | None:
        """
        Gets/Sets whether the mouse should show repeating behavior, i.e.
        repeatedly trigger an action when keeping pressed.

        **optional**
        """
        with contextlib.suppress(AttributeError):
            return self.model.Repeat
        return None

    @repeat.setter
    def repeat(self, value: bool) -> None:
        with contextlib.suppress(AttributeError):
            self.model.Repeat = value

    @property
    def repeat_delay(self) -> int | None:
        """
        Gets/Sets the mouse repeat delay, in milliseconds.

        When the user presses a mouse in a control area where this triggers an action (such as spinning the value), then usual control implementations allow to repeatedly trigger this action, without the need to release the mouse button and to press it again.
        The delay between two such triggers is specified with this property.

        **optional**
        """
        with contextlib.suppress(AttributeError):
            return self.model.RepeatDelay
        return None

    @repeat_delay.setter
    def repeat_delay(self, value: int) -> None:
        with contextlib.suppress(AttributeError):
            self.model.RepeatDelay = value

    @property
    def spin(self) -> bool:
        """
        Gets/Sets if the control has a spin button.
        """
        return self.model.Spin

    @spin.setter
    def spin(self, value: bool) -> None:
        self.model.Spin = value

    @property
    def strict_format(self) -> bool:
        """
        Gets/Sets if the value is checked during the user input.
        """
        return self.model.StrictFormat

    @strict_format.setter
    def strict_format(self, value: bool) -> None:
        self.model.StrictFormat = value

    @property
    def tabstop(self) -> bool:
        """
        Gets/Sets that the control can be reached with the TAB key.
        """
        return self.model.Tabstop

    @tabstop.setter
    def tabstop(self, value: bool) -> None:
        self.model.Tabstop = value

    @property
    def text(self) -> str:
        """
        Gets/Sets the text displayed in the control.
        """
        return self.model.Text

    @text.setter
    def text(self, value: str) -> None:
        self.model.Text = value

    @property
    def text_color(self) -> Color:
        """
        Gets/Sets the text color of the control.

        Returns:
            ~ooodev.utils.color.Color: Color
        """
        return Color(self.model.TextColor)

    @text_color.setter
    def text_color(self, value: Color) -> None:
        self.model.TextColor = value  # type: ignore

    @property
    def text_line_color(self) -> Color:
        """
        Gets/Sets the text line color of the control.

        Returns:
            ~ooodev.utils.color.Color: Color
        """
        return Color(self.model.TextLineColor)

    @text_line_color.setter
    def text_line_color(self, value: Color) -> None:
        self.model.TextLineColor = value  # type: ignore

    @property
    def treat_as_number(self) -> bool:
        """
        Gets/Sets if the text is treated as a number.
        """
        return self.model.TreatAsNumber

    @treat_as_number.setter
    def treat_as_number(self, value: bool) -> None:
        self.model.TreatAsNumber = value

    @property
    def vertical_align(self) -> VerticalAlignment | None:
        """
        Gets/Sets the vertical alignment of the text in the control.

        **optional**

        Hint:
            - ``VerticalAlignment`` can be imported from ``ooo.dyn.style.vertical_alignment``
        """
        with contextlib.suppress(AttributeError):
            return self.model.VerticalAlign  # type: ignore
        return None

    @vertical_align.setter
    def vertical_align(self, value: VerticalAlignment) -> None:
        with contextlib.suppress(AttributeError):
            self.model.VerticalAlign = value  # type: ignore

    @property
    def writing_mode(self) -> int | None:
        """
        Denotes the writing mode used in the control, as specified in the ``com.sun.star.text.WritingMode2`` constants group.

        Only LR_TB (``0``) and RL_TB (``1``) are supported at the moment.

        **optional**
        """
        with contextlib.suppress(AttributeError):
            return self.model.WritingMode
        return None

    @writing_mode.setter
    def writing_mode(self, value: int) -> None:
        with contextlib.suppress(AttributeError):
            self.model.WritingMode = value

    # endregion Properties