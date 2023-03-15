from __future__ import annotations
import pytest
from typing import TYPE_CHECKING, cast

if __name__ == "__main__":
    pytest.main([__file__])

import uno
from ooodev.format.writer.direct.char.font import (
    Font,
    FontStrikeoutEnum,
    FontUnderlineEnum,
    FontWeightEnum,
    CharSetEnum,
    FontFamilyEnum,
    FontSlant,
    CharSpacingKind,
    FontScriptKind,
    FontPosition,
    FontEffects,
    FontOnly,
    CaseMapEnum,
    FontReliefEnum,
    FontLang,
)
from ooodev.format.writer.style.para import Para
from ooodev.format import CommonColor
from ooodev.utils.unit_convert import UnitConvert
from ooodev.utils.gui import GUI
from ooodev.utils.info import Info
from ooodev.utils.lo import Lo

if TYPE_CHECKING:
    from com.sun.star.style import CharacterProperties  # service


def test_font_chain() -> None:
    ft = Font().bold
    assert ft.prop_weight == FontWeightEnum.BOLD
    ft = ft.italic
    assert ft.prop_weight == FontWeightEnum.BOLD
    assert ft.prop_is_italic
    assert ft.prop_is_bold

    ft = ft.fmt_color(CommonColor.RED)
    assert ft.prop_weight == FontWeightEnum.BOLD
    assert ft.prop_is_italic
    assert ft.prop_is_bold
    assert ft.prop_color == CommonColor.RED

    ft = ft.fmt_bg_color(CommonColor.BLUE)
    assert ft.prop_weight == FontWeightEnum.BOLD
    assert ft.prop_is_italic
    assert ft.prop_is_bold
    assert ft.prop_color == CommonColor.RED
    assert ft.prop_bg_color == CommonColor.BLUE

    ft = ft.underline
    assert ft.prop_weight == FontWeightEnum.BOLD
    assert ft.prop_is_italic
    assert ft.prop_is_bold
    assert ft.prop_color == CommonColor.RED
    assert ft.prop_bg_color == CommonColor.BLUE
    assert ft.prop_is_underline

    ft = ft.strike
    assert ft.prop_weight == FontWeightEnum.BOLD
    assert ft.prop_is_italic
    assert ft.prop_is_bold
    assert ft.prop_color == CommonColor.RED
    assert ft.prop_bg_color == CommonColor.BLUE
    assert ft.prop_is_underline
    assert ft.prop_strike == FontStrikeoutEnum.SINGLE

    ft = ft.shadowed
    assert ft.prop_weight == FontWeightEnum.BOLD
    assert ft.prop_is_italic
    assert ft.prop_is_bold
    assert ft.prop_color == CommonColor.RED
    assert ft.prop_bg_color == CommonColor.BLUE
    assert ft.prop_is_underline
    assert ft.prop_strike == FontStrikeoutEnum.SINGLE
    assert ft.prop_shadowed


def test_font(loader) -> None:
    ft = Font(
        name=Info.get_font_general_name(),
        size=22.0,
        charset=CharSetEnum.SYSTEM,
        family=FontFamilyEnum.MODERN,
        b=True,
        i=True,
        u=True,
        color=CommonColor.BLUE,
        strike=FontStrikeoutEnum.BOLD,
        underline_color=CommonColor.AQUA,
        overline=FontUnderlineEnum.BOLDDASHDOT,
        overline_color=CommonColor.BEIGE,
        superscript=True,
        rotation=90.0,
        spacing=CharSpacingKind.TIGHT,
        shadowed=True,
    )
    assert ft.prop_name == Info.get_font_general_name()
    assert ft.prop_charset == CharSetEnum.SYSTEM
    assert ft.prop_family == FontFamilyEnum.MODERN
    assert ft.prop_is_bold
    assert ft.prop_is_italic
    assert ft.prop_is_underline
    assert ft.prop_weight == FontWeightEnum.BOLD
    assert ft.prop_slant == FontSlant.ITALIC
    assert ft.prop_underline == FontUnderlineEnum.SINGLE
    assert ft.prop_color == CommonColor.BLUE
    assert ft.prop_strike == FontStrikeoutEnum.BOLD
    assert ft.prop_underline_color == CommonColor.AQUA
    assert ft.prop_superscript
    assert ft.prop_size.value == 22.0
    assert ft.prop_rotation == 90.0
    assert ft.prop_overline == FontUnderlineEnum.BOLDDASHDOT
    assert ft.prop_overline_color == CommonColor.BEIGE
    assert ft.prop_spacing.value == pytest.approx(CharSpacingKind.TIGHT.value, rel=1e-2)
    assert ft.prop_shadowed

    ft = Font(
        weight=FontWeightEnum.BOLD,
        underine=FontUnderlineEnum.BOLDDASH,
        slant=FontSlant.OBLIQUE,
        subscript=True,
        spacing=2.0,
    )
    assert ft.prop_weight == FontWeightEnum.BOLD
    assert ft.prop_is_underline
    assert ft.prop_underline == FontUnderlineEnum.BOLDDASH
    assert ft.prop_slant == FontSlant.OBLIQUE
    assert ft.prop_subscript
    assert ft.prop_spacing.value == pytest.approx(2.0, rel=1e-2)


