"""Test for ooodev.format.draw.direct.area.Color"""
# pylint: disable=no-member
# pylint: disable=unused-import
# pylint: disable=unused-argument
# pylint: disable=wrong-import-order
# pylint: disable=wrong-import-position
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=invalid-name
from __future__ import annotations
import pytest
from typing import TYPE_CHECKING

if __name__ == "__main__":
    pytest.main([__file__])

import uno
from ooodev.utils.gui import GUI
from ooodev.utils.lo import Lo
from ooodev.office.draw import Draw

from ooodev.format.draw.direct.area import (
    Gradient,
    GradientStyle,
    PresetGradientKind,
    Offset,
    ColorRange,
    IntensityRange,
)

from ooodev.utils.color import StandardColor

if TYPE_CHECKING:
    from com.sun.star.drawing import FillProperties  # service


def test_draw(loader) -> None:
    # Tabs inherits from Tab and tab is tested in test_struct_tab
    delay = 0
    # delay = 0 if Lo.bridge_connector.headless else 3_000

    doc = Draw.create_draw_doc()
    if not Lo.bridge_connector.headless:
        GUI.set_visible()
        Lo.delay(500)
        GUI.zoom(GUI.ZoomEnum.ZOOM_75_PERCENT)
    try:
        slide = Draw.get_slide(doc)

        width = 36
        height = 36
        x = int(width / 2)
        y = int(height / 2)

        rec = Draw.draw_rectangle(slide=slide, x=x, y=y, width=width, height=height)
        style = Gradient.from_preset(preset=PresetGradientKind.DEEP_OCEAN)
        style.apply(rec)

        f_style = Gradient.from_obj(rec)
        assert f_style.prop_inner == style.prop_inner

        Lo.delay(delay)
    finally:
        Lo.close_doc(doc)