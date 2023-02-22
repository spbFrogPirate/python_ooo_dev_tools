from __future__ import annotations
import pytest

if __name__ == "__main__":
    pytest.main([__file__])

import uno
from ooodev.format.writer.modify.frame.wrap import Spacing, StyleFrameKind
from ooodev.utils.gui import GUI
from ooodev.utils.lo import Lo
from ooodev.office.write import Write
from ooodev.exceptions import ex as mEx


def test_write(loader, para_text) -> None:
    # delay = 0 if Lo.bridge_connector.headless else 3_000
    delay = 0

    doc = Write.create_doc()
    if not Lo.bridge_connector.headless:
        GUI.set_visible()
        Lo.delay(500)
        GUI.zoom(GUI.ZoomEnum.ENTIRE_PAGE)
    try:
        cursor = Write.get_cursor(doc)
        if not Lo.bridge_connector.headless:
            Write.append_para(cursor=cursor, text=para_text)

        style = Spacing(all=2.8)

        style.apply(doc)
        # props = style.get_style_props(doc)

        f_style = Spacing.from_style(doc=doc, style_name=style.prop_style_name)
        assert f_style.prop_inner.prop_left == pytest.approx(style.prop_inner.prop_left, rel=1e2)
        assert f_style.prop_inner.prop_right == pytest.approx(style.prop_inner.prop_right, rel=1e2)
        assert f_style.prop_inner.prop_top == pytest.approx(style.prop_inner.prop_top, rel=1e2)
        assert f_style.prop_inner.prop_bottom == pytest.approx(style.prop_inner.prop_bottom, rel=1e2)

        Lo.delay(delay)
    finally:
        Lo.close_doc(doc)