def test_font_effects() -> None:
    fp = FontPosition(
        script_kind=FontScriptKind.SUPERSCRIPT,
        rel_size=45,
        raise_lower=58,
        rotation=93,
        scale=99,
        spacing=CharSpacingKind.TIGHT,
        pair=True,
    )
    assert fp.prop_script_kind == FontScriptKind.SUPERSCRIPT
    assert fp.prop_rel_size == 45
    assert fp.prop_raise_lower == 58
    assert fp.prop_rotation == 93
    assert fp.prop_scale == 99
    assert fp.prop_spacing.value == pytest.approx(CharSpacingKind.TIGHT.value, 0.01)
    assert fp.prop_pair == True

    fp = fp.script_kind_subscript
    assert fp.prop_script_kind == FontScriptKind.SUBSCRIPT
    assert fp.prop_raise_lower == 58

    fp = fp.spacing_normal
    assert fp.prop_spacing.value == pytest.approx(CharSpacingKind.NORMAL.value, 0.01)

    fp = fp.rotation_270
    assert fp.prop_rotation == 270

    fp.prop_script_kind = FontScriptKind.NORMAL
    assert fp.prop_rel_size == 100
    assert fp.prop_raise_lower == 0


def test_font_cursor(loader) -> None:
    delay = 0  # 0 if Lo.bridge_connector.headless else 5_000
    from ooodev.office.write import Write
    from ooodev.format import Styler
    from functools import partial

    doc = Write.create_doc()
    if not Lo.bridge_connector.headless:
        GUI.set_visible()
        Lo.delay(500)
        GUI.zoom(GUI.ZoomEnum.ZOOM_150_PERCENT)
    try:
        ft = Font(size=30.0, b=True, i=True, u=True, color=CommonColor.BLUE, underline_color=CommonColor.GREEN)
        cursor = Write.get_cursor(doc)
        style = partial(Styler.apply, cursor)
        Write.append(cursor, "hello")
        cursor.goLeft(5, True)
        ft.apply(cursor)
        cp = cast("CharacterProperties", cursor)
        assert cp.CharColor == CommonColor.BLUE
        assert cp.CharUnderlineColor == CommonColor.GREEN
        assert cp.CharWeight == FontWeightEnum.BOLD.value
        assert cp.CharPosture == FontSlant.ITALIC
        assert cp.CharUnderline == FontUnderlineEnum.SINGLE.value
        assert cp.CharHeight == pytest.approx(30.0, rel=1e-2)

        # clear attributes or cursor will continue on with font setting just set above.
        # Lo.dispatch_cmd("ResetAttributes")
        # Lo.delay(500)
        cursor.gotoEnd(False)
        Para.default.apply(cursor)

        Styler.apply(cursor, Font(size=40))
        Write.append(cursor, " world")

        cursor.goLeft(5, False)
        cursor.goRight(1, True)
        Styler.apply(cursor, Font(superscript=True))
        assert cp.CharEscapement == 14_000

        cursor.gotoEnd(False)
        cursor.goLeft(1, True)
        # use partial function
        style(Font(subscript=True))
        assert cp.CharEscapement == -14_000
        cursor.gotoEnd(False)

        Write.end_paragraph(cursor)

        Write.append(cursor, "BIG")
        cursor.goLeft(3, True)
        style(Font(size=36, rotation=90.0))
        assert cp.CharRotation == 900
        cursor.gotoEnd(False)

        Write.end_paragraph(cursor)
        cursor.gotoEnd(False)
        Para.default.apply(cursor)

        Write.append(cursor, "Overline")
        cursor.goLeft(8, True)
        style(Font(overline=FontUnderlineEnum.BOLDWAVE, size=40, overline_color=CommonColor.CHARTREUSE))
        # no documentation found for Overline
        assert cursor.CharOverlineHasColor
        assert cursor.CharOverlineColor == CommonColor.CHARTREUSE
        assert cursor.CharOverline == FontUnderlineEnum.BOLDWAVE
        cursor.gotoEnd(False)
        Write.end_paragraph(cursor)

        cursor.gotoEnd(False)
        Para.default.apply(cursor)
        Write.append(cursor, "Highlite")
        cursor.goLeft(8, True)
        style(Font(bg_color=CommonColor.LIGHT_YELLOW))
        assert cp.CharBackColor == CommonColor.LIGHT_YELLOW
        cursor.gotoEnd(False)
        Write.end_paragraph(cursor)

        cursor.gotoEnd(False)
        Para.default.apply(cursor)
        Write.append(cursor, "Very Tight")
        cursor.goLeft(10, True)
        style(Font(spacing=CharSpacingKind.VERY_TIGHT, size=30))
        assert cp.CharKerning == UnitConvert.convert_pt_mm100(CharSpacingKind.VERY_TIGHT.value)
        cursor.gotoEnd(False)
        Write.end_paragraph(cursor)

        Write.append(cursor, "Tight")
        cursor.goLeft(5, True)
        style(Font(spacing=CharSpacingKind.TIGHT, size=30))
        assert cp.CharKerning == UnitConvert.convert_pt_mm100(CharSpacingKind.TIGHT.value)
        cursor.gotoEnd(False)
        Write.end_paragraph(cursor)

        Write.append(cursor, "Normal")
        cursor.goLeft(6, True)
        style(Font(spacing=CharSpacingKind.NORMAL, size=30))
        assert cp.CharKerning == 0
        cursor.gotoEnd(False)
        Write.end_paragraph(cursor)

        Write.append(cursor, "Loose")
        cursor.goLeft(5, True)
        style(Font(spacing=CharSpacingKind.LOOSE, size=30))
        assert cp.CharKerning == UnitConvert.convert_pt_mm100(CharSpacingKind.LOOSE.value)
        cursor.gotoEnd(False)
        Write.end_paragraph(cursor)

        Write.append(cursor, "Very Loose")
        cursor.goLeft(10, True)
        style(Font(spacing=CharSpacingKind.VERY_LOOSE, size=30))
        assert cp.CharKerning == UnitConvert.convert_pt_mm100(CharSpacingKind.VERY_LOOSE.value)
        cursor.gotoEnd(False)
        Write.end_paragraph(cursor)

        Write.append(cursor, "Custom Spacing 6 pt")
        cursor.goLeft(19, True)
        style(Font(spacing=19.0, size=14))
        assert cp.CharKerning == UnitConvert.convert_pt_mm100(19.0)
        cursor.gotoEnd(False)
        Write.end_paragraph(cursor)

        cursor.gotoEnd(False)
        Para.default.apply(cursor)

        Write.append(cursor, "Shadowed")
        cursor.goLeft(8, True)
        style(Font(size=40, shadowed=True))
        assert cp.CharShadowed
        cursor.gotoEnd(False)
        Write.end_paragraph(cursor)

        Lo.delay(delay)
    finally:
        Lo.close_doc(doc)


def test_font_position_super_sub_cursor(loader) -> None:
    delay = 0  # 0 if Lo.bridge_connector.headless else 5_000
    from ooodev.office.write import Write

    doc = Write.create_doc()
    if not Lo.bridge_connector.headless:
        GUI.set_visible()
        Lo.delay(500)
        GUI.zoom(GUI.ZoomEnum.ZOOM_150_PERCENT)
    try:
        fp = FontPosition().script_kind_superscript
        cursor = Write.get_cursor(doc)
        Write.append(cursor, "hello")
        Write.style(pos=0, length=1, styles=(fp,), cursor=cursor)
        cursor.gotoStart(False)
        cursor.goLeft(1, True)
        cp = cast("CharacterProperties", cursor)
        assert cp.CharEscapement == FontScriptKind.SUPERSCRIPT.value
        assert cp.CharEscapementHeight == FontPosition._DEFAULT_SUPER_SUB_HEIGHT

        fp = fp.script_kind_subscript
        Write.style(pos=4, length=1, styles=(fp,), cursor=cursor)
        cursor.goLeft(1, True)
        assert cp.CharEscapement == FontScriptKind.SUBSCRIPT.value
        assert cp.CharEscapementHeight == FontPosition._DEFAULT_SUPER_SUB_HEIGHT
        cursor.gotoEnd(False)

        fp.default.apply(cursor)
        Write.end_paragraph(cursor=cursor)
        pos = Write.get_position(cursor)
        Write.append(cursor, "hello")
        fp.prop_raise_lower = 47
        Write.style(pos=pos, length=1, styles=(fp,), cursor=cursor)
        cursor.goLeft(5, False)
        cursor.goRight(1, True)
        assert cp.CharEscapement == -47
        assert cp.CharEscapementHeight == FontPosition._DEFAULT_SUPER_SUB_HEIGHT

        fp = fp.script_kind_superscript
        fp.prop_rel_size = 45
        Write.style(pos=pos + 4, length=1, styles=(fp,), cursor=cursor)
        cursor.gotoEnd(False)
        cursor.goRight(1, True)
        assert cp.CharEscapement == 47
        assert cp.CharEscapementHeight == 45
        cursor.gotoEnd(False)
        Write.end_paragraph(cursor)

        fp = fp.script_kind_normal
        pos = Write.get_position(cursor)
        Write.append(cursor, "hello")
        Write.style(pos=pos, length=1, styles=(fp,), cursor=cursor)
        cursor.goLeft(5, False)
        cursor.goRight(1, True)
        assert cp.CharEscapement == 0
        assert cp.CharEscapementHeight == 100
        cursor.gotoEnd(False)

        Lo.delay(delay)
    finally:
        Lo.close_doc(doc)


def test_font_position_rotation_cursor(loader) -> None:
    delay = 0  # 0 if Lo.bridge_connector.headless else 5_000
    from ooodev.office.write import Write

    doc = Write.create_doc()
    if not Lo.bridge_connector.headless:
        GUI.set_visible()
        Lo.delay(500)
        GUI.zoom(GUI.ZoomEnum.ZOOM_150_PERCENT)
    try:
        fp = FontPosition().rotation_270.fit
        cursor = Write.get_cursor(doc)
        Write.append(cursor, "hello", (fp,))
        cursor.gotoStart(False)
        cursor.goLeft(5, True)
        cp = cast("CharacterProperties", cursor)
        assert cp.CharRotation == 2700
        assert cp.CharRotationIsFitToLine
        cursor.gotoEnd(False)
        Write.end_paragraph(cursor)

        fp = FontPosition(rotation=90, fit=False, scale=90)
        Write.append(cursor, "hello", (fp,))
        cursor.goLeft(5, True)
        cp = cast("CharacterProperties", cursor)
        assert cp.CharRotation == 900
        assert cp.CharRotationIsFitToLine == False
        assert cp.CharScaleWidth == 90

        fp = FontPosition.from_obj(cursor)
        cursor.gotoEnd(False)
        Write.end_paragraph(cursor)

        Write.append(cursor, "hello", (fp,))
        cursor.goLeft(5, True)
        cp = cast("CharacterProperties", cursor)
        assert cp.CharRotation == 900
        assert cp.CharRotationIsFitToLine == False
        assert cp.CharScaleWidth == 90
        cursor.gotoEnd(False)
        Write.end_paragraph(cursor)

        # in write setting and angle other then 0, 180, or 270 results in Writer converting it.
        fp.prop_rotation = 45
        fp.prop_fit = True
        Write.append(cursor, "hello", (fp,))
        cursor.goLeft(5, True)
        cp = cast("CharacterProperties", cursor)
        assert cp.CharRotation == 2700  # 270 degrees
        assert cp.CharRotationIsFitToLine
        assert cp.CharScaleWidth == 90
        cursor.gotoEnd(False)
        Write.end_paragraph(cursor)

        Lo.delay(delay)
    finally:
        Lo.close_doc(doc)


def test_font_position_spacing_cursor(loader) -> None:
    delay = 0  # 0 if Lo.bridge_connector.headless else 5_000
    from ooodev.office.write import Write

    doc = Write.create_doc()
    if not Lo.bridge_connector.headless:
        GUI.set_visible()
        Lo.delay(500)
        GUI.zoom(GUI.ZoomEnum.ZOOM_150_PERCENT)
    try:
        fp = FontPosition(spacing=CharSpacingKind.TIGHT, pair=False)
        cursor = Write.get_cursor(doc)
        Write.append(cursor, "hello", (fp,))
        cursor.gotoStart(False)
        cursor.goLeft(5, True)
        cp = cast("CharacterProperties", cursor)
        assert cp.CharAutoKerning == False
        assert cp.CharKerning in (-52, -53, -54)
        cursor.gotoEnd(False)
        Write.end_paragraph(cursor)

        fp = fp.spacing_very_loose.pair
        Write.append(cursor, "hello", (fp,))
        cursor.goLeft(5, True)
        cp = cast("CharacterProperties", cursor)
        assert cp.CharAutoKerning
        assert cp.CharKerning in (211, 212, 213)
        cursor.gotoEnd(False)
        Write.end_paragraph(cursor)

        Lo.delay(delay)
    finally:
        Lo.close_doc(doc)


def test_font_effects_cursor(loader) -> None:
    delay = 0  # 0 if Lo.bridge_connector.headless else 5_000
    from ooodev.office.write import Write
    from ooodev.format import Styler
    from functools import partial

    doc = Write.create_doc()
    if not Lo.bridge_connector.headless:
        GUI.set_visible()
        Lo.delay(500)
        GUI.zoom(GUI.ZoomEnum.ZOOM_150_PERCENT)
    try:
        fp = FontEffects(color=CommonColor.BLUE, underline_color=CommonColor.GREEN)
        cursor = Write.get_cursor(doc)
        style = partial(Styler.apply, cursor)
        Write.append(cursor, "hello")
        cursor.goLeft(5, True)
        fp.apply(cursor)
        cp = cast("CharacterProperties", cursor)
        assert cp.CharColor == CommonColor.BLUE
        assert cp.CharUnderlineColor == CommonColor.GREEN

        # clear attributes or cursor will continue on with font setting just set above.
        # Lo.dispatch_cmd("ResetAttributes")
        # Lo.delay(500)
        cursor.gotoEnd(False)

        cursor.gotoEnd(False)
        cursor.goLeft(5, True)
        fp = FontEffects.from_obj(cursor)
        default_font = fp.default.copy()
        fp.prop_overline = FontUnderlineEnum.DASH
        fp.prop_overline_color = CommonColor.AZURE
        Styler.apply(cursor, fp)
        assert cp.CharOverlineColor == CommonColor.AZURE
        assert cursor.CharOverline == FontUnderlineEnum.DASH.value
        assert cp.CharOverlineHasColor

        fp = fp.overline_color_auto
        fp.apply(cursor)
        assert cp.CharOverlineColor == -1
        assert cp.CharOverlineHasColor == False
        cursor.gotoEnd(False)
        default_font.apply(cursor)
        Write.end_paragraph(cursor)

        Write.append(cursor, "hello")
        cursor.goLeft(5, False)
        cursor.goRight(1, True)
        fp = FontEffects(case=CaseMapEnum.SMALLCAPS)
        fp.apply(cursor)
        assert cp.CharCaseMap == CaseMapEnum.SMALLCAPS.value
        cursor.gotoEnd(False)
        Write.end_paragraph(cursor)

        Write.append(cursor, "Hello")
        cursor.goLeft(5, True)
        style(FontEffects(shadowed=True))
        assert cp.CharShadowed
        cursor.gotoEnd(False)
        Write.end_paragraph(cursor)

        fp = FontEffects(transparency=15)
        Write.append(cursor, "Hello")
        cursor.goLeft(5, True)
        fp.apply(cursor)
        assert cp.CharTransparence == 15
        cursor.gotoEnd(False)
        default_font.apply(cursor)
        Write.end_paragraph(cursor)

        fp = FontEffects(hidden=True)
        Write.append(cursor, "Hello")
        cursor.goLeft(5, True)
        fp.apply(cursor)
        assert cp.CharHidden
        cursor.gotoEnd(False)
        default_font.apply(cursor)
        Write.end_paragraph(cursor)

        fp = FontEffects().outline
        Write.append(cursor, "Hello")
        cursor.goLeft(5, True)
        fp.apply(cursor)
        assert cp.CharContoured
        cursor.gotoEnd(False)
        default_font.apply(cursor)
        Write.end_paragraph(cursor)

        fp = FontEffects().relief_embossed
        Write.append(cursor, "Hello")
        cursor.goLeft(5, True)
        fp.apply(cursor)
        assert cp.CharRelief == FontReliefEnum.EMBOSSED.value
        cursor.gotoEnd(False)
        default_font.apply(cursor)
        Write.end_paragraph(cursor)

        # When relief is set shadow should be ignored
        # property can still be applied without issue.
        # same is true for outline property
        fp = fp.relief_engraved.shadowed
        Write.append(cursor, "Hello")
        cursor.goLeft(5, True)
        fp.apply(cursor)
        assert cp.CharRelief == FontReliefEnum.ENGRAVED.value
        cursor.gotoEnd(False)
        default_font.apply(cursor)
        Write.end_paragraph(cursor)

        fp = FontEffects(strike=FontStrikeoutEnum.DOUBLE, word_mode=True)
        Write.append(cursor, "Hello World")
        cursor.goLeft(11, True)
        fp.apply(cursor)
        assert cp.CharStrikeout == FontStrikeoutEnum.DOUBLE.value
        assert cp.CharWordMode
        cursor.gotoEnd(False)
        default_font.apply(cursor)
        Write.end_paragraph(cursor)

        Lo.delay(delay)
    finally:
        Lo.close_doc(doc)


def test_font_only_cursor(loader) -> None:
    delay = 0  # 0 if Lo.bridge_connector.headless else 5_000
    from ooodev.office.write import Write
    from ooodev.format import Styler
    from functools import partial

    doc = Write.create_doc()
    if not Lo.bridge_connector.headless:
        GUI.set_visible()
        Lo.delay(500)
        GUI.zoom(GUI.ZoomEnum.ZOOM_150_PERCENT)
    try:
        # lang = Lang.default
        # fe1 = FontOnly.default
        # fe2 = FontOnly.default
        # assert fe1 is fe2
        # fe_caption = FontOnly.default_caption
        # fe_heading = FontOnly.default_heading
        # fe_index = FontOnly.default_index
        # fe_list = FontOnly.default_list

        fo = FontOnly(name="DejaVu Sans Mono", size=14.0)
        cursor = Write.get_cursor(doc)
        Write.append(cursor, "hello")
        cursor.goLeft(5, True)
        fo.apply(cursor)
        cp = cast("CharacterProperties", cursor)
        assert cp.CharFontName == "DejaVu Sans Mono"
        assert cp.CharHeight == pytest.approx(14, 0.01)
        cursor.gotoEnd(False)
        FontOnly.default.apply(cursor)
        Write.end_paragraph(cursor)

        # fd = fo.get_font_descriptor()
        # assert fd is not None

        fo = FontOnly(name="Lucida Fax", style_name="Demibold Italic")
        Write.append(cursor, "World")
        cursor.goLeft(5, True)
        fo.apply(cursor)
        assert cp.CharFontName == "Lucida Fax"
        assert cp.CharFontStyleName == "Demibold Italic"
        cursor.gotoEnd(False)
        FontOnly.default.apply(cursor)
        Write.end_paragraph(cursor)

        fo = FontOnly(name="Noto Serif Cond", style_name="Regular", size=14.0)
        Write.append(cursor, "World")
        cursor.goLeft(5, True)
        fo.apply(cursor)
        assert cp.CharFontName == "Noto Serif Cond"
        assert cp.CharFontStyleName == "Regular"
        cursor.gotoEnd(False)
        FontOnly.default.apply(cursor)
        Write.end_paragraph(cursor)

        fo = FontOnly(name="Noto Serif Cond", style_name="Bold Italic", size=15.0)
        Write.append(cursor, "World")
        cursor.goLeft(5, True)
        fo.apply(cursor)
        assert cp.CharFontName == "Noto Serif Cond"
        assert cp.CharFontStyleName == "Bold Italic"
        cursor.gotoEnd(False)
        FontOnly.default.apply(cursor)
        Write.end_paragraph(cursor)

        lang = FontLang().english_canada
        fo = FontOnly(name="Noto Serif Cond", style_name="Italic", size=15.0, lang=lang)
        Write.append(cursor, "World")
        cursor.goLeft(5, True)
        fo.apply(cursor)
        assert cp.CharFontName == "Noto Serif Cond"
        assert cp.CharFontStyleName == "Italic"
        assert lang == cp.CharLocale
        cursor.gotoEnd(False)
        FontOnly.default.apply(cursor)
        Write.end_paragraph(cursor)

        # fd = fo._get_font_descriptor("Lucida Fax", "Demibold Italic")
        # assert fd is not None

        Lo.delay(delay)
    finally:
        Lo.close_doc(doc)
